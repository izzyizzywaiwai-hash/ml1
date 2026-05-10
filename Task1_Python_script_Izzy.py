# Python script to scrape an article given the url of the article and store the extracted text in a file
# Url: https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7
import os
import sys
import requests
import re
# Code here - Import BeautifulSoup library
from bs4 import BeautifulSoup
# Code ends here

# function to get the html source text of the medium article
def get_page():
	global url
	
	# Code here - Ask the user to input "Enter url of a medium article: " and collect it in url
	input_str = "Enter url of a medium article: "
	url = input(input_str)
	# Code ends here
	
	# handling possible error
	if not re.match(r'https?://medium.com/',url):
		print('Please enter a valid website, or make sure it is a medium article')
		sys.exit(1)
	
	# Code here - Call get method in requests object, pass url and collect it in res
	# Set the headers to mimic a real browser, to avoid getting blocked by the website
	headers = {'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.3029.110 Safari/537.36""",'Accept-Language': 'en-US,en;q=0.9','Accept-Encoding': 'gzip, deflate, br','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Referer': 'https://www.google.com/','cache-control': 'no-cache', 'Connection': 'keep-alive','Authority': 'medium.com'}
	res = requests.get(url, headers=headers)
	# Code ends here

	# check if the request was successful
	res.raise_for_status()
	soup = BeautifulSoup(res.text, 'html.parser')
	return soup

# function to remove all the html tags and replace some with specific strings
def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>":  "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub(r'\<(.*?)\>', '', text)
    return text

# function to collect text from the soup object
def collect_text(soup):
	final_output = f'url: {url}\n\n'
	# find title, author, date
	title = soup.find('h1', {'data-testid': 'storyTitle'})
	title_text = title.get_text() if title else 'Unknown Title'
	author = soup.find('meta', {'name': 'author'})
	author_name = author.get('content') if author else 'Unknown Author'
	date = soup.find('span', {'data-testid': 'storyPublishDate'})
	published_date = date.get_text() if date else 'Unknown Date'
	# add author, title, and date to big string
	final_output += f'Author: {author_name}\n'
	final_output += f'Title: {title_text}\n'
	final_output += f'Published on: {published_date}\n'
	final_output += "--"*30 + "\n\n"
	print(f"title: {title_text}, author name = {author_name}, published date = {published_date}")
	# find paragraphs and footer
	all_content = soup.find_all(['p','footer'])
	for tag in all_content:
		# get only the text content, strip whitespace, and check if the length is greater than 10 characters
		content = tag.get_text().strip()
		if len(content) > 10: 
			final_output += f"{content}\n\n"
		# if we find a footer, break the loop and stop collecting text
		if tag.name == 'footer':
			break
	return final_output

# function to save file in the current directory
def save_file(text):
	if not os.path.exists('./scraped_articles'):
		os.mkdir('./scraped_articles')
	name = url.split("/")[-1]
	print(name)
	fname = f'scraped_articles/{name}.txt'

	# Code here - write a file using with (2 lines)
	with open(fname, 'w', encoding='utf-8') as f:
		f.write(text)
	# Code ends here

	print(f'File saved in directory {fname}')

# use the above defined functions
if __name__ == '__main__':
	soup = get_page()
	raw_text = collect_text(soup) # collect text from the soup object
	cleaned_text = clean(raw_text) # clean the text to remove html tags and replace some with specific strings
	#print(f"cleaned text = \n {cleaned_text}")
	save_file(cleaned_text)
	# Instructions to Run this python code
	# Give url as https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7