from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
from pickle import dump
from sklearn.decomposition import PCA

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
    select_query = "SELECT * FROM post_vectors;"

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

# get data from post_vectors table
df = query_data_to_df()

# Generate synthetic data with 20 features
X = df['vector'].apply(lambda x: np.frombuffer(x, dtype='float32'))
X = np.vstack(X.values)

# Perform K-means clustering for k = 3
kmeans = KMeans(n_clusters=4, random_state=42).fit(X)

# save the model
dump(kmeans, open('kmeans.pkl', 'wb'))


labels = kmeans.labels_

# Determine unique classes
unique_labels = np.unique(labels)

# get the frequent keywords
keywords_dict_list = []

keywords = df['keywords'].apply(lambda x: x.split('_') if x else "")
for label in unique_labels:
    idx = labels == label
    keywords_dict = {}
    keywords_label = keywords[idx]
    for kwds in keywords_label:
        if kwds:
            for kw in kwds:
                keywords_dict[kw.lower()] = keywords_dict.get(kw.lower(), 0) + 1
    keywords_dict_list.append(keywords_dict)
#print(sorted(keywords_dict_list[0].items(), key=lambda x:x[1], reverse=True)[:10])
#print(sorted(keywords_dict_list[1].items(), key=lambda x:x[1], reverse=True)[:10])
#print(sorted(keywords_dict_list[2].items(), key=lambda x:x[1], reverse=True)[:10])
#print(sorted(keywords_dict_list[3].items(), key=lambda x:x[1], reverse=True)[:10]) 
first_class = [k[0] for k in sorted(keywords_dict_list[0].items(), key=lambda x:x[1], reverse=True)[:10]]
second_class = [k[0] for k in sorted(keywords_dict_list[1].items(), key=lambda x:x[1], reverse=True)[:10]]
third_class = [k[0] for k in sorted(keywords_dict_list[2].items(), key=lambda x:x[1], reverse=True)[:10]]
forth_class = [k[0] for k in sorted(keywords_dict_list[3].items(), key=lambda x:x[1], reverse=True)[:10]]

class_names = {
    0: f'{first_class}',
    1: f'{second_class}',
    2: f'{third_class}',
    3: f'{forth_class}',
    # Add more mappings as needed
}

# Assuming 'data_for_clustering' is your data and 'labels' are the class labels

# Perform PCA to reduce to 2 dimensions
pca = PCA(n_components=2)
data_reduced = pca.fit_transform(X)

# save the model
dump(pca, open('pca.pkl', 'wb'))

# save the reduced data and label and class names
dump(data_reduced, open('data_reduced.pkl', 'wb'))
dump(labels, open('labels.pkl', 'wb'))
dump(class_names, open('class_names.pkl', 'wb'))
# Plot the data
plt.figure(figsize=(8, 6))
#plotting the results:
 
for label in unique_labels:
    idx = labels == label
    # Use the class name from the mapping for the label
    plt.scatter(data_reduced[idx, 0], data_reduced[idx, 1], label=class_names[label], alpha=0.7)
#scatter = plt.scatter(data_reduced[:, 0], data_reduced[:, 1], c=labels, cmap='viridis', alpha=0.7)
plt.title('PCA of Dataset')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.show()

plt.savefig('pca.png')


