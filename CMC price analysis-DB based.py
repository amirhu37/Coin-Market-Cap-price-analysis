import requests
import mysql.connector
from sklearn import tree
#PHASE 0 
dates = list()
opens = list()
closes = list()
m_caps = list()
in_data = list()
out_data = list()

print('''COIN MARKETCAP price analysis program.
entered URL must a json file link.
it can be found in 'XNL' in network of developing tool from your browzer ''')

url =input('url: ') 

r = requests.get(url)
pre_file = r.json()

raw_data = pre_file['data']['quotes']

#PHASE 1 Find DATAS

for i in range(len(raw_data)): #date
    for k, v in raw_data[i]['quote']['USD'].items():
        if k == 'timestamp':
            dates.append(v[0:10])

for i in range(len(raw_data)): #open
    for k, v in raw_data[i]['quote']['USD'].items():
        if k == 'open':
            opens.append(v)

for i in range(len(raw_data)): #open
    for k, v in raw_data[i]['quote']['USD'].items():
        if k == 'close':
            closes.append(v)

for i in range(len(raw_data)): #market_cap
    for k, v in raw_data[i]['quote']['USD'].items():
        if k == 'market_cap':
            m_caps.append(v)

#PHASE 2 Connect to DB
cnx = mysql.connector.connect(user=input('DB user: '), password= input('pasword: ') ,
                              host=input('host: ') ,
                              database= input('database: ') )
cursor = cnx.cursor()

query = ('INSERT INTO info(date , open , close , market_cap) VALUES(%s,%s,%s,%s)')

for i in range(len(dates)):
    cursor.execute(query , (dates[i] , opens[i], closes[i] , m_caps[i] ) )

#PHASE 3 READ data FROM DB
cursor.execute("SELECT date,open FROM info")
res = cursor.fetchall()

for x in res: 
  in_data.append(x)

cursor.execute('SELECT close, market_cap FROM info')
res = cursor.fetchall()

for x in res: 
    out_data.append(x)

cnx.commit()
cursor.close()
cnx.close()


#PHASE 4 READY TO USE MACHINE LEARNING
x = [[x.replace('-','') for x in l] for l in in_data]
x = [[float(num) for num in sub] for sub in x]
y = [[float(num) for num in sub] for sub in out_data]

clf = tree.DecisionTreeRegressor()
clf = clf.fit(x,y)
what1 = float(input('date (Correct Format yy-mm-dd): ').replace('-' , ''))
what2 = float(input('open (Correct Format whithout \'$\' ): '))
print(200*'*')
print(clf.predict( [[what1 , what2]] ))



#ALTER USER 'root'@'localhost' IDENTIFIED BY '';
# DELETE FROM info;
#  2021-05-09     0.1431
#https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id=1958&convert=USD&time_start=1588878964&time_end=1620414964