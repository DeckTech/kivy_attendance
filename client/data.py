import os
import csv

#Creating My own data object called person

class Person:
    def __init__(self,first_name,last_name,reg_no,department,password):
        self.first_name = first_name
        self.last_name = last_name
        self.reg_no  = reg_no
        self.department = department
        self.password = password

    def __repr__(self):
        print(f"First name:{ self.first_name } \n Last name: { self.last_name } \n Reg_No:{ self.reg_no } \n Department: { self.department }")

    def person_data(self):

        return {
            'first_name':self.first_name,
            'last_name': self.last_name,
            'reg_no':self.reg_no,
            'department': self.department,
            'password':self.password
        }


#Get the home folder
def get_home_folder():
    home_folder = os.path.expanduser("~")
    if not os.path.isdir(home_folder):
        home_folder = os.environ.get("HOME") or os.environ.get("EXTERNAL_STORAGE") or "/storage/emulated/0"

    return home_folder

#Handling data from csv file
class File_Handler:
    def __init__(self):
        os.chdir(get_home_folder())
        self.file_name = "student_data.csv"

    def check_file(self):
         if os.path.isfile(self.file_name):
             return True
         else:
             return False

    def read_file(self):
        if os.path.isfile(self.file_name):
            with open(self.file_name,"r") as data:
                reader = csv.DictReader(data)
                row = next(reader,None)
                return row
        else:
                pass

    def write_file(self,content):
        with open(self.file_name,"w") as data:
            writer = csv.DictWriter(data,content.keys())
            writer.writeheader()
            writer.writerow(content)
