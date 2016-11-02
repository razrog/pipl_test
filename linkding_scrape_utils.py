import datetime,sys




#Creating Statistics Object and Initializing it
def getStatsObject():
    Statistics = {}
    Statistics["Number_Of_Pages_Extracted"] = 0
    Statistics["Name"] = {}
    Statistics["Name"]["First"] = 0
    Statistics["Name"]["middle"] = 0
    Statistics["Name"]["last"] = 0
    Statistics["Location"] = {}
    Statistics["Location"]["country"] = 0
    Statistics["Location"]["state"] = 0
    Statistics["Location"]["city"] = 0
    Statistics["Recommendations"] = 0
    Statistics["Connections"] = 0
    Statistics["profile_url"] = 0
    Statistics["image_url"] = 0
    Statistics["summary"] = 0
    Statistics["specialties"] = 0
    Statistics["Jobs"] = {}
    Statistics["Jobs"]["title"] = 0
    Statistics["Jobs"]["company"] = 0
    Statistics["Jobs"]["start_date"] = 0
    Statistics["Jobs"]["end_date"] = 0
    Statistics["Jobs"]["description"] = 0
    return Statistics



#Prints STATUS/ERROR messages
def LOG(message):
    INFO = '[' + datetime.datetime.now().time().__str__() + ']\t[STATUS]\t'
    print INFO + message
def LOG_ERROR(message):
    ERROR = '[' + datetime.datetime.now().time().__str__() + ']\t[ERROR]\t'
    print ERROR + message


#Do to the parser we need to clean the returned output
def ObjToString(obj):
    str = "".join(obj)
    str = str.replace("\\r", "")
    str = str.replace("\\n", "")
    str = str.replace("\\t", "")
    return str

#Do to the parser we need to clean the returned output
def cleanLocality(st):
    st = st.replace("'", "")
    st = st.replace("\\n", "")
    st = st.replace("\\r", "")
    st = st.replace("\\t", "")

    f_index = ""
    l_index = ""
    for c in st:
        if (c.isalpha()):
            f_index = st.index(c)
            break
    for c in st:
        if (c.isalpha()):
            l_index = st.rindex(c)
        else:
            continue
    return st[f_index:l_index + 1]

#Do to the parser we need to clean the returned output
def cleanSpecialties(st):
    out = ""
    for value in st:
        value = value.replace("\\r", "")
        value = value.replace("\\n", "")
        value = value.replace("'", "")
        value = value.replace(",", "")
        value = value.strip()
        if (len(value) != 0):
            out += value + ","
    return out[:-1]

#Creating job Object from given values
def createJobObject(title, company, start_date, end_date,description):
    obj = {}
    obj["title"] = ObjToString(title)
    obj["company"] = ObjToString(company)
    obj["start_date"] = ObjToString(start_date)
    obj["end_date"] = ObjToString(end_date)
    obj["description"] = ObjToString(description)
    return obj


#Check JSON values and updates the statistics accordinally
def writeStatistics(json_out,stats):
    stats["Number_Of_Pages_Extracted"] += 1

    if (json_out["Name"]["First"]):
        stats["Name"]["First"] += 1
    if (json_out["Name"]["middle"]):
        stats["Name"]["middle"] += 1
    if (json_out["Name"]["last"]):
        stats["Name"]["last"] += 1
    if (json_out["Location"]["country"]):
        stats["Location"]["country"] += 1
    if (json_out["Location"]["state"]):
        stats["Location"]["state"] += 1
    if (json_out["Location"]["city"]):
        stats["Location"]["city"] += 1
    if (json_out["Recommendations"]):
        stats["Recommendations"] += 1
    if (json_out["Connections"]):
        stats["Connections"] += 1
    if (json_out["profile_url"]):
        stats["profile_url"] += 1
    if (json_out["image_url"]):
        stats["image_url"] += 1
    if (json_out["summary"]):
        stats["summary"] += 1
    if (json_out["specialties"]):
        stats["specialties"] += 1
    if (json_out["Jobs"]):
        for job in json_out["Jobs"]:
            if (job["title"]):
                stats["Jobs"]["title"] += 1
            if (job["company"]):
                stats["Jobs"]["company"] += 1
            if (job["start_date"]):
                stats["Jobs"]["start_date"] += 1
            if (job["end_date"]):
                stats["Jobs"]["end_date"] += 1
            if (job["description"]):
                stats["Jobs"]["description"] += 1
    return stats