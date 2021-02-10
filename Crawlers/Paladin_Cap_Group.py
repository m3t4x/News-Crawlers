import requests,io,xlsxwriter,sys,time,csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd

def out(nm,data):
	wr = pd.DataFrame(data, columns=["Fund Manager Name","Fund Manager Url","Title","Date of Publish","Author","Content","News article page link"])
	wr.to_csv(nm,index = False)

exec_path = "../chromedriver.exe"
save_path = "../csv/Paladin_Cap_Group.csv"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
#options.add_argument("--headless")
#options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Mobile Safari/537.36}"')
driver = webdriver.Chrome(options=options,executable_path=exec_path)
links = []
for i in range(1,19):
	driver.get("https://www.paladincapgroup.com/news/page/%s/"%i)
	qr = driver.find_element_by_class_name("et_pb_ajax_pagination_container")
	ars = qr.find_elements_by_tag_name("article")
	#print(len(ars))
	for a in ars:
		ll = a.find_element_by_tag_name("a").get_attribute("href")
		links.append(ll)
data = []
for link in links:
	driver.get(link)
	tt = driver.find_element_by_class_name("entry-title").text
	date = driver.find_element_by_class_name("published").text
	qr = driver.find_element_by_class_name("entry-content")
	tmp = qr.find_elements_by_tag_name("p")
	cont = ""
	for i in tmp:
		cont = cont + i.text
	dats = ["PaladinCapGroup","https://www.paladincapgroup.com/",tt,date,"",cont,link]
	data.append(dats)
out(save_path,data)
print("[+] Paladin_Cap_Group.csv Saved.")
driver.quit()