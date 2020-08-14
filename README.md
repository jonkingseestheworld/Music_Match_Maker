# Music Match Maker
### A Music Analyzer giving suggestions on what my partner may like from my Spotify playlists based on Listening Histories and Song Features

Here is the thing - Spotify is testing a new subscription called Premium Duo that offers two Premium subscriptions for two people living in the same house at a discounted price. With Premium Duo, the users still have their own separate Spotify accounts. Premium Duo also introduces a new playlist, the Duo Mix, combining the two persons’ music preferences into one. So far, my partner doesn't quite enjoy Spotify's suggestions in the new playlist. (A sad note: I always got complained about my music choice!)   

<img src="img/badmusic.jpg" width="200">

<br>This got me very curious trying to know what songs I listened to in general may also be favoured by my partner based on his listening habit. 

<img src="img/spotify_duo.jpg" width="350">
(Image: Spotify)

Let me have a go and see if I can do a better job than Spotify?!





### About the Music Data
This project uses two main sources of data: i) Spotify audio/track features ("song_attributes.csv") & ii) personal streaming history on Spotify ("xx_StreamingHist.csv").

* 'song_attributes.csv' is a dataset available on Kaggle (https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks; I used the specific file named 'data.csv') (Thanks Yamaç Eren Ay for sharing it). The file contains 19 columns including various song features such as acousticness, danceability, and liveness etc, collected through Spotify Web API. (For more details of these features, check this page: https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/) There are 169,909 rows/entries, with each row representing an individual song.

* The two 'xx_StreamingHist.csv' contains personal streaming data from partner0 and partner1 (for example, from me and my partner) requested via the <a href="https://support.spotify.com/us/article/data-rights-and-privacy-settings/"> Privacy Settings section of the individual Spotify's account pages</a>. The data were provided in the json format. There are four columns in the data-file ('artistName, trackName, endTime, msPlayed). Partner0's file has 15344 entries/rows and partner1's has 11424 entries.

In terms of duration, over the past year partner0 accumulated 790+ hours of listening on Spotify and partner1 accumulated 500+ hours (i.e. the sum of the msPlayed column).



#### Acknowledgement:
There are different song recommendation algorithms out there and I think this one by <a href="https://github.com/isacmlee/song-recommender">isaclee</a> is really well thought and easily extendable. My analysis here expands on his work. Remember to also check out <a href="https://github.com/isacmlee/song-recommender">isaclee</a>'s repo - he has also created a script that enables automation of playlist creation (converting .csv song list into a Spotify playlist). 
