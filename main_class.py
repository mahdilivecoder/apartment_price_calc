import requests
import re
import csv
from sklearn import tree
import os
from util.transform import transform
from util import os_tools
from util import validation

class Data:
    desc_list=[]
    def find_description(format,text):
        """
        Generate description from created info using regex, 
        add data to global variable desc_list using for loop
        desc_list will pass object to transform class to
        creeat suitable data for saving into houses.csv
        """
        Uri_description=re.findall(format,text)
        Uri_description=[(lambda x:x.replace("<!-- -->",""))(x) for x in Uri_description]
        counter=-1
        for i in Uri_description:
            if not "مسکونی" in i:
                Data.desc_list[counter].append(i)
            elif "مسکونی" in i:
                Data.desc_list.append([i,])
                counter+=1
            else:
                pass

    @staticmethod
    def get_the_info():
        #Should first clear the latest filled descriptions list
        Data.desc_list.clear()
        #Fetch links from killid website
        links=["https://kilid.com/buy-apartment/tehran-saadat_abad",
               "https://kilid.com/buy-apartment/tehran-saadat_abad?page=1",
               "https://kilid.com/buy-apartment/tehran-saadat_abad?page=2",
               "https://kilid.com/buy-apartment/tehran-saadat_abad?page=3",
               "https://kilid.com/buy-apartment/tehran-saadat_abad?page=4"
               ]
        Uri_Text=""
        for html_index in links:
            Uri_Text=Uri_Text+requests.get(html_index).text
        return Uri_Text
    
    def ceate_info():
        #Get responses from main get_info function
        Uri_Text=Data.get_the_info()
        #Exclude Prices from Sloppy response
        Uri_default_price=re.findall('<p class="text-primary-700">(.*?)</p>',Uri_Text)
        #geting houses locations
        def get_location(Uri_Text):
            location=list()
            default_location=re.findall('<p class="inline-flex text-grey-500">(.*?)</p>',Uri_Text)
            for i in default_location:
                sanitized_loc=re.findall('<span>(.*?)</span>',i)
                sanitized_loc=str(sanitized_loc)
                sanitized_loc=sanitized_loc[1:] ; sanitized_loc=sanitized_loc.replace(']','')
                location.append(sanitized_loc)
            return location
        
        location=get_location(Uri_Text)
        #Getting actual price from default price
        def get_pure_price(Uri_default_price): 
            Uri_price=list()
            for i in Uri_default_price:
                left_side=i.replace('<span class="text-lg font-bold">','')
                i_compl=left_side.replace('</span>','')
                Uri_price.append(i_compl)
            return Uri_price
        Uri_price=get_pure_price(Uri_default_price)
        #Selecting Descriptions and appending to class list (desc)        
        Data.find_description('<span class="px-2 py-1 m-2 text-sm font-medium rounded-lg bg-grey-100 text-grey-700 whitespace-nowrap">(.*?)</span>',Uri_Text)
        #Make Csv file to Write
        with open("houses.csv",'+w') as csv_file:
            csv_writer=csv.writer(csv_file)
            csv_writer.writerow(["Prices","Type","Bedroom","Parking","Metraj","Location",])
            counter=0
            desc_list=Data.desc_list
            for i in Uri_price:
                if "توافقی" in i:
                    row=0
                else:
                    row=transform.make_trans_price(i[5:])
                if len(desc_list[counter])==4:
                    i_desc_list=desc_list[counter]
                    parking=transform.make_trans_parking(i_desc_list[2])
                    type=transform.make_trans_type(i_desc_list[0])
                    bedroom=transform.make_trans_bedroom(i_desc_list[3])
                    metraj=transform.make_trans_metraj(i_desc_list[1])
                    location_int=transform.make_trans_location(location[counter])
                    csv_writer.writerow([row,type,bedroom,parking,metraj,location_int])
                    counter+=1
                elif len(desc_list[counter])==3:
                    i_desc_list=desc_list[counter]
                    parking=0
                    type=transform.make_trans_type(i_desc_list[0])
                    bedroom=transform.make_trans_bedroom(i_desc_list[2])
                    metraj=transform.make_trans_metraj(i_desc_list[1])
                    location_int=transform.make_trans_location(location[counter])
                    csv_writer.writerow([row,type,bedroom,parking,metraj,location_int])
                    counter+=1
            print("Done!")

class data_entry:
    type=validation.validate_data_entry()
    bedroom=validation.validate_data_entry()
    parking=validation.validate_data_entry()
    metraj=validation.validate_data_entry()
    location_int=validation.validate_data_entry()
    def __init__(self):
        self.type=input("Please enter the type of the apartment between 0-0\n")
        self.parking=input("Pleae enter the number of parking in the house 1-5\n")
        self.bedroom=input("Please enter the number of bedroom \n")
        self.metraj=input("Please enter the metraj of the apartment from 1 - 9999\n")
        self.location=input("Please enter the location in number \n(for example the saddat abbad is in 2 zone of tehran)\n")

def predict_data():
    with open("houses.csv",'r+') as csv_file:
        csv_reader=csv.reader(csv_file)
        counter=0
        price=[]
        description=[]
        for line in csv_reader:
            if counter>=1:
                price.append(line[0])
                description.append(line[1:6])
            counter+=1
    clf=tree.DecisionTreeClassifier()
    clf.fit(description,price)
    enter_data=data_entry()
    newdata=[[enter_data.type,enter_data.bedroom,enter_data.parking,enter_data.metraj,enter_data.location]]
    answer=clf.predict(newdata)
    @os_tools.os_check
    def answer_pr(answer):
            print(answer)
    answer_pr(answer[0])
    main()     

def inner_main():
    path="houses.csv"
    if os.path.isfile(path) and os.access(path,os.R_OK):
            predict_data()
            main()
    else:
        Data.ceate_info()
        predict_data()
@os_tools.os_check
def main():
    while True:
        print("Welcome to the apartment price predictor!")
        print("1.Predict the price \n2.Update The data\n3.exit()")
        menu_number=int(input())
        match menu_number:
            case 1:
                inner_main()
            case 2:
                    if os.path.isfile("houses.csv"):
                        try:
                            print("Updataing...")
                            Data.ceate_info()
                            os.system("clear")
                            print("Update Compeleted!")
                            continue
                        except ConnectionError("Can not load new data(Connection problem!)"):
                            continue
                    else:
                        print("Please first start the program (Select 1 from menu!)")
                        continue 
            case 3:
                print("**Good bye!**")
                exit()
main()