# -*- coding: UTF-8 -*-
#Created by Martin Kodada, 4.11.2019
#save the trees, friends

#Used frameworks

import requests  #to get HTML
from bs4 import BeautifulSoup
import time #To set the loop
import tweepy


def Get_latest_donor():
    #Variables for the functions
    URL = 'https://teamtrees.org/'
    headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
    page = requests.get(URL, headers = headers)
    soup= BeautifulSoup(page.content, 'html.parser')

    totalTrees = int(soup.findAll("div",{"id": "totalTrees"})[0].get("data-count"))
    if totalTrees <= 20000000:
       totalTrees_left = 20000000 - totalTrees#the goal is 20 000 000
    else:
       totalTrees_left = totalTrees
    
    List_of_donors = soup.findAll("div",{"class":"media pt-3"})
    name = List_of_donors[0].findAll("strong")[0].text
    messege = List_of_donors[0].findAll("span",{"class": "d-block medium mb-0"})[0].text
    treecount = List_of_donors[0].findAll("span",{"class":"feed-tree-count"})[0].text
    donor = [totalTrees_left,name, treecount,messege]
    return donor

def Parse_text(donor):
    text = "Just " + str(donor[0]) + " trees left thanks to " + donor[1] + " and their donation which planted " + donor[2]
    if donor[3] != "":
         text = text + "\n included message:" + donor[3]
    text = text + "\n #teamtrees"
    return text

def Post_twitter(donor,api): #it should be checking for the same tweets but right now it doesn't matter that much.
    text = Parse_text(donor)
    try:
        api.update_status(text)
    except:
        print("error")
    
def Loop(api):
    Post_twitter(Get_latest_donor(),api)
    print("sent")
    time.sleep(120) #change to adjust the posting
    Loop(api)
    
if __name__ == '__main__':
    auth = tweepy.OAuthHandler("KEY", "KEY 2")
    auth.set_access_token("KEY", "KEY 2")
    api = tweepy.API(auth)
    Loop(api)
