###############################Web scrapping######################
from bs4 import BeautifulSoup
import requests
import re
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}
##########################################
def csvreader():
    examsampleproductids = []
    print('##################################################################################################################################################################')
    print ('                                        Read Me                                                                       ')
    print('##################################################################################################################################################################')
    print ('Examsample site scrub: Readfile for this program is  examsampleurl.csv(Created by manual sql query from examsample database. Future release this will be automated.')
    print('Mometrix site scrub , Readfile for this program is  mometrixCatalog.csv. this created by program pdffileread.py. The program generates a unique list of records.')
    print('Input file "mometrixCatalog.csv" has duplicate values because they are manually added. Future automatic cleaning of this record is proposed.')
    print('PDF links in mometrixCatalog.csv have to be scrubbed manually and also then created unique urls. future release of the program we will automate that as well.')
    print ('Input and output should be global parameters future enhancment.')
    print ('Future enhancement to convert these files in to pipe delimited output only, till that point please make sure you split based on comma and see if the value coming is right or not.')
    print('##################################################################################################################################################################\n\n\n')


    csvreaderfile = input('Get the file name')
    csvscrubportal = input('Get the scrub portal name Currently configured only for Examsample and Mometrix')
    if csvscrubportal.upper() == 'EXAMSAMPLE':
        hreftextvalue = 'https://ref.mometrix.com/ref.php'
        print(hreftextvalue)
    elif csvscrubportal.upper() == 'MOMETRIX':
        hreftextvalue = 'https://store.mometrix.com/cart/add?'
        print(hreftextvalue)
    else:
        print('this is not right value')
        quit()
   #item = 'https://www.examsample.com/armed-services-test-preparpation'

    with open(csvreaderfile, 'r') as examsampleread:
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
                    if csvscrubportal.upper() == 'EXAMSAMPLE':
                        code = re.search("tid1=([0-9a-zA-Z]+)&?", temp).group(1)

                    elif csvscrubportal.upper() == 'MOMETRIX':
                        code = re.search("id\[\]=([0-9a-zA-Z]+)&?", temp).group(1)

                    print('Title:' + '  ' + array[0] + '   ' + 'Examsample-url' + '  ' + examsampleurl + '   ' + 'Description' + '  '+ anchortext.text + 'Product-id' + '  ' + code)
                    examsampleproductids.append((array[0],examsampleurl,anchortext.text, code))
    return examsampleproductids



def csvwriter():
    ### future enhancement to project when we take out input file we should have call this function and append by date
    ## if selected examsample please add examsample file if selected mometrix please add mometrix file
       with open('examsamplerecordretriver11-27-2020.csv', 'w+', newline='') as examsamplewrite:
        fieldnames = ['Title', 'Examsample-url', 'Description', 'Product-id']
        writer = csv.DictWriter(examsamplewrite, fieldnames=fieldnames)
        writer.writeheader()
        for items in examsamapleproductvalues:
            print ('Title:' +'  '+ items[0] +'   '+ 'Examsample-url' + '  ' + items[1] +  '   ' +'Description' + '  '+ 'Product-id'+ '  ' +items[2])
            writer.writerow({'Title': items[0], 'Examsample-url': items[1], 'Description':items[2], 'Product-id': items[3]})



#examsamapleproductvalues = csvreader()
#csvwriter()
#####################################################################################################################
#######Uncomment the below line post mometrix url is scrubbed. to clean it manually. This code will removed when pipedelimited is installed.

def cleancsvfunction():
    entries = []
    dup_entries =[]
    #with open('mometrixrecordretriver11-26-2020.csv', 'r') as examsampleread:
    with open('examsamplerecordretriver11-10-2020.csv', 'r') as examsampleread:
        i=0
        for row in examsampleread:
            array = row.split(',')
            try:
                examsamplecode = array[3]
                if len(examsamplecode) != 15:
                    print('Remove comma Manually\n' + row)
                elif array[2] == 'Buy Now':
                    print('Validate it with next row\n'+ row)

                else:
                    productid = array[3]
                    if productid not in entries:
                        entries.append(productid)
                        i = i + 1
                    else:
                        dup_entries.append(productid)
                        if (len(array[2])) == 1 and array[3] in dup_entries:
                            print('Duplicate entries\n', row)


            except IndexError:
                print ('#############################################################################################################')
                print('Structure not proper. Please check the row \n' + row)
                print ('#############################################################################################################')


        print(i)
        print (dup_entries)

cleancsvfunction()
#######################################################################################################################
