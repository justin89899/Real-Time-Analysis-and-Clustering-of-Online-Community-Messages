from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import pickle
import numpy as np
import matplotlib.pyplot as plt

def cluster_new_doc(doc):
    #load doc2vec model
    d2v = Doc2Vec.load('doc_vec_model.pth')
    
    # get the vector
    document_vector = d2v.infer_vector(word_tokenize(doc.lower())).reshape(1, -1)
   
    # load kmeans model
    kmeans = pickle.load(open('kmeans.pkl', 'rb'))

    # predict new points
    new_label = kmeans.predict(document_vector) 

    # load reduced data (original cluster points) & labels and class names for visualization
    data_reduced = pickle.load(open('data_reduced.pkl', 'rb'))
    labels = pickle.load(open('labels.pkl', 'rb'))
    class_names = pickle.load(open('class_names.pkl', 'rb'))

    # Determine unique classes
    unique_labels = np.unique(labels)
   
    # load PCA
    pca = pickle.load(open('pca.pkl', 'rb'))

    # tranform new vec
    new_vec_reduced = pca.transform(document_vector)

    # Plot the data
    plt.figure(figsize=(8, 6))
    plt.subplots_adjust(bottom=0.25)
    for label in unique_labels:
        idx = labels == label
        # Use the class name from the mapping for the label
        plt.scatter(data_reduced[idx, 0], data_reduced[idx, 1], label=f'Class {label},{class_names[label]}', alpha=0.2)
    plt.scatter(new_vec_reduced[0, 0],new_vec_reduced[0, 1], label=f'New doc, Class {new_label}', marker= 'v', alpha= 0.9)
    #scatter = plt.scatter(data_reduced[:, 0], data_reduced[:, 1], c=labels, cmap='viridis', alpha=0.7)
    plt.title('PCA of Dataset')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(loc='lower center',bbox_to_anchor=(0.5, -0.4),fontsize='small')
    plt.show()
    #plt.savefig('new_pca.png')

#new_doc = "Good morning and welcome to Tech News Now, TheStreet's daily tech rundown.In todays edition, we re covering Mark Zuckerbergs review of Apples Vision Pro, Microsofts and OpenAIs announcement about how they are dealing with threats from malicious actors, a departure from Apple's design team, and Max is adding Dolby Vision for live sports.It was only a matter of time, truly. But Meta CEO Mark Zuckerberg, like Elon Musk, Sam Altman, and countless other individuals, tried out Apple's Vision Pro and has some thoughts. The main takeaway from his remarks: I don’t just think that [Metas Quest headset] is the better value. I think Q His review was filmed using passthrough on the Quest 3, showing off the ability to also place windows around him. Zuckerberg explained that Metas latest headset weighs a bit less than Apples and can be worn comfortably for longer. Additionally, it is easier to move in since it doesnt have a battery pack, and he believes hand controllers and tracking are better inputs."
#cluster_new_doc(new_doc)
