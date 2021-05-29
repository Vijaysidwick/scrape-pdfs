# pip install tika
from tika import parser
import re
import csv
import os


# place this file in the pdf folder

print(os.path.dirname(__file__))


all_files_in_folder = os.listdir(os.path.dirname(__file__))
all_pdf_files = list(filter(lambda x:x.endswith('.pdf'),all_files_in_folder))

f = open(os.path.dirname(__file__)+"/invoice.csv",'w',newline='')   # change 'w' to 'a' if you want to append
writer = csv.writer(f,delimiter=',')

input_file = open('input.txt','r')
header = ['PDF Filename']
all_keywords = input_file.readlines()
all_keywords = [each_keyword.replace('\n','').lower() for each_keyword in all_keywords] 
header.extend(all_keywords)

writer.writerow(header)                  # CSV Header
# ^invoice date(.*)
#Reg exp

for each_pdf_file in all_pdf_files:
    data = {}
    print(each_pdf_file)    
    csv_output = [each_pdf_file]
    text = parser.from_file(str(os.path.dirname(__file__)+"/"+each_pdf_file))
    pdf_text = text['content'].lower().replace('number','no')
    print(pdf_text)
    for each_keyword in all_keywords:
        print(r'^'+each_keyword+'(.*)')
        all_ = re.findall(r'^invoice no(.*)',pdf_text)
        print(all_)
    break
    all_lines = list(set(pdf_text.splitlines()))
    for each_keyword in all_keywords:
        if each_keyword in each_line and each_keyword not in data.keys():
            all_words = each_line.split(' ')                                                        # include a try block if u get error here
            if all_words[all_words.index(each_keyword.split(' ')[0])+2].upper() != ":" :
                data[each_keyword] = all_words[all_words.index(each_keyword.split(' ')[0])+2].upper()
            else:
                data[each_keyword] = all_words[all_words.index(each_keyword.split(' ')[0])+3].upper()
    all_headers = [data.get(each_keyword.replace('\n','').lower(),None) for each_keyword in all_keywords]
    all_headers.insert(0,each_pdf_file)
    writer.writerow(all_headers)

f.close()
