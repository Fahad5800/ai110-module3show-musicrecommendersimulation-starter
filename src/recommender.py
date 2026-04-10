from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns as list of dictionaries.
    Required by src/main.py
    """
    songs = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields to float
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness'])
                }
                songs.append(song)
        print(f"Loaded {len(songs)} songs from {csv_path}")
        return songs
    except FileNotFoundError:
        print(f"Error: File {csv_path} not found.")
        return []

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Comprehensive scoring using categorical matches and multi-feature audio similarity.
    +2.0 points for genre match
    +1.0 point for mood match
    0-2.0 points for audio similarity (energy, valence, danceability, tempo)
    +0.5 bonus for acoustic preference match
    Returns: (score, list of match reasons)
    """
    reasons = []
    score = 0.0

    # Genre match: +2.0 points (highest priority)
    if song['genre'] == user_prefs.get('favorite_genre'):
        score += 2.0
        reasons.append(f"Genre match: {song['genre']}")

    # Mood match: +1.0 point (moderate priority)
    if song['mood'] == user_prefs.get('favorite_mood'):
        score += 1.0
        reasons.append(f"Mood match: {song['mood']}")

    # Multi-feature audio similarity: 0-2.0 points
    target_energy = user_prefs.get('target_energy', 0.5)
    target_valence = user_prefs.get('target_valence', 0.5)
    target_danceability = user_prefs.get('target_danceability', 0.5)
    target_tempo = user_prefs.get('target_tempo_bpm', 120)

    # Normalize tempo to 0-1 range (assuming 60-180 BPM typical range)
    tempo_normalized = max(0, min(1, (target_tempo - 60) / 120))
    song_tempo_normalized = max(0, min(1, (song['tempo_bpm'] - 60) / 120))

    # Calculate similarities for each feature
    energy_sim = 1.0 - abs(song['energy'] - target_energy)
    valence_sim = 1.0 - abs(song['valence'] - target_valence)
    danceability_sim = 1.0 - abs(song['danceability'] - target_danceability)
    tempo_sim = 1.0 - abs(song_tempo_normalized - tempo_normalized)

    # Weighted combination (energy most important, others balanced)
    weights = {
        'energy': 0.4,      # 40% - most important for user preference
        'valence': 0.25,    # 25% - emotional tone
        'danceability': 0.2, # 20% - rhythm/groove
        'tempo': 0.15       # 15% - speed/pacing
    }

    audio_similarity = (
        weights['energy'] * energy_sim +
        weights['valence'] * valence_sim +
        weights['danceability'] * danceability_sim +
        weights['tempo'] * tempo_sim
    )

    # Scale to 0-2.0 points range
    audio_score = audio_similarity * 2.0
    score += audio_score

    # Acoustic preference bonus: +0.5 if user likes acoustic and song is acoustic
    likes_acoustic = user_prefs.get('likes_acoustic', False)
    if likes_acoustic and song['acousticness'] > 0.7:
        score += 0.5
        reasons.append("Acoustic preference match")
    elif not likes_acoustic and song['acousticness'] < 0.3:
        score += 0.3  # Smaller bonus for matching non-acoustic preference
        reasons.append("Non-acoustic preference match")

    # Add explanations for strong audio matches
    if audio_similarity > 0.8:
        reasons.append("Excellent overall vibe match")
    elif audio_similarity > 0.6:
        reasons.append("Good overall vibe match")
    elif audio_similarity > 0.4:
        reasons.append("Decent vibe match")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores all songs and returns top k recommendations ranked by score.
    Returns: List of (song_dict, score, explanation_string)
    """
    scored_songs = []
    
    # Score each song
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "Similar vibe detected"
        scored_songs.append((song, score, explanation))
    
    # Sort by score (descending) and return top k
    ranked = sorted(scored_songs, key=lambda x: x[1], reverse=True)
    return ranked[:k]
