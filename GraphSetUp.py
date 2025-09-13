
import requests

#----------------------------------------- Making the Graph ------------------------------------------#

#TOKEN = 
#USERNAME = 
#GRAPHID = 

pixela_endpoint = "https://pixe.la/v1/users"

HEADERS = {
    "X-USER-TOKEN": TOKEN
}

def graphSetUp(unit="units", dataType="float", color="kuro", timezone="America/Los_Angeles"):       #Everything that goes into setting up an account to creating a new pixel graph (not currently in use)

    user_params = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
    }

    # response = requests.post(url=pixela_endpoint, json=user_params)           #succsess in creating an account
    # print(response.text)

    graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

    newGraph_config = {
        "id": GRAPHID,
        "name": GRAPHID,
        "unit": unit,
        "type": dataType,
        "color": color,
        "timezone": timezone
    }

    # response = requests.post(url=graph_endpoint, json=newGraph_config, headers=headers)       #success in creating a graph
    # print(response.text)