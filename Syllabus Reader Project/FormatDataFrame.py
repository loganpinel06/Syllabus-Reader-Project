#Format Data Frame will create a nice table in a txt file of the correct schedule for
#the semester using tabulate
#Logan Pinel
#October 24, 2024

#import os to access the folder with the files
import os
#import regex
import re
#import pandas
import pandas as pd
#import tabulate to format the dataFrame nicely
from tabulate import tabulate

#folder path for files
folderPath = '/Users/loganpinel/Folders/Coding/Python/Syllabus Reader Project/files'

#csvFile name
csvFile = "dataFrame.csv"

#define a regex for date patters example "Sep 25"
datePatterns = r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\b"
#define a regex for quiz/exam/final and review exam patterns example "Quiz 1"
quizPatterns = r"\b(?:Quiz|Review Exam|Review for Exam|Exam|Final|Review for Final)\s+\d*\b"
#regex for the week numbers that interfere with the data
weekNumbers = r"^\d+\s+"

#subroutine to join the folder and file paths together
def joinPaths(folder, file):
    fullPath = os.path.join(folder, file)
    return fullPath

#get the file path
filePath = joinPaths(folderPath, csvFile)

#subroutine to get all data
def getSchedule(filePath):
    #load the csv file
    dataFrame = pd.read_csv(filePath)
    #set the correct column in the dataframe
    scheduleColumn = dataFrame.columns[0]
    #make sure the colum is of type string using .astype()
    dataFrame[scheduleColumn] = dataFrame[scheduleColumn].astype(str)
    #arrays for dates, topics, and quizzes
    dates = []
    topics = []
    quizzes = []
    #loop through the DataFrame in the csv file which is named 'Schedule'
    for line in dataFrame['Schedule']:
        #get the dates
        dateMatch = re.search(datePatterns, line)
        #if match
        if dateMatch:
            date = dateMatch.group(0)
        #if nothing fill blank
        else:
            date = None
        #get the quiz matches
        quizMatch = re.search(quizPatterns, line)
        #if match
        if quizMatch:
            quiz = quizMatch.group(0)
        #if nothing fill blank
        else:
            quiz = ""
        #get the topics
        #remove the dates and quizzes and  week numbers from the line
        topicLine = re.sub(datePatterns, '', line)
        topicLine = re.sub(quizPatterns, '', topicLine)
        topicLine = re.sub(weekNumbers, '', topicLine).strip() #strip the line
        #if the topicLine has data append the topics list
        if topicLine:
            topics.append(topicLine)
        #if nothing in topics
        else:
            topicLine = ""
        
        #append the dates and quizzes lists
        dates.append(date)
        quizzes.append(quiz)

    return dates, topics, quizzes

#subroutine to create the dataFrame
def createScheduleDF(dates, topics, quizzes):
    #check is the lengths arent equal
    if len(dates) != len(topics) != len(quizzes):
        #Fill in the shorter list with empty strings
        maxLength = max(len(dates), len(topics), len(quizzes))
        dates += [None] * (maxLength - len(dates))
        topics += [''] * (maxLength - len(topics))
        quizzes += [''] * (maxLength - len(quizzes))

    data = {
        "DATES": dates,
        "TOPICS": topics,
        "Quizzes": quizzes
    }
    #define the dataframe
    scheduleDataFrame = pd.DataFrame(data)
    return scheduleDataFrame

dates, topics, quizzes = getSchedule(filePath)
scheduleDataFrame = createScheduleDF(dates, topics, quizzes)

#format the table using tabulate
tableSchedule = tabulate(scheduleDataFrame, headers='keys', tablefmt='heavy_grid', showindex=False) #'keys' takes the names of the columns from the DF

#create a new txt file for the final schedule
txtFilePath = joinPaths(folderPath, "Schedule.txt")
#write the formated dataFrame to a txt file
with open(txtFilePath, 'w') as file:
    file.write(tableSchedule)

