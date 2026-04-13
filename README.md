# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version (MoodElevator x18) scores each song out of 5.0 points using a content-based approach: +2.0 for genre match, +1.0 for mood match, up to +2.0 for audio similarity across energy, valence, danceability, and tempo, and a small acoustic preference bonus. It runs six user profiles — three standard and three adversarial — against an 18-song catalog, then prints the top 5 ranked recommendations with scores and match explanations for each profile.

---

## How The System Works

Explain your design in plain language.

- Real-world music recommenders like Spotify use a mix of collaborative filtering—analyses, often what users listen to, and content-based filtering, matching song attributes to user preferences. My version prioritizes a simple content-based approach, focusing on features like genre, mood, energy, valence, tempo, danceability, and acousticness to recommend songs that match the user's desired "vibe," emphasizing musical similarity over social trends.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

  Answers:
- Each song in the system uses metadata (id, title, artist), categories (genre, mood) and audio features (energy, tempo_bpm, valence etc)
- My user profile stores genre, mood, energy, valence, danceability, tempo, and acoustic preference. 
- For each song, my 'Recommender' uses the following logic: 
  - +2.0 for genre match
  - +1.0 for mood match
  - 0-2.0 for audio similarity (weighted across 4 features)
  - +0.5/+0.3 acoustic preference bonuses
  - Total range: 0.0 to 5.0 points
- My system scores all songs individually and then based on that scores makes a list of song sorted by the scores. After getting a list of songs for a user, it returns top 5 (default) songs. 



---

## Sample Output

Here is the full terminal output across all profiles:

![Music Recommender Terminal Output](assets/Music%20Recommender%20Terminal.png)

---

### High-Energy Pop

![High-Energy Pop results](assets/High%20Energy%20Pop.png)

"Sunrise City" ranks first because it matches both genre and mood.

---

### Chill Lofi

![Chill Lofi results](assets/Chill%20Lofi.png)

Midnight Coding ranks first because it matches genre, mood, and energy almost exactly. The Chill Lofi profile benefits from having three lofi songs in the catalog, making it the best-served profile — all top three results are genre matches.

---

### Deep Intense Rock

![Deep Intense Rock results](assets/Deep%20Intense%20Rock.png)

Storm Runner ranks first with a rock genre match and one of the highest energy levels in the catalog. The profile is well-served because high energy, low valence, and fast tempo all align tightly with the available rock and metal songs.

---

### High-Energy but Sad *(adversarial)*

![High-Energy but Sad results](assets/High%20Energy%20Sad.png)

Storm Runner still ranks first by rock genre and energy match. No sad, high-energy song exists in the catalog, so the system can never fully satisfy this profile's mood request. This is a catalog gap, not a scoring flaw — the logic is working correctly but the data cannot fulfill the request.

---

### Acoustic Dance *(adversarial)*

![Acoustic Dance results](assets/Acoustic%20Dance.png)

No folk song in the catalog is also highly danceable, so the system compromises: high-danceability songs rank above Folk Tales despite the genre match, because danceability and energy dominate the audio score over the acoustic bonus. When user preferences conflict internally, audio features win over categorical matches.

---

### Unknown Genre *(adversarial)*

![Unknown Genre results](assets/Unknown%20Genre.png)

With no bossa nova songs in the catalog, the system earns zero genre points for every song and ranks entirely on audio similarity and acoustic preference. Coffee Shop Stories (jazz, relaxed) rises to #1 because its energy and acousticness happen to align with the target values — a graceful fallback, but not a true match.

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments That I Tried

**Experiment 1 — Weight shift: doubled energy weight, halved genre bonus**

Changed the genre bonus from +2.0 to +1.0 and doubled the energy weight inside the audio similarity formula (from 0.4 to 0.8). Then compared all six profiles side by side. The Chill Lofi profile barely changed because its top songs matched both genre and energy. The High-Energy but Sad profile shifted significantly — Storm Runner stayed #1 but several mood-matched, low-energy songs that previously ranked in the top 3 dropped to #4 and #5, replaced by high-energy songs that had no mood match. This confirmed that the original genre weight of +2.0 was doing a lot of quiet work to surface mood-matched songs for adversarial profiles.

**Experiment 2 — Adding valence and danceability to the audio score**

The original starter only scored energy. After adding valence (emotional tone) and danceability as weighted features, the Acoustic Dance profile changed the most: previously, high-danceability pop songs dominated because only energy was measured; after adding danceability explicitly, Folk Tales (folk, low danceability) dropped further while Rooftop Lights (high danceability) stayed near the top. This showed that adding more features does not always help the user — it can expose contradictions in the profile itself.

