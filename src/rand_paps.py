import requests, json
import numpy as np
from datetime import date
from datetime import timedelta
import constants as cons

#retrieve notion token and database id
notion_token = cons.NOTION_TOKEN
notion_database = cons.NOTION_DB_ID
notion_headers = {
    "Authorization": "Bearer " + notion_token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
	}


#random papers code and notion implementation

# Work out the month and year to search
today = date.today()
lastweek = today - timedelta(days=7)

# make the request
r=requests.get('https://api.biorxiv.org/details/biorxiv/'+ lastweek.strftime("%Y-%m-%d") +'/'+ today.strftime("%Y-%m-%d"))
out = r.json()

# choose random numbers from the range of results
num_papers=out["messages"][0]["count"]
choice = np.random.choice(num_papers,5,replace=False)
print("num_papers, choice=",num_papers,choice)

# setup notion page object information
docs = out["collection"]
choice_count = 1
author_names = []
categories = []

#create list of notion children objects, append individual papers and remarks afterwards
notion_page_children = [{
				"object": "block",
				"type": "heading_1",
				"heading_1": {
					"text": [{ "type": "text", "text": { "content": "Random Papers" } }]
					}
			},
			{
				"object": "block",
				"type": "divider",
				"divider": {}
			},
			{
				"object": "block",
				"type": "heading_3",
				"heading_3": {
					"text": [
						{ "type": "text",
					      "text": {
							  "content": "This week's papers"
							  },
						  "annotations": {
							  "bold": True,
							  "color": "blue_background"
							  }
						  }
						]
				}
			}] 

#iterate through the selected results and create notion objects with the information about the papers
for i in choice:
	doc = docs[i]
	
	categories.append({"name": str(doc["category"])}) #set categories for tags of each week's papers
	authors = list(doc["authors"].split(";")) #get list of authors
	num_authors = len(authors) #determine how many authors in each paper for representation purposes
	name = str(authors[0])
	authors_var = name.split(',')[0]
	
	#if several authors add et al if only 2 add both if only 1 var will contain first name already
	if num_authors > 2:
		authors_var += " et al. " 
		
	if num_authors == 2:
		name2 = str(authors[1])
		authors_var += " & " + name2.split(',')[0]
	
	#create 5 children consisting on 5 toggles and each with one to-do child
	notion_page_children.append({
				"object": "block",
				"type": "toggle",
				"toggle": {
					   "text": [{
						        "type": "text",
								     "text": {
										 "content": str(doc["category"]) + ": " + authors_var + ", " + str(doc["date"])
										 },
									 "annotations": {
										 "bold": True,
										 "color": "green_background"
										 }
									 }],
					   "children":[{
						   "type": "to_do",
						   "to_do": {
							      "text": [{
									        "type": "text",
											"text": {
												"content": "DOI: "
												},
											"annotations": {
												"bold": True
												}												
											},
									        {
									        "type": "text",
											"text": {
												"content": str(doc["doi"])
												}												
											},
											{
											"type": "text",
											"text": {
												"content": "  Title: "
												},
											"annotations": {
												"bold": True
												}
											},
									        {
											"type": "text",
											"text": {
												"content": str(doc["title"]),
												"link": {
													"url": "https://www.biorxiv.org/content/" + str(doc["doi"]) + "v" + str(doc["version"])
													}
												}
											}
											],
								  "checked": False
								  }	
						   }]
				}
			})
	
	for name in authors:
		author_names.append({"name": name.replace(',', '')})#set for author tags in each week's papers
	
	choice_count+=1#don't remember why i have this count here, must be important (probably not)

