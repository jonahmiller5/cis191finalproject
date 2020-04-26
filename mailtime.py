#!/usr/bin/python3

import re
import os
import datetime
from crontab import CronTab
import random

def user_input():
    print("Welcome to the mail scheduler tool")
    print("This tool requires a functioning mail command")
    print("")
    regex = re.compile("[a-zA-Z0-9\.]+@[a-zA-Z0-9\.]+\.[a-zA-Z]+")
    emails = list()
    while (len(emails) == 0):
        rec = input("Who would you like to send the email to?\n")
        emails = regex.findall(rec)
        if len(emails) == 0:
            print("Email format not recognized, please try again\n")
        print("")
    
    subj = input("What is the subject of the email?\n")
    
    print("Enter the contents of the email, press enter twice when finished")
    multiline = []
    while True:
        line = input()
        if line:
            multiline.append(line)
        else:
            break
    body = '\n'.join(multiline)
  
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

def send_email(emails, subj, body):
   
    file = open(".sendnow.txt", 'w')
    file.write(body)
    file.close()
    cmd = baseCommand(emails, subj) 
    cmd = cmd + " < .sendnow.txt"
    os.system(cmd)
    os.system("rm .sendnow.txt")
    print ("email sent")

def schedule(emails, subj, body):
    cmd = baseCommand(emails, subj)
    keepGoing = True
    date = datetime.datetime(2020, 1, 1)
    while keepGoing:
        try:
            year = getNum('year')
            month = getNum('month')
            day = getNum('day')
            hour = getNum('hour (0-24)')
            minute = getNum('minute')
            keepGoing = False
            date = datetime.datetime(year, month, day, hour, minute) 
        except:
            keepGoing = True
            print ("Date forman not valid, please try again")
    cron = CronTab(user='jon')
    randnum = str(random.randint(1, 1000))
    filename = ".email" + randnum + ".txt"
    file = open(filename, 'w')
    file.write(body)
    file.close()
    filename = os.getcwd() +"/" +  filename
    print(filename)
    cmd = cmd + " < " + filename + " && rm " +  filename

    job = cron.new(command=cmd)
    job.setall(date)
    cron.write()
    print ("Email scheduled for " + str(date))



def baseCommand(emails, subj):
    list_emails = ' '.join(emails)  
    cmd =  "mail -s ' " + subj + "' " + list_emails 
    return cmd

def getNum(type): 
    return  int (input("Enter the " + type + " you want the email sent: "))
 


if __name__ == '__main__':
    user_input()
    
