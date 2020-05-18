import mysql.connector
fiveHead = mysql.connector.connect(
  host="localhost",
  user="root",
  password="poggers",
  database = 'PogU'
  
)
cursor = fiveHead.cursor()
updateQ = "SELECT * FROM Houses_Page_2 WHERE buildingID = '4202018'"
d = cursor.execute(updateQ)
b = cursor.fetchone()
if b == None:
    print('smoking')
else:
    print('sasdasd')
