# Extract protection levevls for each permission from website

from bs4 import BeautifulSoup as BS
import urllib2

response = urllib2.urlopen("http://developer.android.com/reference/android/Manifest.permission.html")
soup = BS(response.read())
current_apilevel = 0
for current_apilevel in range(100) :
	ex_data = soup.find_all("div", class_="jd-details api apilevel-"+str(current_apilevel))

	for d in ex_data:
		para = d.find_all('p')
		protection_level = None
		for el in para:
			if el:
				data = el.string
				if data:
					if data.find("Protection") != -1 :
						protection_level = data.split(' ')[-1]
						break
		span = d.find_all('span')
		perm = None
		for el in span:
			data = el.string
			if data:
				if data.find("permission.") != -1 :
					splt = data.split('"')
					for s in splt:
						if s.find('android') != -1:
							perm = s
							break
					break
		#print protection_level
		if perm != None and protection_level != None:
			if protection_level[-1] == '\n':
				protection_level = protection_level[:-1]
			print perm, protection_level,