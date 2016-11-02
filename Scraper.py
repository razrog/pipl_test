from linkding_scrape_utils import *
from lxml import html
import os ,re
import json,jsonschema
import geocoder


RESOURCES_FOLDER = "/linkedin/"
OUTPUT_FOLDER = "/out/"
SCHEMA_NAME = "/linkedin_schema.json"




files_folder = os.listdir(os.getcwd() + RESOURCES_FOLDER)
stats = getStatsObject()

schema = open(os.path.abspath(os.getcwd() + SCHEMA_NAME)).read()

print schema

#Looping Over each file
for fileName in files_folder:
    try:
        #Getting the files absolute path and Opening them
        filePath = os.path.abspath(os.getcwd() + RESOURCES_FOLDER + fileName)
        file = open(filePath).readlines()

        #Parsing the html with LXML libary
        tree = html.fromstring(file.__str__())

        LOG("parsing " + fileName)

        if (len(tree)==0):
            LOG_ERROR("Couldn't Parse File (file may be corrupted)\t" + fileName)
            continue

        #Evaluating Xpaths to Extract Content
        LOG("Evaluating Xpaths")

        firstName = tree.xpath("//span[contains(@class,'given-name')]//text()")
        firstName = ObjToString(firstName)
        middleName = ""
        if (firstName.__contains__(" ")):
            middleName = firstName.split(" ")[-1]

        lastName = tree.xpath("//span[contains(@class,'family-name')]//text()")
        lastName = ObjToString(lastName)

        # Since the country/state/city couldn't be seperated in a correct way from the pages
        # Using geocoder library to extract them
        locality = tree.xpath("//span[contains(@class,'locality')]/text()")
        locality = cleanLocality("".join(locality))

        g = geocoder.google(locality)

        city = g.city
        if(city):
            city = ''.join(city)
        else:
            city = ""
        state = g.state
        country = g.country


        recomendations = tree.xpath("//dl[contains(@id,'overview')]//dd[not(contains(@class,'over'))]//strong/text()")
        recomendations = ObjToString(recomendations)

        connections = tree.xpath("//dd[contains(@class,'overview')]//strong/text()")
        connections = ObjToString(connections)

        profile_url = tree.xpath("//div[@class='header']//a/@href")
        profile_url = ObjToString(profile_url)

        image_url = tree.xpath("//div[@id='profile-picture']/img/@src")
        image_url = ObjToString(image_url)

        summary = tree.xpath("//p[@class=' description summary']//text()")
        summary = ObjToString(summary)


        specialties = tree.xpath("//a[@class='jellybean']/text()")
        specialties = cleanSpecialties("".join(specialties))


        jobs = tree.xpath("//div[@id='profile-experience']//div[contains(@class,'position')]")

        jobsArr = []
        for div in jobs:
            title = div.xpath(".//span[@class='title']//text()")
            company = div.xpath(".//span[contains(@class,'org summary')]//text()")
            start_date = div.xpath(".//abbr[@class='dtstart']//text()")
            end_date = div.xpath(".//abbr[@class='dtend']//text()")
            description = div.xpath(".//p[contains(@class,'description')]/text()")
            jobObj = createJobObject(title,company,start_date,end_date,description)
            jobsArr.append(jobObj)


        # Creating Object with the extracted values
        jsonObj = {}
        jsonObj["Name"]= {}
        jsonObj["Name"]["First"] = firstName
        jsonObj["Name"]["middle"] = middleName
        jsonObj["Name"]["last"] = lastName
        jsonObj["Location"] = {}
        jsonObj["Location"]["country"] = country
        jsonObj["Location"]["state"] = state
        jsonObj["Location"]["city"] = city
        jsonObj["Recommendations"] = recomendations
        jsonObj["Connections"] = connections
        jsonObj["profile_url"] = profile_url
        jsonObj["image_url"] = image_url
        jsonObj["summary"] = summary
        jsonObj["specialties"] = specialties
        jsonObj["Jobs"] = []
        jsonObj["Jobs"] = jobsArr

        #Parsing to JSON with json library
        json_out = json.loads(json.dumps(jsonObj))


        #Validating against Schema (Normaly we would need to validate if a certain field isn't well formed)
        #jsonschema.validate(json.dumps(json_out),json.loads(schema))

        #Wrting to Disk
        out = open(os.path.abspath(os.getcwd() + OUTPUT_FOLDER + fileName.replace(".html",".json")),"wb")
        out.write(json.dumps(json_out))


        LOG("Writing Json to a file")



        #Writing Statistics
        stats = writeStatistics(json_out,stats)
        LOG("Writing Statistics")

    except Exception as e:
        LOG_ERROR(str(e))
        continue

stats_out = open(os.path.abspath(os.getcwd() + OUTPUT_FOLDER + "Statistics.json"),"wb")
stats_out.write(json.dumps(stats))
LOG("Writing Statistics to Disk ")



