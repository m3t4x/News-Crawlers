import requests,io,xlsxwriter,sys,time,csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd

def out(nm,data):
	wr = pd.DataFrame(data, columns=["Fund Manager Name","Fund Manager Url","Title","Date of Publish","Author","Content","News article page link"])
	wr.to_csv(nm,index = False)

exec_path = "../chromedriver.exe"
save_path = "../csv/Wind_Rose.csv"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
#options.add_argument("--headless")
#options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Mobile Safari/537.36}"')
driver = webdriver.Chrome(options=options,executable_path=exec_path)
lks = []
for i in range(2007,2021):
	lks.append("https://www.windrose.com/%s/?post_type=news"%i)
links = []
for lk in lks:
	driver.get(lk)
	time.sleep(1)
	to = driver.find_element_by_id("primary")
	tb = to.find_elements_by_class_name("row")
	for a in tb:
		tmp = a.find_element_by_class_name("post-title")
		links.append(tmp.find_element_by_tag_name("a").get_attribute("href"))
data = []
for link in links:
	driver.get(link)
	time.sleep(0.5)
	tt = driver.find_element_by_class_name("post-title").text
	date = driver.find_element_by_class_name("posted-on").text
	tmp = driver.find_element_by_class_name("shapely-content")
	tmp = tmp.find_elements_by_tag_name("p")
	cont = ""
	for i in tmp:
		cont = cont + i.text
	dats = ["Wind Rose","https://www.windrose.com",tt,date,"",cont,link]
	data.append(dats)
out(save_path,data)
print("[+] Wind_Rose_.csv Saved.")
driver.quit()