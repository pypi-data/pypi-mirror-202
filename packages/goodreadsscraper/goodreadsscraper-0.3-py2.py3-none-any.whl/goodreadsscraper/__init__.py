#! /usr/bin/env python3
"""Module to scrap book information from goodreads
"""

__version__ = '0.3'

__description__ = 'Module to scrap book information from goodreads'

import os
import time
import re
import json
import traceback
import jellyfish
import threading as th
import requests
from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import *
from .book import Book
from .author import Author
from .review import Review

path = os.path.dirname(os.path.realpath(__file__))





def create_driver(args)->webdriver:
	"""Create driver to make requests from pages\nNeeded because of the great use of js"""
	driver = None
	log(args,f'Creating driver')
	try:
		log(args,f'Firefox')
		opf = webdriver.FirefoxOptions()
		opf.add_argument('--window-size=1440,900')
		opf.add_argument('--headless')
		driver = webdriver.Firefox(options=opf)
	except:
		log(args,f'Could not create Chrome driver')
		try:
			log(args,f'Chrome')
			opg = webdriver.ChromeOptions()
			opg.add_argument('--window-size=1440,900')
			opg.add_argument('--headless')
			driver = webdriver.Chrome(options=opg)
		except:
			log(args,f'Could not create Firefox driver')
			driver = None
	if driver:
		driver.implicitly_wait(2)
		log(args,f'Driver created')
	else:
		log(args,f'Could not create driver. Please read documentation to install proper dependencies.')
		error(args,f'Could not create driver. Please read documentation to install proper dependencies.')
	return driver


def driver_wait_element_to_be_clickable(driver:webdriver,xpath:str,timeout:int=1):
	'''Waits until timeout for element in XPATH to become clickable'''
	WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH,xpath)))

def driver_wait_element(driver,xpath:str,timeout:int=1,exist:bool=True):
	'''Waits until timeout for element in XPATH to either exist or not'''
	if exist:
		WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
	else:
		WebDriverWait(driver, timeout).until(EC.none_of(EC.presence_of_element_located((By.XPATH, xpath))))






def search_book_option(args):
	"""Verify if a book search option was given"""
	return args.isbn or args.id or args.btitle


def search_btitle(args,driver:webdriver,btitle:str,page:str)->str:
	"""Searches for a book page using its name and author if given"""
	log(args,f'Finding best match...')
	r = None
	soup = BeautifulSoup(page,features='lxml')
	books = soup.find_all('a',{'class':'bookTitle'})
	authors = soup.find_all('a',{'class':'authorName'})
	similarityDic = []
	if args.author:
		a = args.author.lower().replace(' ','')
	# Search through every listed book for a book match
	for i,book in enumerate(books):
		bname = book.find('span',{'itemprop':'name'}).get_text().lower().replace(' ','')
		bname = re.sub(r'([^(]+)\s*(\(.+\))?',r'\1',bname)
		url = book['href']
		difference = jellyfish.levenshtein_distance(btitle,bname)
		# Use given author to increase book search precision
		if args.author:
			author = authors[i]
			aname = author.find('span',{'itemprop':'name'}).get_text().lower().replace(' ','')
			differenceA = jellyfish.levenshtein_distance(a,aname)
			if similitarity_percent(aname,differenceA) < 0.6:
				if similitarity_percent(btitle,difference) < 0.6:
					similarityDic.append((bname,url,difference))
				# Stops with perfect match
				if difference == 0:
					break
		# Default search
		else:
			if similitarity_percent(btitle,difference) < 0.5:
				similarityDic.append((bname,url,difference))
			# Stops with perfect match
			if difference == 0:
				break
	# Choose the best match
	if len(similarityDic)>0:
		log(args,f'Match found.')
		similarityDic = sorted(similarityDic,key=lambda x: x[2])
		driver.get(f'https://www.goodreads.com{similarityDic[0][1]}')
		r = driver.page_source
	else:
		error(args,f'Could not find book name {args.btitle}')
	return r

def is_book_page(url:str)->bool:
	"""Checks if response is relative to a book page"""
	return re.search('www.goodreads.com/book/show/',url)


