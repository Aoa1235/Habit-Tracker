
#Ugly Habit Tracker

#visit the page: https://pixe.la/@loserwithproblems

#Idea - By tracking how often an addiction in a day, I hope to become more aware of it

# Current Implementations:
#
# Use a Pixela graph that updates with an increase in number for a particular day
# seperated classes into seperate files for ease of use
# make a tkinter interface
#   option to choose a day
#   option to choose number of times
#   quick "today" option
#   add, update, and delete pixel options
#   default date and spinbox
#   message boxes instead of command window errors
#       differentiates between errors
#   if "update" used on a non-existing pixel, given option to "add" a new pixel
#   ignore request rejections from pixela and still go through and setup retry senarios in event of other errors
#   made seperate "status" window to display data:
#       maxQuantity, avgQuantity (overall), Average Quantity (in past week) - **WIP, todaysQuantity, yesterdayQuantity, totalQuantity since minDate
#   detect whether date is in correct format (no letters, correct format) 
#
# Problems to be resolved
#   
# 
#
# Future Implentations
# 
# display an updating graph (WIP)
# more detailed error message titles
# after clicking increase button, spinbox should reset
# default date showing correct format should only be placeholdere - idea: https://stackoverflow.com/questions/27820178/how-to-add-placeholder-to-an-entry-in-tkinter
# make a revisable window for making choices
#   for making a window in updatePixel (ClassPixel) to either replace a pixel, increase a pixel, or cancel (message windows dont allow for button editing)
# 
# if go gitHub route:
#   make important global variables enviromental
#   re-organize code for easy reading (including adding explaination comments)
#   make interactive funcionality to create, config, and delete graphs

from ClassPixel import Pixel
from ClassPixelUI import PixelUI

pixel = Pixel()             #See ClassPixel
pixel_UI = PixelUI(pixel)   #See ClassPixelUI
