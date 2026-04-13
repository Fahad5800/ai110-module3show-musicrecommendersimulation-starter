# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---
Name: MoodElevator x18

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---
- It generates a ranked list of top 5 songs from a small dataset based on user's prefernce. 
- One energy target describes the user fully, it does not look for the context. Also, most users are treated as independant users with no influence from what other user listen to.
- This is strictly for classroom exploration. The data is small, plus it does not automatically tain itself from real world data.


## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

Every song in the catalog carries two kinds of information: category labels (its genre like "pop" or "rock", and its mood like "happy" or "intense") and audio measurements (how energetic it sounds on a 0–1 scale, how fast the tempo is, how emotionally positive it feels, how danceable it is, and how acoustic versus electronic it sounds).

Every user has a matching set of preferences: a favorite genre, a favorite mood, a target energy level, and targets for valence, danceability, tempo, and whether they prefer acoustic sounds.

When a user asks for recommendations, the system gives every song in the catalog a score out of 5.0 points using three layers of comparison:

1. **Genre check (0 or 2 points):** If the song's genre matches the user's favorite genre, it gets 2 points. If not, it gets nothing. This is the biggest single factor — it acts like a hard filter that rewards songs in the right category.

2. **Mood check (0 or 1 point):** If the song's mood matches the user's favorite mood, it gets 1 point. A match here is meaningful but not enough on its own to beat a song with a strong audio score.

3. **Audio similarity (0 to 2 points):** The system measures how close the song's energy, emotional positivity, danceability, and tempo are to the user's targets. Energy counts the most (40% of this portion), then emotional tone (25%), danceability (20%), and tempo (15%). A perfect match across all four gives the full 2 points; a complete mismatch gives 0.

4. **Acoustic bonus (0, 0.3, or 0.5 points):** If the user likes acoustic music and the song is highly acoustic, it gets a small bonus of 0.5 points. If the user prefers non-acoustic sounds and the song is clearly electronic, it gets a 0.3 bonus.

After all songs are scored, they are sorted from highest to lowest and the top 5 are returned. The starter logic only used energy; this version adds valence, danceability, and tempo as additional audio features with individual weights, making the audio comparison more nuanced.

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---
- Total songs = 18
- Genres: pop, lofi, rock, metal, jazz, electronic, synthwave, ambient, indie pop, classical, hip-hop, country, folk, R&B, reggae. Total of 15 genres for 18 songs. while, Moods: happy, chill, intense, relaxed, focused, moody, sad, energetic, nostalgic, melancholic, peaceful, groovy, uplifting — 13 distinct moods.
- Data is not altered.
- Yes, the dataset skews more towards western, english music. This does not reflect the full range of global cutural music. 

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---
- Users whose genres exist multiple times in the catalog benefits more then others. Chill Lofi consistently gets 3 genre matched songs in their top 5 songs.
- The system correctly captures the idea that genre is the strongest parameter. The acoustic bonus also works very well, as it correctly seperates acoustic loving profiles from non-acoustic profiles. 
- Sunrise City ranking #1 for High-Energy Pop felt exactly right, Storm Runner ranking #1 for both Deep Intense Rock and High-Energy but Sad made sense, and Midnight Coding and Library Rain trading #1 and #2 for Chill Lofi felt very intutive. 

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---
- It does not cover lyrics, language, song duration, and artists popularity.
- Genres like rock, jazz, hip-hop etc are only tied to 1 song each. 
- Genre overfits more than energy. With +2.0 score it can override a poor audience match entirely. 
- Lofi users get 3 genre matches while the most of the rest reflects only 1 genre match. Acoustic users get +0.5 bonus while non-acoustic users shows +0.3 score. 

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---
- All 6 profiles, which includes High-Energy Pop, Chill Lofi, Deep Intense Rock, High-Energy but Sad, Acoustic Dance, and Unknown Genre, are tested. The last 3 were adversarial.
- I checked whther top songs matches genre and mood for our profiles. Further, I checked high-energy songs, unknown genre profile, and acoustic dance profile.
- The "High Energy but Sad" profile originally Midnight Whispers ranked at #3, which had energy = 0.22. This was contradicting because it revealed that mood match was overriding audio reality.
- Ran a weight shifting experiment that doubled the energy weight and halved genre bonus. After that compared all of the 6 profiles side by side.

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---
- Listning context like sleeping, work out, and studying must be added. Also, a recently played list should be added to avoid recommending same artist repeatedly.
- A warning should be highlighted when no genre matches. System trade offs should also be highlighted like "Energy matched but not your mood".
- Currently the top 5 can be nearly identical songs (Midnight Coding and Library Rain score almost the same for Chill Lofi). A diversity penalty could push the 2nd result to be from a different genre or artist than #1
- Instead of target value, a range can be added to reflect users taste better. Additionally, weight preferences should be changed based on user's taste.
## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
---
- Recommender systems works on the basis of scores. These scores reflects users behavior. By carfully analyzing user's behaviour, model can be trained to for better recommendations. 
- The most surprising thing was how much catalog size mattered more than scoring logic. The "High-Energy but Sad" profile did not fail because the scoring was wrong — it failed because no sad, high-energy song existed in the data.
- The real life music recommender app are trained on millions of parameters. Each chosen carefully to reflect the diverse taste of human beings. Our small model that is only trained on subset of real world parameters urged me to think beyond just an music recommender apps. All smart models follows the same pattern. 
