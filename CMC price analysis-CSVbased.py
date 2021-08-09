import requests
import csv
from sklearn import tree
opens = list()
closes = list()
dates = list()
m_caps = list()
in_data = list()
out_data = list()

print('COIN MARKETCAP price analysis program \n entered URL must a json file link \n it can be found in \'XNL\' in network of developing tool from your browzer ')
url =input('url: ')  

r = requests.get(url)

pre_file = r.json()

raw_data = pre_file['data']['quotes']

for i in range(len(raw_data)):
    for k, v in raw_data[i]['quote'].items():
        if k == 'open':
            opens.append(str(v))

for i in range(len(raw_data)):
    for k, v in raw_data[i]['quote'].items():
        if k == 'close':
            closes.append(str(v))

for i in range(len(raw_data)):
    for k, v in raw_data[i]['quote'].items():
        if k == 'timestamp':
            dates.append(str(v[0:10]))

for i in range(len(raw_data)):
    for k, v in raw_data[i]['quote'].items():
        if k == 'marketCap':
            m_caps.append(str(v))

with open('data.csv' , 'w' , newline = '\n') as csvfile: #writeing
    writer = csv.reader(csvfile )
    for line in range(len(dates)):
        csvfile.write(dates[line])
        csvfile.write(',')
        csvfile.write(opens[line])
        csvfile.write(',')
        csvfile.write(closes[line])
        csvfile.write(',')
        csvfile.write(m_caps[line])
        csvfile.write('\n')
    csvfile.close()

with open('data.csv' , 'r') as cfile:
    reader = csv.reader(cfile)
    for row in reader:
        in_data.append((row[0:2]))
        out_data.append(row[2:])
    csvfile.close()

x = [[x.replace('-','') for x in l] for l in in_data]
x = [[float(num) for num in sub] for sub in x]
y = [[float(num) for num in sub] for sub in out_data]


clf = tree.DecisionTreeRegressor()
clf = clf.fit(x,y)
what1 = float(input('date (True Format yy-mm-dd): ').replace('-' , ''))
what2 = float(input('open (True Format whithout \'$\' ): '))
print(200*'*')
print(clf.predict( [[what1 , what2]] ))
input('press any KEy to close')


