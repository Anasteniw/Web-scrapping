import requests
from bs4 import BeautifulSoup
from pprint import pprint
from fake_headers import Headers
import json


HOST = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
headers = Headers(browser="Microsoft Edge", os = "win").generate()

hh_search_html = requests.get(HOST, headers = headers).text
soup = BeautifulSoup(hh_search_html, features="lxml")
vac_list = soup.find_all(class_="serp-item")


skills = ["Django", "Flask"]

result =[]
for vac in vac_list:
    link=vac.find("a", class_="serp-item__title")["href"]
    salary =vac.find("span", {"data-qa":"vacancy-serp__vacancy-compensation"})
    company = vac.find ("div", class_="vacancy-serp-item__meta-info-company").text
    city = vac.find("div", {"data-qa":"vacancy-serp__vacancy-address"}).text
    skills_text = vac.find("div", class_="g-user-content").text

    
    if any ([skills_word in skills_text for skills_word in skills]) and salary != None:
        result.append({
        "Link":link,
        "Salary":salary.text,
        "Company":company,
        "City":city
        })
        
with open("vacansy_list.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=3)
  