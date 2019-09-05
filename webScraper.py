#Allows initialization of a browser
from selenium import webdriver
#ALlows searching of things using specific parameters
from selenium.webdriver.common.by import By
#Allows waiting for a page to load
from selenium.webdriver.support.ui import WebDriverWait
#Specifies what to look for on a specific page to determine that the webpage has loaded
from selenium.webdriver.support import expected_conditions as EC
#Handles timeout situations
from selenium.common.exceptions import TimeoutException
import mysql.connector
import time
from termcolor import colored


#Adds an incognito argument to the webdriver
option = webdriver.ChromeOptions()
option.add_argument(" - incognito")

#Initalizes the Chrome browser
browser = webdriver.Chrome(executable_path='/Users/reed/Documents/selenium/chromedriver', chrome_options=option)

#Connects to MySQL Database
mydb = mysql.connector.connect(
    host=#Removed for security,
    user="rfodge",
    passwd=#Removed for security,
    database="hosp"
)

#Fetches all of the websites from database
mycursor = mydb.cursor()
mycursor.execute("SELECT WEBSITE FROM hospitalList")
myresult = mycursor.fetchall()

websiteList = []

#Adds all the websites to a list
for x in myresult:
    websiteList.append(str(x))

#Formats the websites
websiteList = [e[3:len(e)-3] for e in websiteList]

def findAllInDomain(a):
    hrefArr = []
    try:
        browser.get(a)
    except:
        print colored("ERROR GETTING URL", "red")
    hrefs = browser.find_elements_by_xpath("//a[@href]")
    for i in hrefs:
        try:
            hrefString = i.get_attribute("href")
        except:
            print colored("ATTRIBUTE ERROR", "red")
        domainString = a[4:len(a)-1]
        #print(hrefString, domainString)
        if(hrefString.find(domainString) != -1):
            hrefArr.append(hrefString)
    return hrefArr

def findAllHref(a):
    hrefArr = []
    try:
        browser.get(a)
    except:
        print colored("ERROR GETTING URL", "red")
    hrefs = browser.find_elements_by_xpath("//a[@href]")
    for i in hrefs:
        try:
            hrefString = i.get_attribute("href")
        except:
            print colored("ATTRIBUTE ERROR", "red")
        hrefArr.append(hrefString)
    return hrefArr

def checkString(href):
    if "financ" in href:
        return True
    elif "bill" in href:
        return True
    elif "charge" in href:
        return True
    elif "pay" in href:
        return True
    elif "pric" in href:
        return True

suffix = {".pdf", ".xls", ".xslx", ".csv", ".xml", ".zip"}

# for a in websiteList:
#     mainHref = findAllInDomain(a)
#     visitedPage = []
#     keywordPages = []
#     #Gets all the hrefs on the original page
#     print colored("MAIN HREF: " + a, "magenta")
#     for x in mainHref:
#         print colored("SUB HREF (1): " + x, 'cyan')
#         #Avoids examining repeated domains
#         if(x not in visitedPage):
#             if(checkString(x)):
#                 keywordPages.append(x)
#             #Gets all the sub hrefs for every href on the original page
#             subHrefs = findAllInDomain(x)
#             for y in subHrefs:
#                 if(y not in visitedPage):
#                     print colored("SUB HREF (2): " + y, 'blue')
#                     #Checks if href has specific keywords indicating pricing information
#                     if(checkString(y)):
#                         keywordPages.append(y)
#                         #print(y)
#                         #Gets every href on pricing-related page
#                         tertiaryHref = findAllHref(y)
#                         for b in tertiaryHref:
#                             if(b not in visitedPage):
#                                 foundFile = False
#                                 #Checks to see if any hrefs end with suffixes for data files
#                                 for c in suffix:
#                                     if(str(b).endswith(c)):
#                                         print colored("SUB HREF (3): " + b, 'green')
#                                         foundFile = True
#                                 if(not foundFile):
#                                     quartHref = findAllHref(b)
#                                     for d in quartHref:
#                                         if(d not in visitedPage):
#                                             foundFile = False
#                                             for c in suffix:
#                                                 if(b.endswith(c)):
#                                                     print colored("SUB HREF (4): " + b, 'yellow')
#                                                     foundFile = True
#                                             visitedPage.append(d)
#                                 visitedPage.append(b)
#                     visitedPage.append(y)
#             visitedPage.append(x)
#         print("----------")
#     print("KEYWORD PAGES: ")
#     for k in keywordPages:
#         print(k)
#     print("====================")

for a in websiteList:
    visitedPages = []
    keywordPages = []
    layer1 = findAllInDomain(a)
    visitedPages.append(a)
    for l1 in layer1:
        if(l1 not in visitedPages):
            visitedPages.append(l1)
            layer2 = findAllInDomain(l1)
            for l2 in layer2:
                if(l2 not in visitedPages):
                    visitedPages.append(l2)
                    layer3 = findAllInDomain(l2)
                    for l3 in layer3:
                        if(l3 not in visitedPages):
                            visitedPages.append(l3)
                            layer4 = findAllInDomain(l3)
                            for l4 in layer4:
                                if(l4 not in visitedPages):
                                    visitedPages.append(l4)
    for v in visitedPages:
        if(checkString(v)):
            keywordPages.append(v)
    print("Keyword Pages:")
    for i in keywordPages:
        print(i)
    print("===================================")