**Experiment 3 — Running all six profiles, including three adversarial**

The three adversarial profiles (High-Energy but Sad, Acoustic Dance, Unknown Genre) were designed to expose edge cases. In all three cases the scoring logic itself did not break — it returned results and scores — but the results revealed catalog gaps rather than algorithm bugs. The biggest insight was that adversarial profiles stress-test the data more than the code.

---

## Limitations and Risks

- It only works on a catalog of 18 songs, so any genre represented by just one song (rock, jazz, hip-hop) gives almost no room to rank within that genre.
- It does not understand lyrics, language, song duration, or artist popularity — features that matter significantly to real users.
- Genre overfits: the +2.0 genre bonus can fully override a poor audio match, meaning a song in the right genre but wrong mood or energy can outrank a nearly perfect audio match in the wrong genre.
- The catalog skews toward western, English-language music and does not reflect global musical diversity — users whose taste falls outside that range get weaker recommendations.
- The acoustic preference bonus is asymmetric (+0.5 for acoustic lovers vs. +0.3 for non-acoustic), which gives a small but consistent scoring advantage to users who prefer acoustic music.
- All users are treated as independent — there is no collaborative filtering, so the system cannot learn that users with similar genre preferences also tend to enjoy the same mood combinations.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this system taught me that a recommender is just a scoring function dressed up as intelligence. Every recommendation is the result of arithmetic — points assigned to features like genre and energy — not any real understanding of what music feels like. What surprised me most was how much catalog size mattered more than scoring logic. The "High-Energy but Sad" profile did not fail because the math was wrong; it failed because no sad, high-energy song existed in the data. The model was working correctly but the data could not fulfill the request. That mirrors how real systems work: no matter how good the algorithm, it can only recommend what exists in the catalog.

Building this also made bias much more concrete. The lofi profile gets three genre matches in the top five while most other genres only get one — not because the scoring favors lofi users intentionally, but because the catalog happened to include more lofi songs. That is exactly how real-world bias creeps in: a dataset skewed toward certain genres, moods, or cultures quietly advantages users whose taste fits the overrepresented categories. The acoustic preference bonus is also slightly asymmetric — acoustic lovers get +0.5 while non-acoustic users only get +0.3 — a small design choice that would compound across millions of users in a real product. These are not bugs, they are the result of decisions made during design that embed assumptions about whose taste matters most.

---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

> MoodElevator x18

---

## 2. Intended Use

> This model suggests top 5 songs from an 18-song catalog based on a user's preferred genre, mood, energy, valence, danceability, tempo, and acoustic preference. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Each song carries category labels (genre and mood) and four audio measurements: energy, valence, danceability, and tempo. Each user profile stores a favorite genre, favorite mood, and matching target values for those same audio features. The system scores every song out of 5.0 points — 2 points for a genre match, 1 for a mood match, up to 2 for audio similarity across energy, valence, danceability, and tempo (energy weighted most heavily at 40%), and a small bonus of 0.3–0.5 for acoustic preference alignment. Songs are ranked by score and the top 5 are returned.

---

## 4. Data

- The catalog contains 18 songs across 15 genres (pop, lofi, rock, metal, jazz, electronic, synthwave, ambient, indie pop, classical, hip-hop, country, folk, R&B, reggae) and 13 moods (happy, chill, intense, relaxed, focused, moody, sad, energetic, nostalgic, melancholic, peaceful, groovy, uplifting).
- No songs were added or removed from the original dataset.
- The data is skewed toward western, English-language music and does not reflect the full range of global musical taste. Genres like lofi have 3 songs while most others have only 1.

---

## 5. Strengths

- The Chill Lofi profile consistently gets 3 genre-matched songs in its top 5 because the catalog has 3 lofi entries — the strongest genre coverage of any profile.
- Sunrise City ranking #1 for High-Energy Pop, Storm Runner ranking #1 for Deep Intense Rock, and Midnight Coding ranking #1 for Chill Lofi all felt immediately correct. Genre + mood alignment drove those results exactly as intended.
- The scoring is fully transparent — every recommendation comes with a numeric score and a plain-text explanation of why each song ranked where it did, which makes the system easy to audit and understand.

---

## 6. Limitations and Bias

