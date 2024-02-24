from gensim.models.doc2vec import Doc2Vec,\
    TaggedDocument
from nltk.tokenize import word_tokenize
 
import pandas as pd
import mysql.connector

def query_data_to_df():
    # Database Setup
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='dsci560',
        database='lab4'
    )
    cursor = conn.cursor()

    # SQL query to select all data
    select_query = "SELECT * FROM posts;"

    # Execute the query
    cursor.execute(select_query)

    # Fetch all rows from the database table
    rows = cursor.fetchall()

    # Get column names
    columns = [desc[0] for desc in cursor.description]

    # Create a DataFrame from the rows and columns
    df = pd.DataFrame(rows, columns=columns)

    # Close the database connection
    conn.close()

    return df

# Example usage
df = query_data_to_df()

# drop rows where article is null
df = df.dropna(subset=['article'])

# define a list of documents.
docs = df['article']

# preproces the documents, and create TaggedDocuments
tagged_data = [TaggedDocument(words=word_tokenize(doc.lower()),
                              tags=[str(i)]) for i,
               doc in enumerate(docs)]
 
# train the Doc2vec model
model = Doc2Vec(vector_size=10,
                min_count=2, epochs=50)
model.build_vocab(tagged_data)
model.train(tagged_data,
            total_examples=model.corpus_count,
            epochs=model.epochs)

# save the model for future use
model.save('doc_vec_model.pth')
 
# get the document vectors
document_vectors = [model.infer_vector(
    word_tokenize(doc.lower())) for doc in docs]
print(document_vectors[0]) 
#  print the document vectors
#for i, doc in enumerate(docs):
#    print("Document", i+1, ":", doc)
#    print("Vector:", document_vectors[i])
#    print()

# add vectors into df
df['vector'] = document_vectors

def create_post_vectors_table():
    # Database Setup
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='dsci560',
        database='lab4'
    )
    cursor = conn.cursor()
    
    # SQL statement for creating the table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS post_vectors (
        id VARCHAR(255) NOT NULL,
        article TEXT,
        keywords TEXT,
        vector BLOB,
        PRIMARY KEY (id),
        FOREIGN KEY (id) REFERENCES posts(id)
    );
    """
    
    cursor.execute(create_table_query)
    conn.commit()
    print("Table created successfully")
    conn.close()
def insert_data_into_post_vectors(df_vectors):
    # Database Setup
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='dsci560',
        database='lab4'
    )
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO post_vectors (id, article, keywords,  vector)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    article = VALUES(article),
    keywords = VALUES(keywords),
    vector = VALUES(vector);
    """
    
    for i, row in df_vectors.iterrows():
        # Assuming the vector is stored in a format that can be directly inserted into the database
        # Convert the vector to a suitable format if necessary (e.g., serialized if it's an array)
        data_tuple = (row['id'], row['article'], row['keywords'], row['vector'].tobytes()) # convert it to bytecode , use numpy.fromstring to convert it back
        cursor.execute(insert_query, data_tuple)
    
    conn.commit()
    print("Data inserted successfully into post_vectors table")
    conn.close()

# create post_vector table if not exist
create_post_vectors_table()

# insert data to the table
insert_data_into_post_vectors(df)
print("post vectors inserted")
