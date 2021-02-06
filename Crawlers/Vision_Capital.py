import requests,io,xlsxwriter,sys,time,csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd

def out(nm,data):
	wr = pd.DataFrame(data, columns=["Fund Manager Name","Fund Manager Url","Title","Date of Publish","Author","Content","News article page link"])
	wr.to_csv(nm,index = False)

exec_path = "../chromedriver.exe"
save_path = "../csv/Vision_Capital_.csv"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
#options.add_argument("--headless")
#options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Mobile Safari/537.36}"')
driver = webdriver.Chrome(options=options,executable_path=exec_path)
lks = ["http://www.visioncapital.com/Media/?year=2017","http://www.visioncapital.com/Media/?year=100"]
links = []
for lk in lks:
	driver.get(lk)	
	tb = driver.find_element_by_class_name("PRTable")
	x = tb.find_elements_by_tag_name("a")
	for a in x:
		links.append(a.get_attribute("href"))
links = list(set(links))
data = []
for link in links:
	driver.get(link)
	time.sleep(0.5)
	tb = driver.find_element_by_class_name("PRTable")
	tt = tb.find_elements_by_tag_name("td")[0].text
	date = tb.find_elements_by_tag_name("td")[1].text
	tmp = driver.find_element_by_class_name("content")
	tmp = tmp.find_elements_by_tag_name("p")
	cont = ""
	for i in tmp:
		cont = cont + i.text
	dats = ["Vision Capital","http://www.visioncapital.com",tt,date,"",cont,link]
	data.append(dats)
out(save_path,data)
print("[+] Vision_Capital_.csv Saved.")
driver.quit()