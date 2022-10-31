import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import csv
import LocationChecker
import Webscraper_Linkedin
import Webscraper_Handshake
import Webscraper_Indeed
import Webscraper_GetJobText
import ProcessingText
import Webscraper_GetStopwords
import easygui as gui
import Webscraper_JobFinder as JobFinder
import sys

class GUI:

    #Starts the Program
    def __init__(self):
        start = gui.buttonbox("Welcome to the Resume Optimizer?", title='Resume Optimizer', choices=["Start", "Exit"])
        if start == "Exit" or start is None:
            sys.exit()

        importantMessage = "Before The Program Begins, Would You Like This Program To Gather Stopwords From Multiple Job Postings? \nThis Will Add At Least An Hour To Your Wait Time BUT Give More Refined Results For What Words They Are \nLooking For In Your Resume. \n\n This Is Not Recommended If You Have Done This Recently, But IS Recommended If You Have Never Done This."
        self.stopwordCheck = gui.ynbox(importantMessage, title='Resume Optimizer')

        self.Questionare()
        gui.msgbox("Please Do Not Close The Browser That Will Open Up After Reading This Message \nAt Any Point While Using The Program Or It Will Cause An Error!")
        self.JobFinder = JobFinder.JobFinder(self.field, self.type, self.location, self.inPerson, self.fullTime, self.salary, self.experience)
        gui.msgbox("This Browser Is What Will Be Referred To As The Selenium Browser. \nAgain, Please Do NOT Close This Browser At Any Point During The Program!")
        self.DoProgram()

    def DoProgram(self):

        #self.JobFinder.LoginToJobs()
        #self.JobFinder.GetJobLinks()
        #self.JobFinder.GetJobText()

        #if self.stopwordCheck == "Yes":
            #self.JobFinder.GetStopWords()

        specialWordsAndDictonary=self.JobFinder.ProcessJobText()

        for dic in specialWordsAndDictonary:
            print(dic)

        self.JobFinder.EndProgram()


    def Questionare(self):
        msg1 = "What Field Of Work Are You Looking For?"
        fow = "Field Of Word"
        self.field = gui.enterbox(msg1, title='Resume Optimizer')
        if self.field is None:
            sys.exit()
        elif len(self.field) > 0:
            self.field.lower()


        msg2 = "Are You Looking For a Job or Internship?"
        joi = ["Job", "Internship"]
        self.type = gui.buttonbox(msg2, title='Resume Optimizer', choices=joi)
        if self.type is None:
            sys.exit()
        else:
            self.type.lower()

        while True:
            msg3 = "What city do you want this job to be located at? \nIf you are not looking for a specific location leave these fields blank"
            cos = ["City", "State"]
            cityAndState = gui.multenterbox(msg3, title='Resume Optimizer', fields=cos)

            if cityAndState is None:
                sys.exit()
            if cityAndState[0] == "" and cityAndState[1] == '':
                self.location = ""
                break
            elif LocationChecker.isCity(cityAndState[0]) and LocationChecker.isState(cityAndState[1]):
                if LocationChecker.isLocation(cityAndState[0] + "," + cityAndState[1]):
                    self.location = cityAndState[0] + "," + cityAndState[1]
                    break
                else:
                    gui.msgbox("The City And State You Have Choosen Do Not Exist Together. \nPlease Try Again.")
            else:
                if len(cityAndState[0]) > 0 and len(cityAndState[1]) > 0:
                    gui.msgbox("The City And State You Have Choosen Do Not Exist Together. \nPlease Try Again.")
                else:
                    gui.msgbox("You Must Either Leave Both Fields Blank or Fill Them BOTH Out. \nPlease Try Again.")

        msg4 = "Do You Want This Job To Be Remote, In Person, or Both?"
        roip = ["Remote", "In Person", "Both"]
        self.inPerson = gui.buttonbox(msg4, title='Resume Optimizer', choices=roip).lower()
        if self.inPerson is None:
            sys.exit()
        else:
            self.inPerson.lower()

        msg5 = "Do You Want This Job To Be Full Time, Part Time, Or Both?"
        ftopt = ["Full Time", "Part Time", "Both"]
        self.fullTime = gui.buttonbox(msg5, title='Resume Optimizer', choices=ftopt).lower()
        if self.fullTime is None:
            sys.exit()
        else:
            self.fullTime.lower()

        msg6 = "What Salary Are You Looking For? \nType In 0 If You Aren't Looking For A Specific Salary"
        self.salary = gui.integerbox(msg6, title='Resume Optimizer')
        if self.salary is None:
            sys.exit()

        msg7 = "What Is The Highest Level Of College Education You Have?"
        degree = ["Associate", "Bachelor", "Masters", "None"]
        self.education = gui.buttonbox(msg7, title='Resume Optimizer', choices=degree).lower()
        if self.education is None:
            sys.exit()
        elif self.education == "None":
            self.experience = ''
        else:
            self.education.lower()

        msg8 = "What is your experience level?"
        experience = ["Entry", "Mid", "Senior", "None"]
        self.experience = gui.buttonbox(msg8, title='Resume Optimizer', choices=experience).lower()
        if self.experience is None:
            sys.exit()
        elif self.experience == "None":
            self.experience = ''
        else:
            self.experience.lower()



