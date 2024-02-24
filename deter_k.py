from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
import matplotlib.pyplot as plt
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
print(df.shape)
# Generate synthetic data with 20 features
X = df['vector'].apply(lambda x: np.frombuffer(x, dtype='float32'))
print(X[0].shape)
X = np.vstack(X.values)

print(X)
# Range of k values to try
k_values = range(2, 11)

# Initialize lists to store the results
ssd = []  # Sum of Squared Distances
silhouette_scores = []

# Perform K-means clustering for each value of k and calculate SSD and silhouette score
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42).fit(X)
    ssd.append(kmeans.inertia_)  # Sum of squared distances to closest cluster center
    silhouette_scores.append(silhouette_score(X, kmeans.labels_))

# Plotting the Elbow Method result
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(k_values, ssd, 'bo-')
plt.xlabel('k')
plt.ylabel('Sum of Squared Distances')
plt.title('Elbow Method For Optimal k')

# Plotting the Silhouette Score result
plt.subplot(1, 2, 2)
plt.plot(k_values, silhouette_scores, 'ro-')
plt.xlabel('k')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score For Optimal k')

plt.tight_layout()
plt.show()
plt.savefig('elbow.png')
