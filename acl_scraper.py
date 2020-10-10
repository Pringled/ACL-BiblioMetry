import requests
import time

url='https://www.aclweb.org/anthology/'
page = requests.get(url)
page_source = page.text
page_source = page_source.split(' ')

links = []
for line in page_source:
	if 'anthology/events' in line:
		link = "https://www.aclweb.org/" + "/".join(line.split("/", 4)[1:4])
		links.append(link)

total_counter = 0
for link in links:
	title = link.split("/")[5]
	page = requests.get(link)
	page_source = page.text 
	page_source = page_source.split(' ')
	counter = 0
	skip = 0
	for i, line in enumerate(page_source):
		if ".pdf" in line and not "Poster" in line and not "Presentation" in line and not "Supplementary" in line and not "Notes" in line and not "Attachment" in line:
			# only download pdfs that are actual papers
			if skip == 1:
				# skip first occurance of pdf and bib file
				pdf_link = line[5:]
				pdf_title = title + "-" + str(counter)
				bib_link = pdf_link[0:-4] + ".bib"
	
				if total_counter >= 0:
					# in case of a crash, start scraping at current total_counter
					try:
						response = requests.get(pdf_link)
						bib_response = requests.get(bib_link)
						with open(str(pdf_title) + '.bib', 'wb') as f:
							f.write(bib_response.content)
						with open(str(pdf_title) + '.pdf', 'wb') as f:
							f.write(response.content)   
					except ConnectionError:
						time.sleep(1)
						print("Error, retrying")	
		
				print(total_counter)
			skip = 1
	
			counter += 1
			total_counter += 1