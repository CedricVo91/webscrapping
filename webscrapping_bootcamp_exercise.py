#1. outer while loop to go through the pages until no more pages available
#2. inner loop to go through all the job names (saved before in a list) -> create a function like "scrape_page" to reuse is a best practice
#3. outer outer loop to go through each job name and get the job lists data (add data to the df)

#each job name tag: <span data-cy="page-header" title="1 796 Data Engineer job offers" class="Span-sc-1ybanni-0">1 796 Data Engineer job offers</span>
#each job better: <input value="Data Engineer"
#new page tag: found it using chatgpt on the arrow key on the bottom using the tag "a",{"data-cy":"paginator-next"} i.e. soup.find("a",{"data-cy":"paginator-next"})["href"]

import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

#First steps:
#define a base url and a specific url you are inspecting called "url"
base_url = "https://www.jobs.ch"
url = "https://www.jobs.ch/en/vacancies/?term=Data%20Engineer"


###
#3. def a scrape page function to always use inside the main construct i.e. outer loop -> the url needs to be adjusted for the job name
# look for job title, date, company name, location

#data container to save entries. Here, a dictionary is sutiable: a) structured saving, b) easy transferable into pandas data frame
# look for job title, date, company name, location

#using these three different tags to get job info:
#job_title_first_job = listed_jobs[0].find("a", {"data-cy":"job-link"}).get("title")
#job_date_first_job = listed_jobs[0].find_all("span", {"class":"Span-sc-1ybanni-0 Text__span-sc-1lu7urs-12 Text-sc-1lu7urs-13 ftUOUz eEFkdA"})
#job_companyinfo_first_job = listed_jobs[0].find_all("p",{"class": "P-sc-hyu5hk-0 Text__p2-sc-1lu7urs-10 Span-sc-1ybanni-0 Text__span-sc-1lu7urs-12 Text-sc-1lu7urs-13 cHnalP cTUsVs"} )

#print(job_title_first_job)
#print(job_date_first_job[0].text)
#company_name_first_job = job_companyinfo_first_job[0].text
#company_location_first_job = job_companyinfo_first_job[1].text
#print(company_name_first_job)
#print(company_location_first_job)

#next step: structure this information in the data dictionary and create a function to reuse in main script 

aggregate_data = []

def scrape_data(url):
    scrape_data = {}
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    #getting a list of all jobs on the jobpage i.e. they all have the same class tag and data-cy
    listed_jobs = soup.find_all("article", {"data-cy":"serp-item"}, {"class":"Div-sc-1cpunnt-0 VacancySerpItem__ShadowBox-sc-ppntto-0  fHeZup"})
    for i in range(len(listed_jobs)):
        
            scrape_data["job_title"] = listed_jobs[i].find("a", {"data-cy":"job-link"}).get("title")
            scrape_data["date"] = listed_jobs[i].find_all("span", {"class":"Span-sc-1ybanni-0 Text__span-sc-1lu7urs-12 Text-sc-1lu7urs-13 ftUOUz eEFkdA"})[0].text
            scrape_data["company name"] = listed_jobs[i].find_all("p",{"class": "P-sc-hyu5hk-0 Text__p2-sc-1lu7urs-10 Span-sc-1ybanni-0 Text__span-sc-1lu7urs-12 Text-sc-1lu7urs-13 cHnalP cTUsVs"})[0].text
            try: #I had to insert this because of an error which occured 
                scrape_data["location"] = listed_jobs[i].find_all("p",{"class": "P-sc-hyu5hk-0 Text__p2-sc-1lu7urs-10 Span-sc-1ybanni-0 Text__span-sc-1lu7urs-12 Text-sc-1lu7urs-13 cHnalP cTUsVs"})[1].text
            except:
                pass
            aggregate_data.append(scrape_data.copy())
    


###################################################################
#code block to go through the different job names
#pattern in main link: https://www.jobs.ch/en/vacancies/?term=Data%20Scientist or "https://www.jobs.ch/en/vacancies/?term=Data%20Engineer"




def jobs_to_be_searched(url, job_titles = ["Data Scientist", "Data Analyst", "Python Developer", "Data Engineer", "Data Manager", "Data Architect", "Big Data Analyst", "Data Python"]):
    job_titles = job_titles
    job_titles_in_link = []
    job_links = []
    #get the names in the correct url form
    for job in job_titles:
        link_job_name = ""
        for entry in job.split(" "):
            link_job_name += entry +"%20"
            
        link_job_name = link_job_name[:-3]
        job_titles_in_link.append(link_job_name)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_title_link = soup.find("link",{"rel":"canonical"})["href"]
    job_title_link = job_title_link.split("=")[0]

    for entry in job_titles_in_link:
        url = job_title_link + "=" + entry
        job_links.append(url)
    
    return job_links

#print(jobs_to_be_searched(url, job_titles=["Data Scientist", "Data Analyst", "Python Developer", "Data Engineer", "Data Manager", "Data Architect", "Big Data Analyst", "Data Python"]))



#get the correct links to access each job title and its second page! works

    #print(base_url+next_page)






#################################################################
#code block to browse through the pages per predefined job

def scrape_pages(url, base_url):
    while url:
        page = requests.get(url) #works -> if I use the right url 
        soup = BeautifulSoup(page.content, 'html.parser')
        scrape_data(url)
        next_page = soup.find("a",{"data-cy":"paginator-next"})# does not works if I use the abbreviated link (=base url) above..only works if I use https://www.jobs.ch/en/vacancies/?page=2&term=Data%20Engineer
        if next_page:
            url = base_url + next_page["href"]
        else:
            url = None




base_url = "https://www.jobs.ch" #, "Data Analyst", "Python Developer", "Data Engineer", "Data Manager", "Data Architect", "Big Data Analyst", "Data Python"]
urls = jobs_to_be_searched(url, job_titles=["Data Scientist", "Data Analyst", "Python Developer", "Data Engineer", "Data Manager", "Data Architect", "Big Data Analyst", "Data Python"])
aggregate_data = []

for url in urls:
    scrape_pages(url, base_url)

df1 = pd.DataFrame(aggregate_data) #do a research on how to incorporate data in dictionary into pdf...seems like a list of dictionary works directly, but not a dict -> write down in notion seperate area
#print(df1)