def load_book_page(args,driver)->bool:
	"""Waits for book page to be loaded, refreshes some times if stuck"""
	loaded = False 
	tries = 5
	while not loaded and tries > 0:
		try:
			log(args,f'Waiting for page to load...')
			driver_wait_element(driver,"//div[@class='LoadingCard']",10,False)
			driver_wait_element(driver,'//script[@type="application/json"]',10)
			if re.search('ROOT_QUERY',driver.page_source):
				loaded = True
			else:
				log(args,f'Refreshing page...')
				driver.get(driver.current_url)
				time.sleep(1)
			tries-= 1
		except:
			log(args,f'Refreshing page...')
			driver.get(driver.current_url)
			time.sleep(1)
			tries-= 1
	return loaded


def get_book_page(args,driver:webdriver)->str:
	"""Performs a get request to goodreads for a book with a give isbn, work id or search name"""
	r= None
	# Search with book's isbn
	if args.isbn:
		log(args,f"Searching for book with isbn - {args.isbn}...")
		driver.get(f"https://www.goodreads.com/search?q={args.isbn}")
		args.id = get_book_id(driver.current_url)
		loaded = load_book_page(args,driver)
		if loaded:
			log(args,f'Loaded')
			r = driver.page_source

	# Search with book's work id'
	elif args.id:
		log(args,f"Searching for book with id - {args.id}...")
		driver.get(f"https://www.goodreads.com/book/show/{args.id}")
		loaded = load_book_page(args,driver)
		if loaded:
			log(args,f'Loaded')
			r = driver.page_source

	# Search with search name (less precise)
	elif args.btitle:
		log(args,f"Searching for book with name - {args.btitle}...")
		btitle = args.btitle.lower().replace(' ','')
		driver.get(f"https://www.goodreads.com/search?q={args.btitle}")
		page = driver.page_source
		r = search_btitle(args,driver,btitle,page)
		if r:
			args.id = get_book_id(driver.current_url)
			loaded = load_book_page(args,driver)
			if loaded:
				log(args,f'Loaded')
				r = driver.page_source
			else:
				r = None

	log(args,f"Search finished")
	if r  and is_book_page(driver.current_url):
		return r
	else:
		error(args,f'Could not find book')
		return None




def get_book_id(url:str)->str:
	"""Return a book's id using a url"""
	id = re.search(r'www.goodreads.com/book/show/(\d+)',url).group(1)
	return id



def scrape_book_page(args,html_page:str)->Book:
	"""Scrapes a book's page for info such as title, score, number of reviews and others"""
	log(args,f"Scraping book info...")
	page = BeautifulSoup(html_page,features='lxml')

	# Read and prepare dic with information
	page_info_dic = page.find('script',{'type':'application/json'}).get_text()
	page_info_dic = json.loads(page_info_dic)
	page_info_dic = page_info_dic['props']['pageProps']['apolloState']
	book_query = page_info_dic['ROOT_QUERY']
	key = 'getBookByLegacyId({"legacyId":"'+args.id+'"})'
	book_legacy_id = book_query[key]['__ref']
	book_info = page_info_dic[book_legacy_id]
	book_contributor_id = book_info['primaryContributorEdge']['node']['__ref']
	author_info = page_info_dic[book_contributor_id]
	book_work_id = book_info['work']['__ref']
	book_stats = page_info_dic[book_work_id]['stats']

	# Scrape information from dic
	book_details = book_info['details']
	
	book_name = book_info['title']
	book_author = author_info['name']
	book_description = book_info['description']

	book_score = book_stats['averageRating']
	book_nratings = book_stats['ratingsCount']
	book_nreviews = book_stats['textReviewsCount']

	book_npages = book_details['numPages']
	book_language = book_details['language']['name']
	book_isbn = book_details['isbn13']
	try:
		# Original date
		book_publishing_date = datetime.fromtimestamp(page_info_dic[book_work_id]['details']['publicationTime']/1000).date()
	except:
		# Edition date
		book_publishing_date = datetime.fromtimestamp(book_details['publicationTime']/1000).date()

	book_genres = []
	for genre in book_info['bookGenres']:
		book_genres.append(genre['genre']['name'])


	log(args,f"Scrape finished")
	return Book(book_name,book_isbn,book_author,
	     book_description,book_publishing_date,book_score,
		 book_nratings,book_nreviews,book_npages,
		 book_language,book_genres)






