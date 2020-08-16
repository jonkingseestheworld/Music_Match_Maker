# Music Match Maker
## A Music Analyzer giving suggestions on what my partner may like from my Spotify playlists based on Listening Histories and Song Features

Here is the thing - Spotify is testing a new subscription called Premium Duo that offers two Premium subscriptions for two people living in the same house at a discounted price. With Premium Duo, the users still have their own separate Spotify accounts. Premium Duo also introduces a new playlist, the Duo Mix, combining the two persons’ music preferences into one. So far, my partner doesn't quite enjoy Spotify's suggestions in the new playlist. (A sad note: I always got complained about my music choice!)   

<img src="img/badmusic.jpg" width="220">

<br>This got me very curious trying to know what songs I listened to in general may also be favoured by my partner based on listening habit. 

<img src="img/spotify_duo.jpg" width="350">
(Image: Spotify)

<br> Let me have a go and see if I can do a better job than Spotify?!

The project here analyzed the streaming histories of my partner and me in the last 12 months, in relation to some metrics of song characteristics that are available from a large collated 'song attributes' database. The database contains 160,000+ songs released in the years between 1921 and early 2020.

**The objective** of this project was to build a classifier that may be used to predict what 'new' songs a person may like (and not like) based on their listening histories. 


### About the Music Data
This project uses two main sources of data: i) **Spotify audio/track features** ("song_attributes.csv") & ii) **personal streaming history on Spotify** ("xx_StreamingHist.csv").

* **'song_attributes.csv'** is a dataset available on Kaggle (https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks; I used the specific file named 'data.csv') (Thanks Yamaç Eren Ay for sharing it). The file contains 19 columns including various song features such as acousticness, danceability, and liveness etc, collected through Spotify Web API. (For more details of these features, check this page: https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/) There are 169,909 rows/entries, with each row representing an individual song.

* The two **'xx_StreamingHist.csv'** contains personal streaming data from partner0 and partner1 (for example, from me and my partner) requested via the <a href="https://support.spotify.com/us/article/data-rights-and-privacy-settings/"> Privacy Settings section of the individual Spotify's account pages</a>. The data were provided in the json format. There are four columns in the data-file (artistName, trackName, endTime, msPlayed). Partner0's file has 15344 entries/rows and partner1's has 11424 entries.

In terms of duration, this translates to an accumulation of 790+ hours of listening on Spotify for partner0 over the past 12 months and 500+ hours for partner1 (i.e. the sum of the msPlayed column).

### Definition of 'Favourite' (vs 'not Favourite') song classes     
'Favourite' (1) and 'not favourite' (0) songs are defined by the number of listens in the past 12 months. From an exploratory analysis (see histogram below), I found that with an overpowering majority of songs Partner0 only listened to them for less than 5 times last year, and this person quite seldom listened to a song more than 5 times. This is a clear cut-off.

<br>Check the section 'What makes a favourite song' below for more details.

### Predictive Modelling
I will mainly compare the performance of 3 classification models here:

> **Nu Support Vector Classifier**     
  **Decision Tree**       
  **Random Forest**

<br>Before narrowing down the search for further hyperparameter tuning with these models, I'd also tested a number of other classifiers (e.g. Gaussian Processes, Gradient Boosting, Multilayer Perceptron), the performances of which were not as great. The scripts and outputs of those initial exploratory attempts are stored in the same repo with this notebook.

### Evaluation metrics - F1 score
When dealing with datasets with a high class imbalance like our case here (there are much fewer 'favourite' songs based on partner0's listening habit), accuracy may not be a reliable measure. The reason is that a high accuracy can be solely/largely contributed by a large number of correctly predicted negatives (i.e. True Negatives) while the positive class could be poorly predicted. In scenarios with heavily imbalanced data, we care equally about precision and recall, and F1 score would be a more preferred evaluation metric.

<br>Precision is a measure of the correctly identified positive cases from all the predicted positive cases. It is useful when the costs of False Positives is high. Recall measures the ratio of the correctly identified positive cases to all the actual positive cases. It is important when the cost of False Negatives is high.

<br>Then, F1 score is a harmonic mean of Precision and Recall, thus giving more attention to the incorrectly classified cases in general.

### Highlights of Results
A trained model using a Random Forest Classifier was able to predict unseen test data with a F1 score of 77.8%, which would be used as the final algorithm for music recommendation to predict what songs partner0 may like in an entirely separate partner1's songlist.


### Acknowledgement/Reference:
There are different song recommendation algorithms available out there and I think this one by <a href="https://github.com/isacmlee/song-recommender">isaclee</a> is really well thought and easily extendable. Remember to also check out <a href="https://github.com/isacmlee/song-recommender">isaclee</a>'s repo. My analysis here has extended based on his work. I trained a wider range of models as an initial exploratory attempt at the beginning (before filtering out models with very low performance). Also, I have written another notebook for a more in-depth [exploration of the 'song attributes' data set](https://github.com/jonkingseestheworld/Music_Match_Maker/blob/master/EDA_Song_Attributes.ipynb), for example examining how different song features varied across years.
