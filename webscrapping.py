###############################Web scrapping######################
from bs4 import BeautifulSoup
import requests
import re
import csv
hreftextvalue = 'https://ref.mometrix.com/ref.php'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

def csvreader():
    examsampleproductids = []

    #item = 'https://www.examsample.com/armed-services-test-preparpation'
    with open('examsampleurl.csv', 'r') as examsampleread:

             for row in examsampleread:
                 array = row.split(',')
                 examsampleurl = array[1]
                 examsampleurl = examsampleurl.strip('\n')
                 source = requests.get(examsampleurl, headers=headers).text
                 soup = BeautifulSoup(source, 'lxml')
                 anchorvalue = soup.find_all('a', href=True)
                 for anchortext in anchorvalue:
                     if re.search(hreftextvalue, anchortext['href']):
                         temp = anchortext['href']
                         code = re.search("tid1=([0-9a-zA-Z]+)&?", temp).group(1)
                         print('Title:' + '  ' + array[0] + '   ' + 'Examsample-url' + '  ' + examsampleurl + '   ' + 'Description' + '  '+ anchortext.text + 'Product-id' + '  ' + code)
                         examsampleproductids.append((array[0],examsampleurl,anchortext.text, code))


    return examsampleproductids
csvreader()
examsamapleproductvalues = csvreader()

def csvwriter():
    with open('examsampleurl1.csv', 'w+', newline='') as examsamplewrite:
        fieldnames = ['Title', 'Examsample-url', 'Description', 'Product-id']
        writer = csv.DictWriter(examsamplewrite, fieldnames=fieldnames)
        writer.writeheader()
        for items in examsamapleproductvalues:
            print ('Title:' +'  '+ items[0] +'   '+ 'Examsample-url' + '  ' + items[1] +  '   ' +'Description' + '  '+ 'Product-id'+ '  ' +items[2])
            writer.writerow({'Title': items[0], 'Examsample-url': items[1], 'Description':items[2], 'Product-id': items[3]})

csvwriter()