def get_author_page(args,driver:webdriver)->str:
	"""Performs a get request to goodreads for a author with a give name or id\n
	   If a name is given an indirect search is made by finding a work of the author and proceeding from there
	"""
	r= None
	# Check flag
	#if args.author and not search_book_option(args):
	if args.author:
		a = args.author.lower().replace(' ','')
		match = re.match(r'\d+$',a)
		# Search by author id
		if match:
			log(args,f"Searching for author with id - {args.author}...")
			driver.get(f"https://www.goodreads.com/author/show/{args.author}")
			search = driver.page_source
			soup = BeautifulSoup(search,features='lxml')
			if re.search(r'Page not found',soup.find('title').get_text()):
				error(args,f'Could not find author id {args.author}')
			else:
				r = search

		# Search by author name
		else:
			log(args,f"Searching for author with name - {args.author}...")
			driver.get(f"https://www.goodreads.com/search?q={args.author}")
			search = driver.page_source
			soup = BeautifulSoup(search,features='lxml')
			authors = soup.find_all('a',{'class':'authorName'})
			similarityDic = []
			# Search through every listed book for an author match
			for author in authors:
				name = author.find('span',{'itemprop':'name'}).get_text().lower().replace(' ','')
				url = author['href']
				difference = jellyfish.levenshtein_distance(a,name)
				if similitarity_percent(a,difference) < 0.5:
					similarityDic.append((name,url,difference))
				if difference == 0:
					break

			# Choose the best match
			if len(similarityDic)>0:
				similarityDic = sorted(similarityDic,key=lambda x: x[2])
				driver.get(similarityDic[0][1])
				r = driver.page_source
			else:
				error(args,f'Could not find author name {args.author}')
		log(args,f"Search finished")
	return r


def get_page_works(page:BeautifulSoup)->List[str]:
	"""Get all the books from a page that lists them"""
	works = []
	books = page.find_all('a',{'class':'bookTitle'})
	for book in books:
		works.append(book.find('span',{'itemprop':'name'}).get_text().strip())
	return works




def get_author_works(args,works_url:str,max:int=None)->List[str]:
	"""Get the list of unique works of an author\n
	Max represents the maximum number of works to obtain (by default gathers all going from page to page)"""
	works = []
	if works_url:
		log(args,f"Scraping author's books")
		page_number = 1
		count = 0
		r = requests.get(f'https://www.goodreads.com/{works_url}?page=1&per_page=30')
		if r.status_code == 200:
			page = BeautifulSoup(r.content.decode(r.encoding),features='lxml')
			max_pages_element = page.find('div',{'style':'float: right'}).find_all('a')
			if max_pages_element:
				max_pages = int(max_pages_element[-2].get_text().strip())
			else:
				max_pages = 1
			page_works = get_page_works(page)
			if max and count + len(page_works) > max:
				works += page_works[:max-count]
			else:
				works += page_works
				count += len(page_works)
				# Search through all the pages of books, until limit reached (max to collect or all collected)
				for i in range(2,max_pages+1):
					r = requests.get(f'https://www.goodreads.com/{works_url}?page={i}&per_page=30')
					if r.status_code == 200:
						page = BeautifulSoup(r.content.decode(r.encoding),features='lxml')
						page_works = get_page_works(page)
						if max and count + len(page_works) > max:
							works += page_works[:max-count]
							break
						else:
							works += page_works
							count += len(page_works)
		log(args,f"Scraping finished")
	if works:
		return works
	else:
		return None


