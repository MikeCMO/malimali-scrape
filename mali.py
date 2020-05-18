import requests
#originalLink = 'http://www.malimalihome.net/residential?status=1&region1=3&region2=39&price=0&price_b=700&price_e=880'
originalLink = 'http://www.malimalihome.net/residential?status=1&region1=3&region2=10&price=0&price_b=700&price_e=880&prepage=20&keywords=%E5%90%9B%E8%96%88&page=1'
originalPage = True

link = originalLink
linkList = [originalLink]

def getHouses(link):
    print(link)
    r = requests.get(link)
    #print(r.text)

    import pymongo 
    client = pymongo.MongoClient('localhost', 27017)
    database = client["mali"]
    mongoCol = database["ha"]

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(r.text,'html.parser')

    house = soup.find_all('div', class_='result-list')

    houseDict = {}
    update = False
    for x in house:
        if x.find('div',class_='result-list-l')==None:
            continue
        #find website unique id for website
        contact_number = x.find('div',class_='list-cover')
        contactA = contact_number.find('a')
        contactLink = contactA.get('href')
        houseID = []
        for letters in contactLink.split('/'):
            if letters.isdigit():       
                houseID.append(letters)
        iceD = houseID[0]
        houseDict["Website House ID"] = iceD
        if mongoCol.find_one({"Website House ID":iceD})!=None:
            update = True

        if update ==False:
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
                            houseDict['呎'] = each.text
                            miniCounter+=1
                        elif miniCounter ==1:
                            houseDict["更新日期"] = each.text
                elif counter ==3:
                    miniCounter = 0
                    for each in bs:
                        if miniCounter ==0:
                            houseDict["房"] = each.text
                            miniCounter+=1
                        elif miniCounter ==1:
                            houseDict['呎'] = each.text
                            miniCounter+=1
                        else:
                            houseDict["更新日期"] = each.text
                elif counter ==4:
                    miniCounter = 0
                    for each in bs:
                        if miniCounter ==0:
                            houseDict["房"] = each.text
                            miniCounter+=1
                        elif miniCounter ==1:
                            houseDict["厅"] = each.text
                            miniCounter+=1
                        elif miniCounter ==2:
                            houseDict['呎'] = each.text
                            miniCounter+=1
                        else:
                            houseDict["更新日期"] = each.text
                #print('\n')
            
            building_price = x.find('div',class_='result-list-r-price red')
            if building_price == None:
                continue
            houseDict["万"] = building_price.contents[0].strip()
            
            building_description = x.find('div',class_='result-list-c-desc')
            houseDict["building description"] = building_description.text

            #contact number is found by get method, find the id for each post and save it to variable
            #then put it in the changing link for phone number
            ogLink= 'http://www.malimalihome.net/api/v2/prop-contact?prop_id=&full_contact=1'
            newLink= ogLink[:56] + iceD + ogLink[56:]
            
            import re
            n = requests.get(newLink)
            badPhone = n.text
            badPhone = re.findall('[0-9]{8}',badPhone)
            bbbtemp = 1
            for each in badPhone:
                houseDict["phone number "+str(bbbtemp)] = each
                bbbtemp+=1
            mongoCol.insert_one(houseDict)
            #print(houseDict)
        
        else:
            building_name = x.find_all('div', class_='result-list-c-title')
            for y in building_name:
                finallyName = y.find('a')
                mongoCol.update({"Website House ID":iceD},{"$set":{"building name":finallyName.text}})
                
            
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
                            mongoCol.update({"Website House ID":iceD},{"$set":{'呎':each.text}})
                            miniCounter+=1
                        elif miniCounter ==1:
                            mongoCol.update({"Website House ID":iceD},{"$set":{'更新日期':each.text}})
                elif counter ==3:
                    miniCounter = 0
                    for each in bs:
                        if miniCounter ==0:
                            mongoCol.update({"Website House ID":iceD},{"$set":{'房':each.text}})
                            miniCounter+=1
                        elif miniCounter ==1:
                            mongoCol.update({"Website House ID":iceD},{"$set":{'呎':each.text}})
                            miniCounter+=1
                        else:
                            mongoCol.update({"Website House ID":iceD},{"$set":{'更新日期':each.text}})
                elif counter ==4:
                    miniCounter = 0
                    for each in bs:
                        if miniCounter ==0:
                            mongoCol.update({"Website House ID":iceD},{"$set":{'房':each.text}})
                            miniCounter+=1
                        elif miniCounter ==1:
                            mongoCol.update({"Website House ID":iceD},{"$set":{'厅':each.text}})
                            miniCounter+=1
                        elif miniCounter ==2:
                            mongoCol.update({"Website House ID":iceD},{"$set":{'呎':each.text}})
                            miniCounter+=1
                        else:
                            mongoCol.update({"Website House ID":iceD},{"$set":{'更新日期':each.text}})
                #print('\n')
            
            building_price = x.find('div',class_='result-list-r-price red')
            if building_price == None:
                continue
            mongoCol.update({"Website House ID":iceD},{"$set":{'万':building_price.contents[0].strip()}})
            
            
            building_description = x.find('div',class_='result-list-c-desc')
            houseDict["building description"] = building_description.text
            mongoCol.update({"Website House ID":iceD},{"$set":{'building description':building_description.text}})
            

            #contact number is found by get method, find the id for each post and save it to variable
            #then put it in the changing link for phone number
            ogLink= 'http://www.malimalihome.net/api/v2/prop-contact?prop_id=&full_contact=1'
            newLink= ogLink[:56] + iceD + ogLink[56:]
            
            import re
            n = requests.get(newLink)
            badPhone = n.text
            badPhone = re.findall('[0-9]{8}',badPhone)
            bbbtemp = 1
            for each in badPhone:
                houseDict["phone number "+str(bbbtemp)] = each
                mongoCol.update({"Website House ID":iceD},{"$set":{"phone number "+str(bbbtemp):each}})
                bbbtemp+=1
        
        houseDict = {}
        update = False
    
    link = soup.find('ul',class_='pagination')
    link2 = link.find_all('li')

    theLink = link2[-1].find('a')
    if theLink ==None:
        originalPage= False
        exit()
        
    actualLink = theLink.get('href')
    for e in linkList:
        if e == actualLink:
            break
        
        else:
            linkList.append(actualLink)
        
    
while originalPage==True:
    getHouses(linkList[-1])

        





            
            
            
                
                    





            
                
            




        
    


