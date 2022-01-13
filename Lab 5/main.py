#Парсинг сайта herzen.spb.ru
from urllib.request import urlopen #Преобразуем страницу в HTML
from bs4 import BeautifulSoup
import re

html = urlopen('https://www.herzen.spb.ru/main/structure/inst/') #Преобразуем страницу в HTML файл
bs = BeautifulSoup(html, "html.parser") #Преобразование кода для библиотеки BS
nameList = bs.find('td',{'class':'block'}).children #Ищем тег td класса блок и всё что внутри
l = re.compile("/inst/.") #Маска для регулярных выражений
nameList = bs.findAll('a',{'class':'', 'href':l}) #Найти все теги а с ссылкой по маске l


data = [] #Список институтов
key = True
firstName = ''
for name in nameList: #Цикл который добавляет все нужные данные в переменную data
    uni = name.get_text()
    if uni == firstName:
      break
    if key:
      firstName = name.get_text()
    key = False
    obj = {'institute_name':uni, 'url':'https://www.herzen.spb.ru' + name.get('href')} #
    data.append(obj)

print(data)

html = urlopen('https://atlas.herzen.spb.ru/faculty.php')
bs = BeautifulSoup(html, "html.parser")
nameList = bs.findAll('a',{'class':'alist'}) #Ищем теперь с нужным классом alist
data2 = [] #Список кафедр
flag = False
for e in nameList:
  name = e.get_text()
  if e.get('href') == "faculty.php":
    name = name.split(' ')
    reg = re.compile(name[1])
    #print(reg)
    for el in data:
      if re.search(reg, el['institute_name']):
        if flag:
          #print(inst)
          inst.update({"list_of_deps": data2})
        data2 = []
        flag = True
        inst = el
  else:
    if re.search("кафедра", name):
      url = "https://atlas.herzen.spb.ru/" + e.get('href')
      dep = BeautifulSoup(urlopen(url), "html.parser")
      reg = re.compile("teacher")
      head = dep.find('a',{'href':reg})
      if head:
        head_name = head.get_text()
        head_name = re.sub('^\s+', '',head_name)
        head_url = "https://atlas.herzen.spb.ru/" + head.get('href')
        head_bs = BeautifulSoup(urlopen(head_url), "html.parser")
        mail = head_bs.find('a', {'href':re.compile('@')})
      data2.append({"dep_name":name, "head_name":head_name.replace("\n", ""), "email":mail.get('href')}) #Добавляем информацию парсинга в список
print(data2)

import json
with open('data.json', 'w', encoding="utf16") as f: #Запись в json
    json.dump(data, f, ensure_ascii=False, indent=4)