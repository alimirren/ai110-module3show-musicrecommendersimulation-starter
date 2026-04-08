# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**EarBless Alpha Release**

---

## 2. Intended Use  

EarBless is a music recommender simulator that you could use to find songs (in existing database) you would enjoy.

---

## 3. How the Model Works  

This simulation has a scoring function. It is rated against your favorite genre, mood, and qualities like energy level, tempo, danceability, positivity, and acousticity. When the song matches your taste, it goes through some math that will calculate its score. The higher the score, the higher the song is on the list.

---

## 4. Data  

There are a total of 18 songs in the dataset. They feature different genres and are very diverse. I upgraded the original dataset and added new qualities to the songs.

---

## 5. Strengths  

Math works well in the code. Every binary comparison works well to be honest. I believe that the recommended songs would be enjoyable to the listener, since the genre, mood, and energy match well.

---

## 6. Limitations and Bias 

Energy dominates every ranking. Songs that are related get a score of 0 - same as a completely irrelevant song. There are unused features that do not contribute to the score (e.g. valence, avousticness, danceability). Mood vocabulary is very narrow and too specific.

---

## 7. Evaluation  

One of the bug tests I and Claude made was the test for acoustic importance. When making tests, I realized that the score function does not include the acoustic feature of the song. Then there are related genres that do not match, for example pop and happy never match, even though they are closely related.

---

## 8. Future Work  

The dataset definitely needs to be bigger next time I do a project like this. I will try to include as many song features as I can to please the listener.

---

## 9. Personal Reflection  

I always blamed youtube algorithms for recommending me certain questionable things, but now I see how complicated it might be. Behind the scenes, there is much more going on, especially in professional-grade code of corporations like google and apple. There is a ton of information to process, and now that I think about it, the recommendation algorithms can be pretty accurate which is amazing.