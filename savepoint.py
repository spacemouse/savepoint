# save point
# version 1.0
# by spacemouse
# licensed under creative commons
import sys, traceback
import urllib
from lxml import html
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import json
import cgi


def converttext(text):
    retext = ((((text.encode_contents()).decode()).replace('\n', '<br />')).replace('\r', '')).encode('ascii', 'xmlcharrefreplace') 
    return retext.decode()

print("------- SAVE POINT -------")
print("---------Ver. 1.0---------")
print("------By SpaceMouse-------")
print("-Licenced under CC: BY-SA-")

# input URL
url = input("Input thread URL: ")
#url = "https://tgchan.org/kusaba/questarch/res/692327.html"
parts = url.split('//', 1)
domain = parts[0]+'//'+parts[1].split('/', 1)[0]
#domain = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
# output file
outputfile = input("Specify output file: ")
#outputfile = "text.json"
# which mode? 1: all posts with images 2: all posts by authorname with images
#print("1: All posts with images")
#print("2: All posts by authorname with images")
try:
    #whichmode = int(input("Specify mode: "))
    whichmode = 1
except ValueError:
    # not number
    print("That is not a number.")
    sys.exit(0)

# is number
if (whichmode < 1) or (whichmode > 2):
    print("Invalid mode.")
    sys.exit(0)

print("Alright.")
#open file, initialize
#with open(outputfile, mode='w', encoding='utf-8') as f:
#    json.dump([], f)
# open url
with urllib.request.urlopen(url) as response:
   page = response.read()
#page = html.fromstring(theraw)
soup = BeautifulSoup(page, 'html.parser')
i = 1 #iterations
mainthread = soup.find("form", id="delform") #find the main thread
firstpostdiv = mainthread.find("div", class_="postwidth") # this has the first image in it
firsta = firstpostdiv.find("a")
firstpostimg = firsta.find_next("a") # this is the first image
firstpostimgsrc = domain + firstpostimg['href'] # first image
firstpostblock = mainthread.find("blockquote") # this is the text of the first post
firstpoststring = converttext(firstpostblock)
#firstpoststring = firstpostblock.text
#firstpoststring = "".join([str(item) for item in firstpostblock.contents])
print(firstpostimgsrc)
print("-")
print(firstpoststring)
print("--")
with open(outputfile, mode='w', encoding='utf-8') as f:
    #thejson = json.load(f)
    firstpage = [{'pagenum' : i, 'img' : firstpostimgsrc, 'text' : str(firstpoststring)}]
    thejson = {'pages' : [{}]}
    thejson['pages'].append(firstpage)
    #thejson.append(firstjson)
    #json.dump(firstjson,f, indent=4, sort_keys=True)

#sweet the first one is done, now the rest are easier
#with open(outputfile, mode='r+', encoding='utf-8') as f:
#    thejson = json.load(f)
    for tag in mainthread.find_all("table"):
        i = i + 1 #increment post number
        postdiv = tag.find("div", class_="postwidth") #find the post
        #we need to check if this has an image
        if (postdiv.find("img")): #has an image
            postimg = postdiv.find("a", target="_blank")

            checkstring = postimg['href']
            if ("sage" in checkstring):
                postimg = postimg.find_next("a")
            postimgsrc = domain + postimg['href'] # first image
            postblock = tag.find("blockquote") # this is the text of the first post
            #poststrings = postblock.strings
            poststring = converttext(postblock)
            print(postimgsrc)
            print("-")
            print(poststring)
            print("--")
            newpage = [{'pagenum' : i, 'img' : postimgsrc, 'text' : str(poststring)}]
            #newjson = {'pages' : newpage }
            thejson['pages'].append(newpage)
    # finally, write to file
    json.dump(thejson,f, indent=4, sort_keys=True)
#we're done, now make it look good
#thefile = open(outputfile, "r+")
# magic happens here to make it pretty-printed
#thefile.write(simplejson.dumps(simplejson.loads(thefile), indent=4, sort_keys=True))
#thefile.close()
print("Done")
