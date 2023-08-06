import os
from time import sleep

class Data():
    def __init__(self, file_name, text, onePress=False):
        self.file_name = file_name
        self.text = text
        self.onePress = onePress

        if onePress == True:
            sleep(0.100)
            try:
                self.file = open(file_name, "r")
            except:
                try:
                    self.my_file = open(file_name, "w+")
                    self.my_file.write(text)
                    self.my_file.close()
                except:
                    self.my_file = open(file_name, "w+")
                    self.my_file.write(text)
                    self.my_file.close()

        if onePress == False:
            sleep(2)
            try:
                file = open(file_name, "r")
            except:
                try:
                    os.mkdir("Data")
                    my_file = open(f"Data/{file_name}", "w+")
                    my_file.write(text)
                    my_file.close()
                except:
                    my_file = open(f"Data/{file_name}", "w+")
                    my_file.write(text)
                    my_file.close()

class Upload_data():
    def __init__(self, file_name, text_start, onePress=False):
        self.file_name = file_name
        self.text_start = text_start
        self.onePress = onePress
    def up1(self, file_name, text, text_if2, onclickFunction=None, onclickFunction_2=None):
        self.file_name = file_name
        self.text = text
        self.text_if2 = text_if2
        self.onclickFunction = onclickFunction
        self.onclickFunction_2 = onclickFunction_2
        try:
            if text in open(rf'Data/{file_name}'):
                fons = 'gray'
                self.onclickFunction()
            elif text_if2 in open(rf'Data/{file_name}'):
                fons = '#DCDCDC'
                self.onclickFunction_2()
            else:
                my_file = open(rf"Data/{file_name}", "w")
                my_file.write(text)
                my_file.close()
        except:
            pass
    def up2(self, file_name, text, text_if2, text_if3, onclickFunction=None, onclickFunction_2=None, onclickFunction_3=None):
        self.file_name = file_name
        self.text = text
        self.text_if2 = text_if2
        self.text_if3 = text_if3
        self.onclickFunction = onclickFunction
        self.onclickFunction_2 = onclickFunction_2
        self.onclickFunction_3 = onclickFunction_3
        try:
            if text in open(rf'Data/{file_name}'):
                self.onclickFunction()
            elif text_if2 in open(rf'Data/{file_name}'):
                self.onclickFunction_2()
            elif text_if3 in open(rf'Data/{file_name}'):
                self.onclickFunction_3()
            else:
                my_file = open(rf"Data/{file_name}", "w")
                my_file.write(text)
                my_file.close()
        except:
            pass


# False = лож
# True = правда


# import Data_Save

# def r20():
#     print('text if 1')
# def r670():
#     print('text if 2')
# def r620():
#     print('text if 3')

# Data_Save.Data("save_play.save", "text if 1") # Create a file named "save_play.save" and with the text "text if 1"

# test = Data_Save.Upload_data("save_play.save", "Home") # make the initial word for verification
# test.up2("save_play.save", "text if 1", "text if 2", "text if 3", r20, r670, r620)

# # call functions (r20, r670, r620)

# # result: text if 1



import Data_Save

def r20():
    print('text if 1')
def r670():
    print('text if 2')

Data_Save.Data("save_play.save", "text if 1") # Create a file named "save_play.save" and with the text "text if 1"

test = Data_Save.Upload_data("save_play.save", "Home") # make the initial word for verification
test.up2("save_play.save", "text if 1", "text if 2", r20, r670)

# call functions (r20, r670, r620)


# def r20():
#     print('GREEN')
# def r670():
#     print('RED')
# def r620():
#     print('gray')

# # Data("hipi.hi", 'input({"(hipi)" + GREEN} {"->" + WHITE})')

# up = Upload_data("hipi.hi", 'input({"(hipi)" + GREEN} {"->" + WHITE})')
# up.up2("hipi.hi", 'input({"(hipi)" + REC} {"->" + WHITE})', 'input({"(hipi)" + RED} {"->" + WHITE})', 'input({"(hipi)" + GRAY} {"->" + WHITE})', r20, r670, r620)
