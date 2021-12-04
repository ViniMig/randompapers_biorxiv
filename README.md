# Random Papers (Biorxiv) - Notion integration

This is an adaptation of Random Papers code from McGill Space Institute. This was changed to do a similar job but using the Biorxiv repository. Original code: https://github.com/andrewcumming/randompapers

Motivation
----
The motivation behind this small project is to avoid getting lost in a sea of options and ending up demotivating form reading papers at all because of not being able to chose. With this said, after googling a little bit I found the McGill Space Institute's Random Papers page and their code available to use, so decided to work on it and adapt it for my own needs.
A few months ago my wife introduced me to Notion and I underrated it quite quickly. However now with a second wind of energy and motivation decided that in terms of organizing my thoughts and my life it is a great tool, even though some people have amazingly stunning dashboards I am quite the simplist myself so nothing very extravagant will be made. Just some easy to access and read dashboard with exactly what i need and no visual distractions.

How does it work
----
This is quite a simple python script. It can be divided in 3 steps:
1. Retrieve papers through a request to the Biorxiv API and randomly select 5:
    * In this case we are requesting specifically a list of any papers between the current day and 7 days before;
    * The random selection is done by a call to numpy random.choice.
2. Create the Notion blocks with all the information:
    * Create general blocks with information that is general to all the papers (mostly text blocks in Notion referring to the page properties in the data base and general information about the papers);
    * Create blocks respective to each individual paper selected (set the Toggle and To-do blocks in Notion);
    * Create blocks with a small reference to the original Random Papers project.
3. Update and Publish Notion pages:
    * Update existing head page "Status" tag to "Past" (if database not empty);
    * Publish page to database which will appear at the top of the table in Notion with the "Status" tag "New".

The output of running the script is thus a Notion page with the 5 selected random papers of the week, containing: Category, Author, date, doi, title and a url to the paper. Each is set in a To-Do block so it can be checked upon reading. The to-do are inserted inside toggles containing the category, author name and date for tydiness.

_Additionally for each time the code is executed a new Notion page is created and the Status tag of previous ones renamed from "New" to "Past"._

Automation
---
For simplicity this process of executing the script is automated with a Windows Task Scheduler task. I have a .bat file set which calls my python.exe with the environment which contains the required packages installed and executes this specific script on a weekly basis.

How to use
---
**This code can be used and modified by anyone who so wishes, this is a small contribution of mine to anyone interested.**

Anyone can use this directly just by executing the python script in the src folder. My current configuration is:

![Image](https://img.shields.io/badge/python-3.8-informational) 

With packages:

![Image](https://img.shields.io/badge/numpy-v1.21.4-informational)

![Image](https://img.shields.io/badge/requests-v2.26.0-informational)

**You will need to create an additional constants.py file (named just as it is being imported in the script), in the same directory as the script, containing 2 variables defined:**
  - NOTION_TOKEN = "your notion integration token"
  - NOTION_DB_ID = "your notion database id"
As the names suggest these are your specific Notion token and database id upon configuring your Notion integration. More information on what these are and how to get them configured please refer to [Notion API documentation](https://developers.notion.com/docs).

Future ideas
---
From some feedback by posting on reddit an idea is to allow for retrieval of papers by doi. This will most likely be the next step of this project. Additional to this, maybe wouldn't be so bad to try and implement this with an executable and a first basic UI to allow for input of things such as: **Notion token**, **Notion database id**, **mode select** (random | get specific paper),**doi**, **...**. The first 2 I may rethink them as it will become a very repètitive process to input the same 2 keys all the time vs having them stored locally, an hybrid solution may be better.

One idea in the back of my mind is to also try to implement some kind of statistics such as "favoured category" or "hottest keyword in titles read", or some other things i may think of.


Random Papers working:
---
https://user-images.githubusercontent.com/72768584/144718339-0daba357-ba8d-4ff8-9d78-cc59c986f316.mp4
