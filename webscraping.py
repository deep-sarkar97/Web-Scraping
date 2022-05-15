#Importing Libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import copy

Host = "https://www.stfrancismedicalcenter.com"
url = "https://www.stfrancismedicalcenter.com/find-a-provider/"
search_param = "_m_=FindAPhysician&PhysicianSearch$HDR0$PhysicianName=&PhysicianSearch$HDR0$SpecialtyIDs=&PhysicianSearch$HDR0$Distance=5&PhysicianSearch$HDR0$ZipCodeSearch=&PhysicianSearch$HDR0$Keywords=&PhysicianSearch$HDR0$LanguageIDs=&PhysicianSearch$HDR0$Gender=&PhysicianSearch$HDR0$InsuranceIDs=&PhysicianSearch$HDR0$AffiliationIDs=&PhysicianSearch$HDR0$NewPatientsOnly=&PhysicianSearch$HDR0$InNetwork=&PhysicianSearch$HDR0$HasPhoto=&PhysicianSearch$FTR01$PagingID="
header_data = {'Content-Type': 'application/x-www-form-urlencoded'}

all_profile = []
profile_data = {}
page = 1
while(page<=38):
    #checking for progress
    print(page)
    # Fetching Data from the page
    response = requests.post(url,data=search_param + str(page),headers=header_data)
    # Parsing the Data
    soup = BeautifulSoup(response.content, 'html5lib')
    table = soup.find('ul', attrs = {'class':'system-cards items-452'})

    for row in table.findAll('li', attrs = {'data-role':'tr'}):
        profile_data["name"] = row.findAll('span',attrs={'class':"title-style-5"})[0].text
        try:
            profile_data["speciality"] = row.findAll('div',attrs={'class':"specialty-list items-1 note-style-1 ui-repeater"})[0].text.replace("\n","").replace("\t","")
        except:
            profile_data["speciality"] = ""
        profile_data["Address"]=row.find('meta',{"itemprop":"streetAddress"})["content"]+ \
            row.find('meta',{"itemprop":"addressLocality"})["content"]+ \
                row.find('meta',{"itemprop":"addressRegion"})["content"]+ \
                    row.find('meta',{"itemprop":"postalCode"})["content"]+ \
                        row.find('meta',{"itemprop":"addressCountry"})["content"]
        profile_data["city"] =  row.find('meta',{"itemprop":"addressLocality"})["content"]
        profile_data["state"] = row.find('meta',{"itemprop":"addressRegion"})["content"]
        profile_data["zip"] = row.find('meta',{"itemprop":"postalCode"})["content"]
        profile_data["telephone"] = row.find('meta',{"itemprop":"telephone"})["content"]
        profile_data["URL"]= Host+row.findAll('a',attrs={'class':"flex-top-between-block-500"})[0]['href']
        all_profile.append(copy.copy(profile_data))
    page = page+1

print(all_profile)
#List to dataframe
df = pd.DataFrame(all_profile)
print(df)
df.to_csv("profiles.csv")