def scrape_author_page(args,html_page:str)->Author:
	"""Scrapes an author's page for info such as name, birthday, average score, number of reviews and others"""
	log(args,f"Scraping author's page for info")
	page = BeautifulSoup(html_page,features='lxml')

	author_name = page.find('h1',{'class':'authorName'}).get_text().strip()
	author_birthdate = page.find('div',{'class':'dataItem','itemprop':"birthDate"}).get_text().strip()
	author_birthplace = page.find('div',{'class':'dataTitle'}).next_sibling.get_text().strip()
	author_deathdate = None
	# Death date
	element_deathdate = page.find('div',{'class':'dataItem','itemprop':"deathDate"})
	if element_deathdate:
		author_deathdate = element_deathdate.get_text().strip()
	author_website = page.find('a',{'itemprop':"url"}).get_text().strip()
	# Description
	element_description = page.find('div',{'class':'aboutAuthorInfo'}).find('span')
	if(element_description.find_next_sibling('span')):
		author_description = element_description.get_text().strip()
	else: author_description = element_description.get_text().strip()

	author_averageRating = page.find('span',{'class':'average','itemprop':'ratingValue'}).get_text().strip()
	author_nratings = page.find('span',{'class':'value-title','itemprop':'ratingCount'}).get_text().strip()
	author_nreviews = page.find('span',{'class':'value-title','itemprop':'reviewCount'}).get_text().strip()
	author_nUniqueWorks = None

	# Catch author's genres and influences
	dataItems = page.find_all('div',{'class':'dataItem'})
	author_genres = []
	author_influences = []
	works_url = None
	for item in dataItems:
		items = item.find_all('a')
		for item in items:
			if item['href']:
				if re.search('genres',item['href']):
					author_genres.append(item.get_text().strip())
				elif re.search('/author/show/',item['href']):
					author_influences.append(item.get_text().strip())

	author_stats = page.find('div',{'class':'hreview-aggregate'})
	items = author_stats.find_all('a')
	for item in items:
		if re.search('/author/list/',item['href']):
			author_nUniqueWorks = item.get_text().strip()
			works_url = item['href']

	max = args.maxworks
	author_works = get_author_works(args,works_url,max)
	log(args,f"Scraping finished")
	return Author(author_name,author_birthdate,author_birthplace,
	       author_deathdate,author_website,author_genres,
		   author_influences,author_description,author_averageRating,
		   author_nratings,author_nreviews,author_nUniqueWorks,author_works)


def load_reviews_page(args,driver)->bool:
	"""Waits for review page to be loaded, refreshes some times if stuck"""
	loaded = False 
	tries = 5
	while not loaded and tries > 0:
		try:
			log(args,f'Waiting for page to load...')
			# Wait for reviews to appear
			driver_wait_element(driver,"//div[@class='ReviewsList']",20)
			# Check if something is still loading
			driver_wait_element(driver,"//div[@class='LoadingCard']",20,False)
			if re.search('ROOT_QUERY',driver.page_source):
				loaded = True
			else:
				log(args,f'Refreshing page...')
				driver.get(driver.current_url)
				time.sleep(1)
			tries-= 1
		except:
			log(args,f'Refreshing page...')
			driver.get(driver.current_url)
			time.sleep(1)
			tries-= 1
	return loaded

def get_book_reviews_page(args,driver)->str:
	"""Return the book reviews page (if book flags active)"""
	r = None

	if search_book_option(args):
		log(args,f"Searching for book reviews's page")
		id = None
		if args.id:
			id = args.id

		elif args.isbn or args.btitle:
			get_book_page(args,driver)
			url = driver.current_url
			id = get_book_id(url)
		
		if id:		
			log(args,f"Trying to get reviews page")
			driver.get(f'https://www.goodreads.com/book/show/{id}/reviews')
			if not load_reviews_page(args,driver):
				error(args,'Could not get proper reviews page')
			else:
				r = driver.page_source

		log(args,f"Search finished")
	return r


def scrape_reviews_page(args,html_page:str,lower_limit:int=None,higher_limit:int=None)->List[Review]:
	"""Scrape reviews from page, if range is given only grab reviews in that range"""
	reviews_list = []
	log(args,f"Scraping reviews's page for info")

	page = BeautifulSoup(html_page,features='lxml')
	book_name = page.find('a',{'data-testid':'title'}).get_text()
	div_reviews_list = page.find('div',{'class':'ReviewsList'})
	reviews = div_reviews_list.find_all('article',{'class':'ReviewCard'})
	# Change range of reviews to gather
	reviews = list_range(reviews,lower_limit,higher_limit)
	# Get info from all the reviews
	for review in reviews:
		reviewer_info = review.find('div',{'class':'ReviewerProfile__name'})
		reviewer_main = reviewer_info.find('a')
		reviewer_name = reviewer_main.get_text().strip()
		reviewer_id = re.search(r'/user/show/(\d+)',reviewer_main['href']).group(1)
		review_score = None
		review_score_elem = review.find('div',{'class':'ShelfStatus'}).find('span')
		if review_score_elem:
			review_score = re.search(r'Rating (\d+) out of \d+',review_score_elem['aria-label']).group(1)
		review_description_card = review.find('section',{'class','ReviewText__content'})
		review_description = review_description_card.find('span').get_text().strip()
		rev = Review(book_name,reviewer_id,reviewer_name,review_score,review_description)
		reviews_list.append(rev)
	log(args,f"Scraping finished")
	return reviews_list



