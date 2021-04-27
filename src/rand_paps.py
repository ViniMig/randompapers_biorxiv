import requests
import numpy as np
from datetime import date
from datetime import timedelta
import os
import time
import glob

api_key=''
www_dir = './'

# Rename the index.html file using its creation date
try:
	previous_fname = time.strftime("%Y_%m_%d.html",time.localtime(os.path.getmtime(www_dir+'index.html')))
	os.rename(www_dir+'index.html',www_dir+previous_fname)
except:
	pass

# Open a new index.html file and write the header
fp = open(www_dir+"index.html","w")

fp.write('''<html>
  <head>
	<meta name="viewport" content="width/device-width" charset="utf-8">
  	<title>Random Papers</title>
	<link rel="stylesheet" href="style.css">
  </head>
  <body>
  <div class="heading">
  <h1>Random Papers</h1>
  </div>
  <div class="container">''')

fp.write("<h4>This week's papers</h4>")

# Work out the month and year to search
today = date.today()
lastweek = today - timedelta(days=7)

# make the request
r=requests.get('https://api.biorxiv.org/details/biorxiv/'+ lastweek.strftime("%Y-%m-%d") +'/'+ today.strftime("%Y-%m-%d"))
print(r.url)
print('Response: ', r.status_code)
out = r.json()
# choose random numbers
num_papers=out["messages"][0]["count"]
choice = np.random.choice(num_papers,5,replace=False)
print("num_papers, choice=",num_papers,choice)

# print out the info about the chosen papers
docs = out["collection"]
choice_count = 1
for i in choice:
	doc = docs[i]
	authors = list(doc["authors"].split(";"))
    
	num_authors = len(authors)
	name = str(authors[0])
	fp.write(name.split(',')[0])
	if num_authors > 2:
		fp.write(' et al. ')
	if num_authors == 2:
		name2 = str(authors[1])
		fp.write(' &amp; ' + name2.split(',')[0])
	
	fp.write(", Category: "+str(doc["category"]))
	fp.write(', '+str(doc["date"]))
	fp.write(", doi: "+str(doc["doi"]))
	fp.write(", title: <a href=https://www.biorxiv.org/content/"+str(doc["doi"])+"v"+str(doc["version"])+">"+str(doc["title"])+"</a><br>")    
	fp.write('</font></p>')
	
	namestring=''
	for name in authors:
		namestring = namestring + name + ', '
	choice_count+=1

# summary information
fp.write("<P>Selected on %s, %d %s from a total of %d papers published last month in Biorxiv</p>" % (today.strftime("%A"),today.day,today.strftime("%B %Y"),num_papers))

# About
fp.write("<h4>This uses an adaptation of the code used for Random Papers, please refer to the code at the bottom</h4>")
fp.write("<h4>About Random Papers</h4>")
fp.write('''<p>We meet every second Monday at noon at the <a href="http://msi.mcgill.ca/">McGill Space Institute</a> to discuss 5 random astrophysics papers.</p>
<p>The goal of Random Papers is to gain a broad view of current astrophysics research. For each meeting, we run a script to choose 5 random papers published in the last month in refereed astrophysics journals. This gives a different slice of the literature than the typical astro-ph discussion, with papers from outside our own research areas or those that might not otherwise be chosen for discussion.</p>
<p>Rather than reading each paper in depth, the goal is to focus on the big picture, with questions such as: How would we summarize the paper in a few sentences? What are the key figures in the paper? What analysis methods are used? Why is this paper being written, and Why now?
</p>
''')

# make a list of previous random papers
fp.write("<h4>Previous random papers</h4>")

file_list = glob.glob(www_dir+'*.html')
file_list = [os.path.basename(file) for file in file_list]
file_list.sort(reverse=True)
for fname in file_list:
	if fname!='index.html':
		fp.write('<a href="'+fname+'">'+fname.replace("_",".")[:-5]+'</a> ')

fp.write('''<p><br>
Image credit: <a href="https://www.nasa.gov/image-feature/celestial-fireworks">NASA/HST</a><br>
Code: <a href="https://github.com/andrewcumming/randompapers">GitHub</a><br>
<a href="feed.xml">RSS</a>
</p>''')
fp.write("</div></body></html>")

fp.close()
