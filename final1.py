import time
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import os
import re
import requests
import urllib2
import bleach
from final2 import writer

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:/Users/vishal/AppData/Local/Google/Chrome/test")



driver = webdriver.Chrome(executable_path="G:/chromedriver.exe",chrome_options=chrome_options)
driver.get("https://www.quora.com/Rafael-de-Oliveira")

i = 0
for _ in xrange(0, 3):
    driver.execute_script("window.scrollTo(0, 1000000);")
    time.sleep(2)
    i = i + 1
    print i


html_source = driver.page_source
data = html_source.encode('utf-8')

soup = BeautifulSoup(data)
# print soup.get_text()

# for con in soup.find_all(href=re.compile("/answer/")):
# 	print con.get('href').encode('utf-8')
valid_links = []
for link in soup.find_all('a'):
	try:
		answer_link = link.get('href')
		if isinstance(answer_link, basestring):
			# converting unicode to string
			ab = answer_link.encode('utf-8')
			if re.search('answer', ab):
				spill = ab.split('/')
				if len(spill)==4 and not('Vishal-Jain-10' in spill) and not(re.search('snids', spill[3])):
					# print ab
					#truth_value = 'Vishal-Jain-10' in ab.split('/')
					# print truth_value
					#if not(truth_value):
					#print ab
					valid_links.append(answer_link)
		# print ab

	except UnicodeEncodeError:
		print "Error"

# valid_links = list(set(valid_links))
# removing duplicates while preserving order
#driver.get("http://www.quora.com"+valid_links[3])
valid_links = f7(valid_links)

# for link in valid_links:
# 	print link.encode('utf-8')
print "No of links" + str(len(valid_links))


#content = driver.find_element_by_class_name('more_link')
#content.click()
#print content.text
#menu = driver.find_element_by_class_name("more_link")
#hidden_submenu = driver.find_element_by_css_selector(".nav #submenu1")

#ActionChains(driver).click(menu).perform()



 
doc = SimpleDocTemplate("form_letter2.pdf",pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=28)
Story=[]
logo = "quora_logo.png"

 
formatted_time = time.ctime()


 
im = Image(logo, 2*inch, inch)
Story.append(im)
 
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY,fontSize  = 12, leading = 20))

full_name ='<font name=Times-Roman size=14>Rafael de Oliveira</font>'
# full_name = "Vishal Jain"
styles1=getSampleStyleSheet()
styles1.add(ParagraphStyle(name='Justify', alignment=TA_CENTER, fontSize  = 16))  
Story.append(Spacer(1, 25))
Story.append(Paragraph(full_name, styles1["Justify"]))
Story.append(Spacer(1, 12))

ptext = '<font size=12 name=Times-Roman>%s</font>' % formatted_time 
Story.append(Paragraph(ptext, styles1["Justify"]))
Story.append(Spacer(1, 12))


Story.append(Spacer(1, 520))

# styleH = styles['Heading1']

for link in valid_links:
	Story = writer(link, Story, driver)

doc.build(Story)
print "No of links" + str(len(valid_links))