def get_review_page_stats(page:str)->List[int]:
	"""Recovers simple stats about review page, such as number of reviews and range shown"""
	soup = BeautifulSoup(page,features='lxml')
	try:
		number_reviews_elem = soup.find('div',{'class':'ReviewsList__listContext'}).find('span')
		number_reviews_info = re.search(r'(\d+((,|\.)\d+)?)[^\d]*(\d+((,|\.)\d+)?)[^\d]*(\d+((,|\.)\d+)?)',number_reviews_elem.get_text().strip())
		if len(number_reviews_info.groups()) >= 7:
			n_reviews = int(re.sub(r'(.*),|\.(.*)',r'\1\2',number_reviews_info.group(7)))
			lower_review = int(re.sub(r'(.*),|\.(.*)',r'\1\2',number_reviews_info.group(1)))
			higher_review = int(re.sub(r'(.*),|\.(.*)',r'\1\2',number_reviews_info.group(4)))
		else :
			n_reviews = int(re.sub(r'(.*),|\.(.*)',r'\1\2',number_reviews_info.group(4)))
			lower_review = int(re.sub(r'(.*),|\.(.*)',r'\1\2',number_reviews_info.group(1)))
			higher_review = int(re.sub(r'(.*),|\.(.*)',r'\1\2',number_reviews_info.group(4)))
	except:
		n_reviews = 0
		lower_review = 0
		higher_review = 0
	return [n_reviews,lower_review,higher_review]


def review_page_show_more(args,driver):
	"""Activates show more reviews javascript on review page"""
	log(args,f'Showing more reviews...')
	try:
		elem = driver.find_element(By.XPATH,"//span[text()='Show more reviews']")
		driver.execute_script("arguments[0].scrollIntoView();", elem)
		driver_wait_element_to_be_clickable(driver,"//span[text()='Show more reviews']",1000000)
		time.sleep(0.5)
		elem.click()
		driver_wait_element(driver,"//button[@class='Button Button--secondary Button--small Button--disabled']",1000000,False)
		log(args,f'Got more reviews.')
	except Exception as e:
		log(args,f'No more reviews.')
		print(traceback.format_exc())


def reviews_page_filter_language(args,driver)->bool:
	"""Activates filter option on review page"""
	log(args,f'Filtering reviews...')
	filtered = False
	try:
		elem = driver.find_element(By.XPATH,"//span[text()='Filters']")
		if elem:
			elem.click()
			driver_wait_element_to_be_clickable(driver,"//span[text()='Apply']",1000000)
			filter = driver.find_element(By.XPATH ,f"//label[@class='RadioInput'][@for='{args.reviews_language}']")
			if filter:
				driver.execute_script("arguments[0].scrollIntoView();", filter)
				WebDriverWait(driver, 10000).until(EC.presence_of_element_located((By.XPATH, f"//label[@class='RadioInput'][@for='{args.reviews_language}']")))
				time.sleep(0.5)
				filter.click()
				driver_wait_element_to_be_clickable(driver,"//span[text()='Apply']",1000000)
				apply = driver.find_element(By.XPATH,"//span[text()='Apply']")
				apply.click()
				filtered = True
				driver_wait_element(driver,"//div[@class='LoadingCard']",10,False)
	except Exception as e:
		print(e)
	if filtered:
		log(args,f'Reviews filtered.')
	else:
		log(args,f'Could not filter reviews.')
	return filtered


