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

def youtube_url(attrs, new=False):
    """Shorten overly-long URLs in the text."""

    attrs['_text'] = "youtube_url"
    return attrs

def writer(link, Story, driver):
	styles=getSampleStyleSheet()
	styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY,fontSize  = 12, leading = 20))
	
	question = link.split('/')[1]
	question = question.replace('-', ' ')
	question = question + "?"
	print link.encode('utf-8')
	ptext = question.encode('utf-8')
	Story.append(Paragraph(ptext, styles["Heading1"]))
	Story.append(Spacer(1, 18))
	driver.get("http://www.quora.com"+link)

	html_source = driver.page_source
	data = html_source.encode('utf-8')
	soup = BeautifulSoup(data)
	try:
		s = soup.find_all(id=re.compile('container'))[1]
		dump = ""

		for con in s.contents:
		    ab = con.encode('utf-8')
		    if not(re.search('<span>?', ab)) and not(re.search('img', ab)) and not(re.search('<div', ab)):
		        dump = dump + unicode(con).encode('utf-8')

		    elif re.search('youtube', ab):
		        #print con.contents[0]['src']
		        #print type(con['data-embed'])
		        # try:
		        try:
		        	m = re.search('//www.youtube.com/embed/...........', con['data-embed'])
			        if m:
			            found = m.group(0)
			            link_split = found.split('/')
			            url = "https://www.youtube.com/watch?v=" + link_split[4] 
			            youtube_link = bleach.linkify(url, callbacks=[youtube_url,])
			            # print type(you
			            a = youtube_link.split(">")[0] + ' color="blue"'
			            o_links = a + ">" + youtube_link.split(">")[1] + ">"
			            dump = dump + o_links.encode('utf-8')

		        except KeyError:
		        	pass

		        # m = re.search('//www.youtube.com/embed/...........', con['data-embed'])
		        # if m:
		        #     found = m.group(0)
		        #     link_split = found.split('/')
		        #     url = "https://www.youtube.com/watch?v=" + link_split[4] 
		        #     youtube_link = bleach.linkify(url, callbacks=[youtube_url,])
		        #     # print type(you
		        #     a = youtube_link.split(">")[0] + ' color="blue"'
		        #     o_links = a + ">" + youtube_link.split(">")[1] + ">"
		        #     dump = dump + o_links.encode('utf-8')



				# try:

				# except:




		    elif re.search('img', ab):
		        ptext = dump
		        Story.append(Paragraph(ptext, styles["Justify"]))
		        Story.append(Spacer(1, 12))

		        dump = ""
		        try:
			        src = con.contents[0]['src']
			        print type(src)
			        r = urllib2.urlopen(src.encode('utf-8'))
			        identity = src.split('/')[3]
			        iden = identity.split('?')[0]
			        f = open('img/'+iden+'.jpeg', 'wb')
			        f.write(r.read())
			        f.close()
			        im = Image('img/'+iden+'.jpeg', 400, 300)
			        Story.append(im)
		        except KeyError:
		        	pass
		        except TypeError:
		        	pass
		    elif re.search('href', ab):
		    	if not(re.search('</?i>',ab)) and not(re.search('</?b>',ab)) and not(re.search('</?u>',ab)):
			    	try:
				        po = con.contents[0]['href']
				        jo = po.split('/')
				        if re.search('^/', po):
				            o_links = "http://www.quora.com"+po
				            dump = dump + o_links.encode('utf-8')
				        else:
				            # other_links = bleach.clean(str(con),strip=True)
				            # dump = dump + other_links
				            other_links = bleach.clean(str(con),strip=True)
				            a = other_links.split(">")[0] + ' color="blue"'
				            print a
				            o_links = a + ">" + other_links.split(">")[1] + ">"
				            dump = dump + o_links.encode('utf-8')

			    	except KeyError:
			    		pass
			    	except TypeError:
		        		pass


		        # tag = con.contents[0]
		        # p = tag.attrs
		        
		        # print con.contents[0]['href']
		        # url = con.contents[0]['href']


		ptext = dump           		
		Story.append(Paragraph(ptext, styles["Justify"]))
		Story.append(Spacer(1, 12))
	except IndexError:
		pass

	return Story