"""
    def Questionare(self):

        msg1 = "What Field Of Work Are You Looking For?"
        fow = ["Field Of Word"]
        self.field = gui.multenterbox(msg1, title='Resume Optimizer', fields=fow)
        print(self.field)
        if self.field is None:
            return None
        elif len(self.field) > 0:
            self.field.lower()



        msg2 = "Are You Looking For a Job or Internship?"
        joi = ["Job", "Internship"]
        self.type = gui.buttonbox(msg2, title='Resume Optimizer', choices=joi)
        if self.type is None:
            return None
        else:
            self.type.lower()

        while True:
            msg3 = "What city do you want this job to be located at? \nIf you are not looking for a specific location leave these fields blank"
            cos = ["City", "State"]
            cityAndState = gui.multenterbox(msg3, title='Resume Optimizer', fields=cos)
            if cityAndState is None:
                return None
            if cityAndState[0] == "" and cityAndState[1] == '':
                self.location = ""
            elif LocationChecker.isCity(cityAndState[0]) and LocationChecker.isState(cityAndState[1]):
                if LocationChecker.isLocation(cityAndState[0] + ","+ cityAndState[1]):
                    self.location = cityAndState[0] + ","+ cityAndState[1]
                    break
                else:
                    gui.msgbox("The City And State You Have Choosen Do Not Exist Together. \nPlease Try Again.")
            else:
                gui.msgbox("You Must Either Leave Both Fields Blank or Fill Them BOTH Out. \nPlease Try Again.")



        msg4 = "Do You Want This Job To Be Remote, In Person, or Both?"
        roip = ["Remote", "In Person", "Both"]
        self.inPerson = gui.buttonbox(msg4, title='Resume Optimizer', choices=roip).lower()
        if self.inPerson is None:
            return None
        else:
            self.inPerson.lower()

        msg5 = "Do You Want This Job To Be Full Time, Part Time, Or Both?"
        ftopt = ["Full Time", "Part Time", "Both"]
        self.fullTime = gui.buttonbox(msg5, title='Resume Optimizer', choices=ftopt).lower()
        if self.fullTime is None:
            return None
        else:
            self.fullTime.lower()


        msg6 = "What Salary Are You Looking For? \nType In 0 If You Aren't Looking For A Specific Salary"
        self.salary = gui.integerbox(msg6, title='Resume Optimizer')
        if self.salary is None:
            return None

        msg7 = "What Is The Highest Level Of College Education You Have?"
        degree = ["Associate", "Bachelor", "Masters", "None"]
        self.education = gui.buttonbox(msg7, title='Resume Optimizer', choices=degree).lower()
        if self.education is None:
            return None
        else:
            self.education.lower()

        msg8 = "What is your experience level?"
        experience = ["Entry", "Mid", "Senior", "None"]
        self.experience = gui.buttonbox(msg8, title='Resume Optimizer', choices=experience).lower()
        if self.experience is None:
            return None
        else:
            self.experience.lower()
"""

GUI()
