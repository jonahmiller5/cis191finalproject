#!/bin/python


import re #processes regex
import os #lets us un bash commands or get information about the system
import datetime
from crontab import CronTab #shecdule cron jobs
import random


#method for handling user input
def user_input():

    print("Welcome to the mail scheduler tool")
    print("This tool requires a functioning mail command")
    print("")

    #regex to ensure well formed emails
    regex = re.compile("[a-zA-Z0-9\.]+@[a-zA-Z0-9\.]+\.[a-zA-Z]+")
    emails = list() #list to store input emails
    while (len(emails) == 0):
        rec = input("Who would you like to send the email to?\n")
        emails = regex.findall(rec)
        if len(emails) == 0:
            print("Email format not recognized, please try again\n")
        print("")
    
    subj = input("What is the subject of the email?\n")
    
    print("Enter the contents of the email, press enter twice when finished")
    multiline = []
    
    #loop continues until the user presses enter twice so that they can inpur multi line emails
    while True:
        line = input()
        if line:
            multiline.append(line)
        else:
            break
    body = '\n'.join(multiline)
  
    #determines to send email now or later
    sendnow = False
    while True:
        now_or_later = input("Would you like to send the email now [y/n]")
        
        if now_or_later == 'y':
            sendnow = True
            break
        elif now_or_later == 'n':
            sendnow = False
            break
        else:
            print ("input not recognized")
            print ("")
    
    if not sendnow :
        schedule (emails, subj, body)
    else:
        send_email(emails, subj, body)

#method for sending email right now
def send_email(emails, subj, body):
   
    file = open(".sendnow.txt", 'w')
    file.write(body)
    file.close()
    cmd = baseCommand(emails, subj) 
    cmd = cmd + " < .sendnow.txt"
    os.system(cmd)
    os.system("rm .sendnow.txt")
    print ("email sent")

#shedules the email for a lter date
def schedule(emails, subj, body):
    cmd = baseCommand(emails, subj)
    keepGoing = True
    date = datetime.datetime(2020, 1, 1)

    #user inputs date, must be a proper date
    while keepGoing:
        try:
            year = getNum('year (at least 2020)')
            month = getNum('month (1-12)')
            day = getNum('day (1-31, depending on the month)')
            hour = getNum('hour (0-23)')
            minute = getNum('minute (0-59)')
            keepGoing = False
            date = datetime.datetime(year, month, day, hour, minute) 
        except:
            keepGoing = True
            print("Date forman not valid, please try again")

    #creates a cron job for the email send
    randnum = str(random.randint(1, 1000))
    filename = ".email" + randnum + ".txt"

    #writes the body of the messge in a random txt file that will be removed after the email is sent
    file = open(filename, 'w')
    file.write(body)
    file.close()
    filename = os.getcwd() +"/" +  filename
    atTime = date.strftime("%H:%M %x")
    cmd = "echo '" +  cmd + " < " + filename + " && rm " +  filename + "' | at " + atTime
    os.system(cmd)
    print ("Email scheduled for " + str(date))


#forms base command for sending email
def baseCommand(emails, subj):
    list_emails = ' '.join(emails)  
    cmd =  "mail -s ' " + subj + "' " + list_emails 
    return cmd

#helper method for scheduling emails
def getNum(type): 
    return  int (input("Enter the " + type + " you want the email sent: "))
 

#Main method, starts by getting user input
if __name__ == '__main__':
    user_input()
    
