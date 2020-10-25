import pandas as pd
from flask import Flask, request
import pickle

# load model
indices = pickle.load(open('dish_indices.pkl','rb'))
cosine_sim = pickle.load(open('dish_similarity.pkl','rb'))

# app
app = Flask(__name__)

# routes
@app.route('/', methods=['GET','POST'])

def predict():
    # get data
    name = request.json['name']

    recommended_dishes = []
    
    # gettin the index of the movie that matches the title
    idx = indices[indices == name].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    # getting the indexes of the 10 most similar movies
    top_10_indexes = list(score_series.iloc[1:11].index)
    
    # populating the list with the titles of the best 10 matching movies
    for i in top_10_indexes:
        recommended_dishes.append(indices[i])

    #return result

    # send back to browser
    output = {'results': recommended_dishes}

    return output

if __name__ == '__main__':
    app.run()