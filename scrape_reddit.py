import praw
import pandas as pd
from newspaper import Article
from helper import scrape_ieee, scrape_reuters
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import mysql.connector
from mysql.connector import Error
import spacy

# define fetch posts function
def fetch_posts(posts_dict, subreddit_name='tech', limit=20, resume_from_id=None):
	app = praw.Reddit(client_id="4VUYW4XkQWVC0m61YN6Qrw",
			client_secret="Q1uVY3-7XxvuiIsXJflGtXTlGNp3Pg",
			user_agent='scraping')

	subreddit = app.subreddit(subreddit_name)

	# Adjust the starting point based on resume_from_id
	if resume_from_id:
		posts = subreddit.new(limit=limit, params={'after': resume_from_id})
	else:
		posts = subreddit.new(limit=limit)

	last_id = None
	try:
		for post in posts:
			print(post.title)
			if 'reuters' in post.url:
				continue
			posts_dict["Title"].append(post.title)
			posts_dict["ID"].append(post.id)
			posts_dict["Post URL"].append(post.url)
			print(post.url)
			#if 'spectrum.ieee' in post.url:
			#	full_article = scrape_ieee(post.url)
			#else:
			try:
				article = Article(post.url)
				article.download()
				article.parse()
				full_article = article.text
			except:
				full_article = post.title
			posts_dict["article"].append(full_article)
			nlp = spacy.load("en_core_web_sm")
			doc = nlp(full_article)
			doc = list(doc.ents)
			keywords = ""
			if len(doc) >= 5:
				for i in range(5):
					keywords += str(doc[i])
					keywords += "_"
			else:
				for i in range(len(doc)):
					keywords += str(doc[i])
					keywords += "_"
			posts_dict['keywords'].append(keywords[:-1])
			last_id = post.id  # Update last_id with the current post's ID
	except Exception as e:
		print(f"An error occurred: {e}")
		if last_id:
			# Attempt to resume from the last successful post ID
			print(f"Resuming from ID {last_id} after a short pause...")
			time.sleep(60)  # Wait a bit in case of rate limit errors
			fetch_posts(subreddit_name, posts_dict, limit=limit - len(posts_dict["ID"]), resume_from_id=last_id)

	return pd.DataFrame(posts_dict)

# insert into mysql database
def insert_posts_to_db(df):
	insert_query = """INSERT INTO posts (id, title, post_url, article, keywords)
		VALUES (%s, %s, %s, %s, %s)
		ON DUPLICATE KEY UPDATE
		title = VALUES(title),
		post_url = VALUES(post_url),
		article = VALUES(article),
		keywords = VALUES(keywords);"""

	for i, row in df.iterrows():
		data_tuple = (row['ID'], row['Title'], row['Post URL'], row['article'], row['keywords'])
		cursor.execute(insert_query, data_tuple)
	conn.commit()
	print("Data inserted successfully into posts table")
	conn.close()


# Initialize the dictionary outside the function
posts_dict = {"Title": [],
		"ID": [],
		"Post URL": [],
		"article": [],
		"keywords": []
		}

# Database Setup
conn = mysql.connector.connect(
	host='localhost',
	user='root',
	password='dsci560',
	database='lab4'
)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
    id VARCHAR(255) PRIMARY KEY,
    title TEXT,
    post_url TEXT,
    article TEXT,
    keywords TEXT
    )
''')

input = input("How many posts?")
# Starting the fetch process without resuming (no last_id)
subreddit_name = 'tech'
posts_df = fetch_posts(subreddit_name=subreddit_name, posts_dict=posts_dict, limit=int(input))

# Call the function to insert data
insert_posts_to_db(posts_df)

# Save the DataFrame to CSV
posts_df.to_csv('new_posts.csv', index=False)
