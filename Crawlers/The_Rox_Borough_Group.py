import requests,io,xlsxwriter,sys,time,csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd

def out(nm,data):
	wr = pd.DataFrame(data, columns=["Fund Manager Name","Fund Manager Url","Title","Date of Publish","Author","Content","News article page link"])
	wr.to_csv(nm,index = False)

exec_path = "../chromedriver.exe"
save_path = "../csv/The_Rox_Borough_Group.csv"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
#options.add_argument("--headless")
#options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Mobile Safari/537.36}"')
driver = webdriver.Chrome(options=options,executable_path=exec_path)
links = []
for i in range(1,7):
	driver.get("https://www.theroxboroughgroup.com/news/page/%s/"%i)
	cc = driver.find_element_by_id("content")
	xs = cc.find_elements_by_class_name("post-title")
	for x in xs:
		links.append(x.find_element_by_tag_name("a").get_attribute("href"))
data = []
for link in links:
	driver.get(link)
	time.sleep(0.5)
	tt = driver.find_element_by_class_name("post-title").find_element_by_tag_name("h1").text
	try:
		auth = driver.find_element_by_id("oAuthor").find_element_by_tag_name("strong").text
	except:
		auth = ""
	try:
		date = driver.find_element_by_id("oArticleDate").text
	except:
		date = driver.find_element_by_class_name("post-excerpt").find_elements_by_tag_name("strong")[1].text
		date = date.replace("(","").replace(")","")
		if "About" in date:
			date = ""
	cont = driver.find_element_by_class_name("post-excerpt").text
	dats = ["The Rox Borough Group","https://www.healthcap.eu",tt,date,auth,cont,link]
	data.append(dats)
out(save_path,data)
print("[+] The_Rox_Borough_Group_.csv Saved.")
driver.quit()