def scrape_reviews(args,driver)->List[Review]:
	"""Gets reviews from book page"""
	reviews = []
	if args.reviews_simple or args.reviews:
		log(args,f'Scraping book reviews...')
		page = get_book_reviews_page(args,driver)
		if page:
			driver.refresh()
			# Filters reviews in page according to chosen language
			if args.reviews_language:
				filtered = reviews_page_filter_language(args,driver)
				page = driver.page_source
				if not filtered:
					return reviews
				
			range = [None,None]
			if args.reviews_range:
				range = [args.reviews_range[0],args.reviews_range[1]]

			# Only get the minimum number of reviews
			if args.reviews_simple:
				log(args,f'Simple review scraping')
				reviews = scrape_reviews_page(args,page,range[0],range[1])

			# Get more reviews
			elif args.reviews:
				log(args,f'Full review scraping')
				reviews += scrape_reviews_page(args,page,range[0],range[1])
				review_page_show_more(args,driver)
				count = len(reviews)
				# Writes to file so as not to use too much memory
				if args.reviews_output:
					header = (count > 0)
					write_reviews(args,reviews,header=header)
					if args.reviews_range:
						range[0] = range[0] + len(reviews)
					reviews = []

				n_reviews,lower_review,higher_review = get_review_page_stats(page)
				# Get reviews in range
				if args.reviews_range:
					max_reviews = range[1]-range[0]
					range[0] = range[0] + len(reviews)
				# Get all reviews
				else:
					max_reviews = n_reviews
					range[0] = len(reviews)

				while(count < n_reviews and count < max_reviews):
					log(args,f'Current reviews : {count} of {max_reviews} | total : {n_reviews}')
					page = driver.page_source
					thread = th.Thread(target=review_page_show_more,args=[args,driver])
					thread.start()
					n_reviews,lower_review,higher_review = get_review_page_stats(page)
					reviews += scrape_reviews_page(args,page,range[0],range[1])
					if len(reviews) > 0:
						# Writes to file so as not to use too much memory
						if args.reviews_output:
							if not header:
								header = True
								write_reviews(args,reviews,header=header)
							else:
								write_reviews(args,reviews)
							range[0] += len(reviews)
							count += len(reviews)
							reviews = []
						else:
							range[0] = len(reviews)
							count = len(reviews)
					thread.join()
				
		log(args,f'Finished Scraping')
	return reviews



def goodreadsscraper():
	"""Main function of the program"""
	args = parse_arguments(__version__)
	books,authors = process_arguments(args)
	if len(books) > 0 or len(authors) > 0:
		driver = create_driver(args)
		if driver:
			try:
				results = []
				results_reviews = []
				first_write = True
				
				for book in books:
					# Get the page of a book
					res = get_book_page(book,driver)
					if res:
						b = scrape_book_page(book,prettify_html(res))
						results.append({'out':book.output,'result':b.__str__(True if args.verbose else False)})
					
					if(book.reviews_simple or book.reviews and res):
						reviews = scrape_reviews(book,driver)
						if reviews:
							delim = ';'
							# Allow for multiple review pages to be written in the main review output
							if not book.reviews_output:
								if first_write:
									write_reviews(args,reviews,first_write,True,delim)
									first_write = False
								else:
									write_reviews(args,reviews,first_write,True,delim)
							else:
								df = create_dataset(reviews[0].header(),[review.dataset_line() for review in reviews])
								data = df.to_csv(None,sep=delim,columns=reviews[0].header(),quoting=1)
								out = open(book.reviews_output,'w') if book.reviews_output else None
								results_reviews.append({'out' : out, 'result':data})

					
				for author in authors:
					# Get the page of an author
					res = get_author_page(author,driver)
					if res:
						a = scrape_author_page(author,prettify_html(res))
						results.append({'out':author.output,'result':a.__str__(True if args.verbose else False)})

				driver.quit()
				for result in results:
					write_output(result['out'],result['result'])
				
				for result in results_reviews:
					write_output(result['out'],result['result'])

			except Exception as e:
				error(args,f'Fatal error -> {traceback.format_exc()}')
				file = open(f'{path}/test/debug.html','w')
				file.write(prettify_html(driver.page_source))
				file.close()
				driver.quit()
			except KeyboardInterrupt as e:
				error(args,f'Interrupted error -> {e}')
				file = open(f'{path}/test/debug.html','w')
				file.write(prettify_html(driver.page_source))
				file.close()
				driver.quit()
	else:
		error(args,'No options selected')


