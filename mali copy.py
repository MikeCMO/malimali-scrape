import requests
r = requests.get("http://www.malimalihome.net/residential?status=1&region1=3&region2=39&price=0&price_b=700&price_e=880")
#print(r.text)
holy = 0
import pymongo 
client = pymongo.MongoClient('localhost', 27017)
database = client["mali"]
mongoCol = database["ha"]

from bs4 import BeautifulSoup

soup = BeautifulSoup(r.text,'html.parser')
#print(soup.prettify())
#print(soup.a)
house = soup.find_all('div', class_='result-list')
#house2 = house.find('div',style_='float:right')
#house3 = house2.find('div',class_='result-list-c')
houseDict = {}
for x in house:
    
    building_name = x.find_all('div', class_='result-list-c-title')
    for y in building_name:
        finallyName = y.find('a')
        houseDict["building name"] = finallyName.text
    
    building_size = x.find_all('div',class_='result-list-c-type')
    for y in building_size:
        counter = 0
        houseType = 0
        bs= y.find_all('b')
        for z in bs:
            counter+=1
            #print(z)
        #print(counter)
        if counter == 2:
            miniCounter = 0
            for each in bs:
                if miniCounter ==0:
                    print(each.text,'呎')
                    miniCounter+=1
                elif miniCounter ==1:
                    print('更新日期 :',each.text)
        elif counter ==3:
            miniCounter = 0
            for each in bs:
                if miniCounter ==0:
                    print(each.text,'房')
                    miniCounter+=1
                elif miniCounter ==1:
                    print(each.text,'呎')
                    miniCounter+=1
                else:
                    print('更新日期 :',each.text)
        elif counter ==4:
            miniCounter = 0
            for each in bs:
                if miniCounter ==0:
                    print(each.text,'房')
                    miniCounter+=1
                elif miniCounter ==1:
                    print(each.text,'厅')
                    miniCounter+=1
                elif miniCounter ==2:
                    print(each.text,'呎')
                    miniCounter+=1
                else:
                    print('更新日期 :',each.text)
        #print('\n')
    
    building_price = x.find('div',class_='result-list-r-price red')
    if building_price == None:
        continue
    print(building_price.contents[0].strip(),'万')
    
    building_description = x.find('div',class_='result-list-c-desc')
    print(building_description.text,'\n')

    #contact number is found by get method, find the id for each post and save it to variable
    #then put it in the changing link for phone number
    contact_number = x.find('div',class_='list-cover')
    contactA = contact_number.find('a')
    contactLink = contactA.get('href')
    houseID = []
    for letters in contactLink.split('/'):
        if letters.isdigit():       
            houseID.append(letters)
    iceD = houseID[0]
    ogLink= 'http://www.malimalihome.net/api/v2/prop-contact?prop_id=&full_contact=1'
    newLink= ogLink[:56] + iceD + ogLink[56:]
    
    import re
    n = requests.get(newLink)
    badPhone = n.text
    badPhone = re.findall('[0-9]{8}',badPhone)
    for each in badPhone:
        print(each)
    print(holy,'shit')
    holy+=1


    
    
    
        
            





    
        
        




        
    