- The catalog is too small: genres with only 1 song (rock, jazz, hip-hop) give almost no room to rank within that genre.
- The genre weight (+2.0) can fully override a poor audio match, meaning a wrong-energy song in the right genre can outrank a near-perfect audio match in the wrong genre.
- The lofi profile gets 3 genre matches while most profiles only get 1 — an unintentional catalog-size bias that advantages certain users.
- The acoustic bonus is asymmetric (+0.5 for acoustic, +0.3 for non-acoustic), giving a quiet but consistent scoring edge to acoustic-preferring users.
- All users are treated as independent with a single fixed taste shape — no listening history, no context (workout vs. sleep), and no collaborative signal from other users.
- If used in a real product, the western-music catalog bias would systematically underserve users whose taste lies outside it.

---

## 7. Evaluation

- All 6 profiles were tested: High-Energy Pop, Chill Lofi, Deep Intense Rock, and three adversarial profiles (High-Energy but Sad, Acoustic Dance, Unknown Genre).
- For each profile I checked whether the #1 result matched the expected genre and mood and whether the score breakdown explained the ranking intuitively.
- A weight-shift experiment was run: genre bonus halved to +1.0 and energy weight doubled. All 6 profiles were compared side by side before and after to see which rankings changed and by how much.
- The most revealing finding came from the adversarial profiles: in every case the scoring logic was working correctly, but the data could not fulfill the request — exposing catalog gaps rather than algorithm bugs.

---

## 8. Future Work

- Add listening context (workout, study, sleep) as a separate preference dimension so the same user can get different recommendations depending on what they are doing.
- Introduce a diversity penalty so the top 5 cannot all come from the same genre or artist — currently Midnight Coding and Library Rain can trade the #1 and #2 spots for Chill Lofi because they are nearly identical songs.
- Replace single target values with preference ranges (e.g., energy between 0.6 and 0.8) to better capture the natural variation in human taste.
- Add a "recently played" filter to avoid recommending the same artist twice in a session.
- Surface explicit trade-off explanations when no genre match exists, such as "No bossa nova found — ranked by audio similarity instead."

---

## 9. Personal Reflection

Building this made bias feel concrete rather than abstract. The lofi profile getting three genre matches while rock gets one is not a bug — it is the direct result of a catalog that happened to include more lofi songs. That is exactly how real-world recommender bias works: quiet, unintentional, and invisible unless you run adversarial profiles that expose it. The asymmetric acoustic bonus (+0.5 vs +0.3) is another example — a small design choice that would compound silently across millions of users in a real product.

The most surprising thing was how little the scoring logic mattered compared to the catalog. The "High-Energy but Sad" profile did not fail because the math was wrong; it failed because no sad, high-energy song existed. Human judgment still matters here because no algorithm can decide which gaps in the data are worth filling, or whose musical taste deserves better representation. Those are values questions, not math questions, and they have to be answered before the model is ever trained.

---

## Engineering Process Reflection

**Biggest learning moment**

This project was filled with learning moments. The biggest one was regarding the understanding of how models like mood recognition, recommenders, and similar models works. It basically works on a scoring system that can reflects a mathematical equation. 

**Using AI tools — where they helped and where I double-checked**

AI tools were most useful for scaffolding the scoring structure quickly — setting up the weighted audio similarity formula and the normalization for tempo BPM saved significant time. Where I needed to double-check was in the weight values themselves. The initial energy weight of 0.4 and genre bonus of +2.0 felt reasonable on paper, but they only made sense after running all six profiles and observing that the genre bonus was quietly overriding bad audio matches. No tool could validate that for me — it required reading the actual ranked output and asking whether the number matched the intuition.

**Why simple algorithms still "feel" like recommendations**

What surprised me most is how little complexity is needed to produce results that feel personalized. A handful of weighted comparisons against a user's stated preferences is enough to make the output feel like it "knows" you — especially when genre and mood align. The system has no memory, no learning, and no understanding of music at all. It is just arithmetic. But because the features it uses (genre, mood, energy) map closely to how people naturally describe their taste, the output lands in a familiar place. That gap between what the system is doing and what it feels like it is doing is exactly what makes AI systems hard to reason about at scale.

**What I would try next**

The change I most want to make is replacing single target values with preference ranges. Saying a user wants energy between 0.6 and 0.8 is far more realistic than a fixed target of 0.75, and it would stop penalizing songs that are "close enough." After that, I would add a diversity constraint so the top 5 cannot all cluster around the same genre and energy level — the current system optimizes for similarity, but real recommendation feels better when the list has some variety in it.

