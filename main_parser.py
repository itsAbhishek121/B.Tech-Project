import csv
from ctypes import Array
from types import new_class
from bs4 import BeautifulSoup, NavigableString
import re
import json
# Reading the data inside the xml
# file to a variable under the name
# data
with open('file11.xml', 'r', encoding="utf8") as f:
    data = f.read()

# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object
Bs_data = BeautifulSoup(data, "lxml")

# Extrcting all sections
main_div = Bs_data.find('div', attrs = {'class':"reboot collapse show"})
sections = main_div.find_all('li')
temp = []
for i in range (len(sections)):
    item = sections[i]
    ss = re.findall(">S[0-9]+.*<",str(item.encode("utf-8")))
    if (len(ss) > 0):
        temp.append(ss[0][1:11])
sections = temp
# print(sections)
divvv = Bs_data.find('div', attrs = {'id':"dynamic-xbrl-form"})
all_div = divvv.find_all('div')

all_div.pop(0)
# print(divvv.encode("utf-8"))
new_arr = []
z = 0
for sec in sections:
    for dv in all_div:

        item = str(dv)
        if sec in item:
            try:
                dv_first_sibling = dv.next_element.next_element
            except:
                continue
            while((sec not in str(dv_first_sibling))):
                try:
                    dv_first_sibling = dv_first_sibling.next_sibling.next_sibling
                except:
                    break
            try:
                target_div = dv_first_sibling.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_element.next_sibling.next_sibling.next_element.next_element
            except:
                continue
            useful_text = ""
            arr = []
            while(target_div and not isinstance(target_div, NavigableString)):
                # print(target_div.encode("utf-8"))
                temp_arr = target_div.find_all('table')
                if (len(temp_arr) > 0):
                    arr.append(useful_text)
                    useful_text = ""

                    # table ka h ye
                    rows = target_div.find_all('tr')
                    cols = rows[0].find_all('td')
                    mat = []
                    temp = []
                    for i in range(len(rows)):
                        if (i == 0):
                            for j in rows[i].find_all('td'):
                                tx = ""
                                for k in j.find_all('span'):
                                    tx = tx + " " + k.text
                                temp.append(tx)
                        else:
                            extra = ""
                            for idx, j in enumerate(rows[i].find_all('td')):
                                tx = ""
                                if (idx == 0):  
                                    k = j.find('span')
                                    if (k == None):
                                        continue
                                    tx = tx + " " + k.text
                                    tg = k.find("ix:nonfraction")
                                    if (tg):
                                        tg = tg["name"][3:]
                                    else:
                                        tg = ""
                                        
                                    extra = tx
                                else:
                                    k = j.find('span')
                                    if (k == None):
                                        continue
                                    tx = tx + " " + k.text
                                    tg = k.find("ix:nonfraction")
                                    if (tg):
                                        tg = tg["name"][3:]
                                    else:
                                        tg = ""

                                    obj = {
                                        "row" : extra,
                                        "col" : temp[idx],
                                        "data" : tx,
                                        "tag" : tg
                                    }
                                    mat.append(obj)
                    arr.append(mat)
                elif (target_div):
                    spans = target_div.find_all('span')
                    for sp in spans:
                        useful_text = useful_text + " " + sp.text

                if (target_div and target_div.next_sibling !=None):
                    target_div = target_div.next_sibling.next_sibling
                else:
                    break
            arr.append(useful_text)
            for i in range(len(arr)):
                if (type(arr[i]) == list):
                    if (i > 0 and i < len(arr) - 1):
                        obj = {
                            "Above_txt" : arr[i-1],
                            "Table_data" : arr[i],
                            "Below_txt" : arr[i+1]
                        }
                        new_arr.append(obj)
                    elif (i > 0 and i == len(arr) - 1):
                        obj = {
                            "Above_txt" : arr[i-1],
                            "Table_data" : arr[i],
                            "Below_txt" : ""
                        }
                        new_arr.append(obj)
                    elif (i == 0 and i < len(arr) - 1):
                        obj = {
                            "Above_txt" : "",
                            "Table_data" : arr[i],
                            "Below_txt" : arr[i+1]
                        }
                        new_arr.append(obj)

 

# Writing to sample.json
with open("sample11.json", "w") as outfile:
        # Serializing json
        json_object = json.dumps(new_arr, indent=4)
        outfile.write(json_object)


        
