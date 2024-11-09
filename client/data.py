import os
import csv

#Creating My own data object called person

class Person():
    def __init__(self,first_name,last_name,reg_no,department):
        self.first_name = first_name
        self.last_name = last_name
        self.reg_no  = reg_no
        self.department = department

    def __repr__(self): #Returning data just incase I need to log errors

        print(f"First name:{ self.first_name } \n Last name: { self.last_name } \n Reg_No:{ self.reg_no } \n Department: { self.department }")

        return {
            'first_name':self.first_name,
            'last_name': self.last_name,
            'reg_no':self.reg_no,
            'department': self.department
        }


#Get the home folder
def home_folder():
    home_folder = os.path.expanduser("~")
    if not os.path.isdir(home_folder):
        home_folder = os.environ.get("HOME") or os.environ.get("EXTERNAL_STORAGE") or "/storage/emulated/0"

    return home_folder

#Handling data from csv file
data_folder = home_folder()
data_file = os.path.join(data_folder)
