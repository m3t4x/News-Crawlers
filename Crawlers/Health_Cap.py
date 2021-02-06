import requests,io,xlsxwriter,sys,time,csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd

def out(nm,data):
	wr = pd.DataFrame(data, columns=["Fund Manager Name","Fund Manager Url","Title","Date of Publish","Author","Content","News article page link"])
	wr.to_csv(nm,index = False)

exec_path = "../chromedriver.exe"
save_path = "../csv/Health_Cap.csv"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
#options.add_argument("--headless")
#options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Mobile Safari/537.36}"')
driver = webdriver.Chrome(options=options,executable_path=exec_path)
links = []
for i in range(1,146):
	driver.get("https://www.healthcap.eu/portfolio-companies-news/page/%s/"%i)
	ns = driver.find_element_by_class_name("listning-container")
	lks = ns.find_elements_by_tag_name("a")
	for a in lks[:-1]:
		links.append(a.get_attribute("href"))
data = []
for link in links:
	if ("portfolio-companies-news/page" in link) or ("portfolio-companies-news" in link):
		continue
	driver.get(link)
	time.sleep(0.5)
	try:
		tt = driver.find_element_by_class_name("intro-cta-cta-content").text
	except:
		tt = driver.find_element_by_class_name("entry-title").text
	try:
		date = driver.find_element_by_class_name("intro-date").text
	except:
		date = ""
	try:
		tmp = driver.find_element_by_class_name("markdown-content ")
	except:
		tmp = driver.find_element_by_class_name("entry-content")
	tmp = tmp.find_elements_by_tag_name("p")
	cont = ""
	for i in tmp[1:]:
		cont = cont + i.text
	dats = ["Health Cap","https://www.healthcap.eu",tt,date,"",cont,link]
	data.append(dats)
out(save_path,data)
print("[+] Health_Cap_.csv Saved.")
driver.quit()