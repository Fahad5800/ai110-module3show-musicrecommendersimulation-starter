# Profile Comparison Reflections

## High-Energy Pop vs. Chill Lofi

These two profiles sit at opposite ends of the energy spectrum. The High-Energy Pop user targets energy=0.8, genre=pop, mood=happy — and the system correctly surfaces Sunrise City (pop, happy, energy=0.82) at #1 with a score of 4.26. The Chill Lofi user targets energy=0.4, genre=lofi, mood=chill — and gets Midnight Coding (lofi, chill, energy=0.42) at #1 with 4.45. Both top results are nearly perfect matches, which validates that when genre, mood, and energy all align, the scoring works as intended. The key difference is that the Chill Lofi profile benefits from having 3 lofi songs in the catalog, so its top 3 are all strong genre matches. The pop profile only gets 2 pop songs before falling back to audio similarity — showing how catalog size per genre directly affects recommendation quality.

---

## Deep Intense Rock vs. High-Energy but Sad

These two profiles share the same genre (rock) and nearly the same energy target (0.9 vs. 0.95), but differ in mood — intense vs. sad. Both rank Storm Runner #1 because it matches rock genre and high energy. The difference appears at #3: Deep Intense Rock gets Gym Hero (pop, intense, mood match) while High-Energy but Sad drops Gym Hero lower because there is no mood match to "sad". The system correctly pushes sadness-adjacent songs down when energy is the dominant signal, but it never surfaces any truly sad high-energy song because none exists in the catalog. This shows that adversarial profiles expose catalog gaps more than scoring flaws — the logic is working, but the data cannot fulfill the request.

---

## Acoustic Dance vs. Unknown Genre

Both are adversarial profiles with no clean match available. Acoustic Dance asks for folk genre + high danceability + acoustic preference — a combination that does not exist in the catalog. The system compromises: Folk Tales (folk, acoustic) ranks #3 on genre+acoustic bonus, but mood-happy songs like Rooftop Lights and Sunrise City rank higher because danceability and energy dominate the audio score. This reveals that when preferences conflict internally, the audio features win over categorical matches. Unknown Genre (bossa nova) gets zero genre points for any song, so the entire ranking is driven by audio similarity and mood match alone. Coffee Shop Stories (jazz, relaxed) rises to #1 not because it is close to bossa nova, but because its energy and acousticness happen to align with the target values. Both profiles demonstrate that the system degrades gracefully — it still returns reasonable-sounding songs — but the reason it picks them shifts from explicit preference to numeric proximity.
