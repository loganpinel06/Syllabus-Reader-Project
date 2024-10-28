#Syllabus Reader Project
#Logan Pinel
#October 10, 2024

#import os to access the folder with the files
import os
#import regex
import re
#import pypdf and the PdfReader
import pypdf
from pypdf import PdfReader
#import pandas to make DataFrames (tables)
import pandas as pd   

#folder path for files
folderPath = '/Users/loganpinel/Folders/Coding/Python/Syllabus Reader Project/files'

#define the files that we are reading
pdfFile1 = "csc101 syllabus.pdf"
pdfFile2 = "mat261 syllabus.pdf"
pdfFile3 = "crm101 syllabus.pdf"
#define the written txt files path
txtFile1 = "csc101 syllabus.txt"
txtFile2 = "mat261 syllabus.txt"
txtFile3 = "crm101 syllabus.txt"

#subroutine to join the folder and file paths together
def joinPaths(folder, file):
    fullPath = os.path.join(folder, file)
    return fullPath

#define a regex for date patters example "Sep 25"
datePatterns = r"\b(Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\b" #had chatgpt help me write this pattern

#method to read the pdf
def readPdf(file):
    #create an empty string for the syllabus
    syllabus = ""
    #define the reader for the pdf
    reader = PdfReader(file)
    #loop through all the pages in the pdf
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()
        syllabus += text
                
    return syllabus

#method to write a txt file
def writeTxt(pdf, txt):
    #create a full path for the txt file
    fullTxtPath = joinPaths(folderPath, txt)
    #wrtie the txt file
    with open(fullTxtPath, "w") as newFile:
        newFile.write(pdf)
    #return the txt file to the folder path
    return fullTxtPath

#method to trace through the txt file and refine the data
def searchTxtFile(txtFile):
    #define an empty list
    syllabusList = []
    #variable to check if under a line where the regex is true
    underRegex = False
    with open(txtFile, "r") as file:
        #loop through each line in the file
        for line in file:
            #strip the lines
            line = line.rstrip("\n")
            #search for both regex patterns
            if re.search(datePatterns, line):
                syllabusList.append(line.strip())
                underRegex = True
                #if the line contains the date for the final return the syllabusList
                #so we dont get any unnecessary data
                if "Dec 11" in line:
                    return syllabusList
            #if the underRegex is true append the lines underneath the found 
            #date incase those lines are also dates but dont have months listed
            elif underRegex:
                syllabusList.append(line.strip())

    return syllabusList

#method to convert the syllabusList into a table
def createTable(syllabusList):
    #define the data being used
    data = {
        "Schedule": syllabusList
    }
    #define the DataFrame (table)
    dataFrame = pd.DataFrame(data)
    return dataFrame

#getDataFrame() method will get the dataFrame
def getDataFrame(pdfFile, txt):
    #join the paths together
    pdfFilePath = joinPaths(folderPath, pdfFile)
    txtFilePath = writeTxt(folderPath, txt)
    #get the Data Frame
    pdf = readPdf(pdfFilePath)
    txtFile = writeTxt(pdf, txtFilePath)
    syllabusList = searchTxtFile(txtFile)
    dataFrame = createTable(syllabusList)
    return dataFrame

#get the dataframes and create the csv file
dataFrame1 = getDataFrame(pdfFile2, txtFile2)

#create a csv file and save it into the folder path
csvFilePath = joinPaths(folderPath, "dataFrame.csv")
dataFrame1.to_csv(csvFilePath, index=False)





    