#add a division and original random papers reference remarks
notion_page_children.extend(
	[{
	  "object": "block",
	  "type": "divider",
	  "divider": {}
	  },
#description
	{
	  "object": "block",
	  "type": "paragraph",
	  "paragraph": {
		  "text": [
			  {
				  "type": "text",
				  "text": {
					  "content": "Papers selected out of a total of " + str(num_papers) + " papers published in Biorxiv on the week of " + str(lastweek.day) + " - " + str(today.day) + " " + today.strftime("%B %Y")
					  }
				  }
			  ]
		  }
	  },
	
#remarks about  original Random Papers and reference to sources
	{
	  "object": "block",
	  "type": "paragraph",
	  "paragraph": {
		  "text": [
			  {
				  "type": "text",
				  "text": {
					  "content": "This uses an adaptation of the code used for Random Papers by McGill Space Institute, please refer to the code below"
					  },
				  "annotations": {
					  "bold": True
					  }
				  }
			  ]
		  }
	  },
	{
	  "object": "block",
	  "type": "heading_3",
	  "heading_3": {
		  "text": [
			  {
				  "type": "text",
				  "text": {
					  "content": "About Random Papers"
					  },
				  "annotations": {
					  "bold": True,
					  "color": "blue"
					  }
				  }
			  ]
		  }
	  },
	{
	  "object": "block",
	  "type": "paragraph",
	  "paragraph": {
		  "text": [
			  {
				  "type": "text",
				  "text": {
					  "content": "We meet every second Monday at noon at the "
					  },
				  "annotations": {
					  "italic": True
					  }
				  },
			  {
				  "type": "text",
				  "text": {
					  "content": "McGill Space Institute",
					  "link": {
						  "url": "http://msi.mcgill.ca/"
						  }
					  },
				  "annotations": {
					  "italic": True
					  }
			    },
			  {
				  "type": "text",
				  "text": {
					  "content": " to discuss 5 random astrophysics papers."
					  },
				  "annotations": {
					  "italic": True
					  }
				  }
			  ]
		  }
	  },	
	{
	  "object": "block",
	  "type": "paragraph",
	  "paragraph": {
		  "text": [
			  {
				  "type": "text",
				  "text": {
					  "content": "The goal of Random Papers is to gain a broad view of current astrophysics research. For each meeting, we run a script to choose 5 random papers published in the last month in refereed astrophysics journals. This gives a different slice of the literature than the typical astro-ph discussion, with papers from outside our own research areas or those that might not otherwise be chosen for discussion."
					  },
				  "annotations": {
					  "italic": True
					  }
				  }
			  ]
		  }
	  },
	{
	  "object": "block",
	  "type": "paragraph",
	  "paragraph": {
		  "text": [
			  {
				  "type": "text",
				  "text": {
					  "content": "Rather than reading each paper in depth, the goal is to focus on the big picture, with questions such as: How would we summarize the paper in a few sentences? What are the key figures in the paper? What analysis methods are used? Why is this paper being written, and Why now?"
					  },
				  "annotations": {
					  "italic": True
					  }
				  }
			  ]
		  }
	  },
	{
	  "object": "block",
	  "type": "paragraph",
	  "paragraph": {
		  "text": [
			  {
				  "type": "text",
				  "text": {
					  "content": "Code: "
					  },
				  "annotations": {
					  "italic": True
					  }
				  },
			  {
				  "type": "text",
				  "text": {
					  "content": "GitHub",
					  "link": {
						  "url": "https://github.com/andrewcumming/randompapers"
						  }
					  },
				  "annotations": {
					  "italic": True
					  }
			    }
			  ]
		  }
	  }
])

##define functions for notion

#read database, this will be used to obtain the page ids and iteratively update the status for existing one
def read_database():
	readUrl = 'https://api.notion.com/v1/databases/' + notion_database + '/query'
	resDB = requests.request("POST", readUrl, headers = notion_headers)
	resDB_json = resDB.json()
	return(resDB_json)

#function for crfeation of the new page with retrieved Biorxiv data	
def create_page():
	createUrl = "https://api.notion.com/v1/pages"
	new_page_data = {
		"parent": {"database_id": notion_database},
		"properties": {
            "Week": {
                "title": [
                    {
                        "text": {
                            "content": str(lastweek.day) + " - " + str(today.day) + " " + today.strftime("%B %Y")
                        }
                    }
                ]
            },
            "Status": {
                "multi_select": [
                    {
                        "name": "New"
                    }
                ]
            },
			"Tags":{
				"multi_select": categories
				},
			"Author":{
				"multi_select": author_names
				}
        },
		"children": notion_page_children
	}
	data = json.dumps(new_page_data)
	res = requests.request("POST", createUrl, headers=notion_headers, data=data)
	print("Page created status code: " + str(res.status_code))


#function to be used to update status property
def update_page(page_id):
	
	updateUrl = "https://api.notion.com/v1/pages/" + page_id
	
	updateData = {
        "properties": {
            "Status": {
                "multi_select": [
                    {
                        "name": "Past"
                    }
                ]
            }        
        }
    }
	
	data = json.dumps(updateData)
	updt_response = requests.request("PATCH", updateUrl, headers=notion_headers, data=data)
	print("Page update status code: " + str(updt_response.status_code))
#end of functions definition


def main():
	
	#Verify if pages exist in DB and update Status of the last added page (first in the list) to Past
	dbjson = read_database()
	if len(dbjson["results"]) > 0:
		pageID = dbjson["results"][0]["id"]
		update_page(pageID)
	else:
		print("Empty database, no tags to update")
	#Add new page
	create_page()

#call main
main()