
from GraphSetUp import *

from datetime import datetime
from tkinter import messagebox

class Pixel:

    #----------------------------------------- Updating a pixel on the graph ------------------------------------------#

    def updatePixel(self, increaseAmount, updateDate):          #updates a pixel's quanitity based on the amountToIncrease spinbox (see ClassPixelUI)

        pixel_status_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPHID}/{updateDate}"

        getResponse = pixelaRequests(endpoint=pixel_status_endpoint, command="get", argDate=updateDate)


        if getResponse == -1:           #pixel failed to be accessed
            return
        elif getResponse == 0:          #date had no existing pixel
            newQuantity = increaseAmount
        else:                           #procedure finished and got the pixel quantity
            pixel_quantity = int(getResponse.json()["quantity"])

            #Messy for user please fix
            updateChoice = messagebox.askyesnocancel(title=f"Updating pixel for {readableDate(updateDate)}", message=f"Would you like to replace the current pixel with the value {pixel_quantity} with {increaseAmount}?\nOtherwise the increased amount will be added on top of the current amount. (cancel to return to original screen)")
            
            if updateChoice == None:  #user chooses cancel to return
                return
            elif updateChoice:        #user chooses to replace pixel
                newQuantity = increaseAmount
            else:                     #user chooses to increase amount
                newQuantity = pixel_quantity + increaseAmount

        #new Quantity turned into a json format
        new_pixel_data = {
            "quantity": str(newQuantity)
        }
        
        #updates the pixel
        updateResponse = pixelaRequests(endpoint=pixel_status_endpoint, jsonData=new_pixel_data, command="put", argDate=updateDate)

        if updateResponse == -1 or updateResponse == 0:          #if request failed, return to original screen
            return
        else:                                  #if request succeeds, message states it
            messagebox.showinfo(title="Success", message="Pixel Successfully Updated")


    # def updatePixel(self, increaseAmount, addOrIncrease: str, updateDate):          #Restructure function to support board drawing (functions in function maybe?)

    #     okToUpdate = messagebox.askyesno(title="Update?", message=f"Increase the pixel for {readableDate(updateDate)} by {increaseAmount}?")
        
    #     if not okToUpdate:
    #         return

    #     update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPHID}/{updateDate}"

    #     if addOrIncrease == "inc":      #if increasing amount, add original data to new one

    #         changeToAdd = False
    #         #Getting the related pixel

    #         getResponse = pixelaRequests(endpoint=update_endpoint, command="get")

    #         if getResponse == -1:          #if request failed, return to original screen
    #             return
    #         elif getResponse == 0:         #if nonexisting pixel for date
    #             changeToAdd = messagebox.askyesno(title="Add a new Pixel?", message="Make a new pixel for the provided date instead?.")

    #         if changeToAdd:             #if adding amount, replace original data
    #             newQuantity = increaseAmount
    #         else:
    #             #gets the quantity
    #             self.currPixelQuantity = int(getResponse.json()["quantity"])

    #             #update with new quantity
    #             newQuantity = self.currPixelQuantity + increaseAmount
    #     else:                           #if adding amount, replace original data
    #         newQuantity = increaseAmount

    #     self.new_pixel_data = {
    #         "quantity": str(newQuantity)
    #     }
        
    #     updateResponse = pixelaRequests(endpoint=update_endpoint, jsonData=self.new_pixel_data, command="put")              #updates a piece of data

    #     if updateResponse == -1 or 0:          #if request failed, return to original screen
    #         return
    #     else:
    #         messagebox.showinfo(title="Success", message="Pixel Successfully Updated")

    #----------------------------------------- Deleting a pixel on the graph ------------------------------------------#

    def deleteDate(self, delDate):                  #delete a pixel with a corresponding input date from PixelUpdaterWindow (see ClassPixelUI)

        okToDel = messagebox.askyesno(title="Delete?", message=f"Delete the pixel for {readableDate(delDate)}?")
        
        if not okToDel:
            return

        delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPHID}/{delDate}"
        
        deleteResponse = pixelaRequests(endpoint=delete_endpoint, command="delete", argDate=delDate)

        if deleteResponse == -1:          #if request failed, return to original screen
            return
        elif deleteResponse == 0:           #if there is an invalid format
            messagebox.showerror(title="Format Error", message="The inputed date does not have a pixel and therfore no data pertaining to it.")
        else:
            messagebox.showinfo(title="Success", message="Pixel Successfully Deleted")

    #----------------------------------------- Access a Pixel's Status ------------------------------------------#

    def pixelStatus(self, argDate):         #Returns the json of the stats endpoint for the statsTab (see ClassPixelUI)

        graph_status_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPHID}/stats"

        statusResponse = pixelaRequests(endpoint=graph_status_endpoint, command="get", argDate=argDate)

        if statusResponse == -1 or statusResponse == 0:        #if request failed, return to original screen
            return
        
        return(statusResponse.json())

    #----------------------------------------- Get the current graph ------------------------------------------#

    def getCurrentGraph(self):                  #not currently working - something wrong with it getting the library

        import cairosvg
        
        graph_image_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPHID}"

        graph_image = requests.get(url=graph_image_endpoint, headers=HEADERS)
        graph_image.raise_for_status()

        #print(type(self.graph_image.text))

        # with open("svgGraph.txt", "w") as file:
        #     file.write(self.graph_image.text)           #verified svg text

        cairosvg.svg2png(bytestring=self.graph_image.raw, write_to="graph.png")
        #return(graph_image)

   #----------------------------------------- Requests from Pixela ------------------------------------------#

