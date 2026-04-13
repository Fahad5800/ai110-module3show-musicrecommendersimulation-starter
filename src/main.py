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

    profiles = {
        # --- Standard profiles ---
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "target_valence": 0.8,
            "target_tempo_bpm": 120,
            "target_danceability": 0.8,
            "target_acousticness": 0.2,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.4,
            "target_valence": 0.6,
            "target_tempo_bpm": 78,
            "target_danceability": 0.55,
            "target_acousticness": 0.75,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.9,
            "target_valence": 0.4,
            "target_tempo_bpm": 150,
            "target_danceability": 0.65,
            "target_acousticness": 0.1,
            "likes_acoustic": False,
        },
        # --- Adversarial / edge-case profiles ---
        # Conflicting: max energy but sad mood — tests whether audio score overrides mood penalty
        "High-Energy but Sad": {
            "favorite_genre": "rock",
            "favorite_mood": "sad",
            "target_energy": 0.95,
            "target_valence": 0.2,
            "target_tempo_bpm": 155,
            "target_danceability": 0.6,
            "target_acousticness": 0.1,
            "likes_acoustic": False,
        },
        # Conflicting: acoustic preference but dance-floor tempo — tests acoustic bonus vs. tempo mismatch
        "Acoustic Dance": {
            "favorite_genre": "folk",
            "favorite_mood": "happy",
            "target_energy": 0.7,
            "target_valence": 0.8,
            "target_tempo_bpm": 128,
            "target_danceability": 0.9,
            "target_acousticness": 0.9,
            "likes_acoustic": True,
        },
        # Impossible genre: no songs in catalog match — tests graceful fallback to audio features
        "Unknown Genre": {
            "favorite_genre": "bossa nova",
            "favorite_mood": "relaxed",
            "target_energy": 0.45,
            "target_valence": 0.65,
            "target_tempo_bpm": 95,
            "target_danceability": 0.6,
            "target_acousticness": 0.8,
            "likes_acoustic": True,
        },
    }

    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * 80)
        print(f"  PROFILE: {profile_name}")
        print("=" * 80)
        print(f"Genre: {user_prefs['favorite_genre'].title()} | Mood: {user_prefs['favorite_mood'].title()}")
        print("=" * 80 + "\n")

        for i, rec in enumerate(recommendations, 1):
            # Unpack: (song, score, explanation)
            song, score, explanation = rec
            print(f"{i}. {song['title']} by {song['artist']}")
            print(f"   Genre: {song['genre']} | Mood: {song['mood']}")
            print(f"   Score: {score:.2f}/5.0")
            print(f"   Match: {explanation}")
            print()


if __name__ == "__main__":
    main()
