# Movie-Recommender-System


In the present project I create a content based recommender system for the American movies up the year 2020.
The project consists of the following steps.

#1. Data collection.


The movies up to 2017 was taken from [here] (https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset) and [here](https://www.kaggle.com/rounakbanik/the-movies-dataset?select=credits.csv).
For the years from 2018 to 2020 I used the wikipedia page for the American movies and used the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to scrape the tables. Click [this](https://en.wikipedia.org/wiki/List_of_American_films_of_2020) for the 2020 movies. Some additional data like genres was then obtained with the help of [TMDb API](https://developers.themoviedb.org/3).


#2. Model and prediction.
To classify the reviews for the movies I used TF-IDF and the Random Forest Classifier which gave a 98.8\% accuracy.

To recommend the top 10 movies, I used a simple, yet very powerful cosine similarity algorithm.