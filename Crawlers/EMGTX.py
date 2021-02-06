import requests,io,xlsxwriter,sys,time,csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd

def out(nm,data):
	wr = pd.DataFrame(data, columns=["Fund Manager Name","Fund Manager Url","Title","Date of Publish","Author","Content","News article page link"])
	wr.to_csv(nm,index = False)

exec_path = "../chromedriver.exe"
save_path = "../csv/EMGTX.csv"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
#options.add_argument("--headless")
#options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Mobile Safari/537.36}"')
driver = webdriver.Chrome(options=options,executable_path=exec_path)
lks = []
for i in range(1,11):
	lks.append("https://emgtx.com/news/?lcp_page1=%s#lcp_instance_1"%i)
links = []
for lk in lks:
	driver.get(lk)
	time.sleep(1)
	qr = driver.find_elements_by_class_name("news_list_title")
	for a in qr:
		links.append(a.get_attribute("href"))
data = []
for link in links:
	driver.get(link)
	time.sleep(0.5)
	tt = driver.find_element_by_tag_name("h1").text
	date = driver.find_element_by_class_name("day").text
	date = date + " " + driver.find_element_by_class_name("month").text
	tmp = driver.find_elements_by_tag_name("p")
	cont = ""
	for i in tmp[:-3]:
		cont = cont + i.text
	dats = ["EMGTX","https://emgtx.com",tt,date,"",cont,link]
	data.append(dats)
out(save_path,data)
print("[+] EMGTX.csv Saved.")
driver.quit()