#put and post are the only ones that need inputted jsondata
def pixelaRequests(endpoint, command: str, jsonData = None, argDate: str = None):           #manages all requests going to the api Pixela as well as errors from it

    #Returns:
    # if return 0 -> there is no pixel associated with the date (but the date exists)
    # if return -1 -> there is a access problem with the endpoint or date format which has to be fixed either in code or by fixing date in PixelUpdaterWindow (see ClassPixelUI)

    try:
        match command:
            case "get":         #get request
                request = requests.get(url=endpoint, headers=HEADERS)
            case "delete":      #delete request
                request = requests.delete(url=endpoint, headers=HEADERS)
            case "put":         #put request
                request = requests.put(url=endpoint, json=jsonData, headers=HEADERS)
            case "post":        #post request
                request = requests.post(url=endpoint, json=jsonData, headers=HEADERS)
            case _:
                raise KeyError("command argument does not match previous cases")
        request.raise_for_status()
    except KeyError:                #if error above is raised
        return
    except:
        if request.status_code == 404:                                  #access to pixel fails due to non-exisiting pixel from date (will return to original screen)
            
            if not formatCheck(argDate):        #checks format of the date
                messagebox.showerror(title=f"{request.status_code} Error", message="The inputed date was in a invalid format")
                return -1
            else:
                return 0                      #value used for updatePixel function
        
        elif request.status_code == 503:                                #site rejects access 25% of time (will restart regardless of user)
            pixelaRequests(endpoint, command, jsonData)

        else:                                                           #other errors (user will be asked to retry)
            retry = messagebox.askretrycancel(title=f"{request.status_code} Error", message=f"The method: {command} has failed.\nPlease Try Again.")

            if retry:
                pixelaRequests(endpoint, command, jsonData)
            else:
                return -1                #value used for previous functions
            
    else:
        return(request)

def readableDate(argDate):                      #reorganizes date into readable fashion

    #takes in account date being in YYYYMMDD setup
    dateList = {}
    dateList["year"] = argDate[0:4]
    dateList["month"] = argDate[4:6]
    dateList["day"] = argDate[6:8]

    #makes it a MM/DD/YYYY string
    newDate = f"{dateList["month"]}/{dateList["day"]}/{dateList["year"]}"
    return(newDate)

def formatCheck(argDate: str):                  #Checks the format of the date
    
    #Date should be in YYYYMMDD setup
    #All Checks:
    #   length of date string
    #   realistic days and months
    #   no letters or other special characters (only numbers)

    dateList = {}
    try:
        dateList["year"] = int(argDate[0:4])
        dateList["month"] = int(argDate[4:6])
        dateList["day"] = int(argDate[6:8])
    except:             #if argDate string is not long enough, it will throw an error and is wrong format
        return(False)
    else:
        #if the month or day is greater or less than what already exists wrong format or if there is anything other than a number
        if not argDate.isnumeric() or dateList["month"] > 12 or dateList["month"] < 1 or dateList["day"] > 31 or dateList["day"] < 1:
            return(False)
        else:           
            return(True)