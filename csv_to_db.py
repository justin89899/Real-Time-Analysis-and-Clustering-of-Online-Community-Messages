import pandas as pd
import mysql.connector

# Function to read CSV and insert data into DB
def read_csv_and_insert_to_db(csv_file_path):
    # Read CSV file into DataFrame
    df = pd.read_csv(csv_file_path)
    # Convert NaN values to None (SQL NULL)
    df = df.where(pd.notnull(df), None) 
    # Call the function to insert data into the database
    insert_posts_to_db(df)

# Function to insert or update data into the database
def insert_posts_to_db(df):
    # SQL query for inserting or updating data
    insert_query = """INSERT INTO posts (id, title, post_url, article, keywords)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        title = VALUES(title),
        post_url = VALUES(post_url),
        article = VALUES(article),
        keywords = VALUES(keywords);"""

    # Iterate over DataFrame rows and insert data into the database
    for i, row in df.iterrows():
        data_tuple = (row['ID'], row['Title'], row['Post URL'], row['article'], row['keywords'])
        cursor.execute(insert_query, data_tuple)
    
    conn.commit()
    print("Data inserted successfully into posts table")
    conn.close()

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

# Example usage
csv_file_path = 'new_posts.csv'
read_csv_and_insert_to_db(csv_file_path)
