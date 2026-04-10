"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Define a specific taste profile for comparisons
    # This represents a user who likes upbeat, happy pop music with electronic production
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,           # High energy (0.0-1.0)
        "target_valence": 0.8,          # Positive/happy tone (0.0-1.0)
        "target_tempo_bpm": 120,        # Upbeat tempo in BPM
        "target_danceability": 0.8,     # Groovy and danceable (0.0-1.0)
        "target_acousticness": 0.2      # Mostly electronic, not acoustic (0.0-1.0)
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "="*80)
    print("🎵  MUSIC RECOMMENDER RESULTS  🎵")
    print("="*80)
    print(f"Profile: {user_prefs['favorite_genre'].title()} + {user_prefs['favorite_mood'].title()}")
    print("="*80 + "\n")
    
    for i, rec in enumerate(recommendations, 1):
        # Unpack: (song, score, explanation)
        song, score, explanation = rec
        print(f"{i}. {song['title']} by {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"   ⭐ Score: {score:.2f}/5.0")
        print(f"   ✓ Match: {explanation}")
        print()


if __name__ == "__main__":
    main()
