"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print("\n" + "=" * 50)
    print(f"  {label}")
    print(f"  Prefs: {user_prefs}")
    print("=" * 50)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{i}. {song['title']} by {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']} | Acoustic: {song['acousticness']}")
        print(f"   Score: {score:.2f} / 3.00")
        print(f"   Why:")
        for reason in explanation.split(", "):
            print(f"     - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # ── BASELINE ────────────────────────────────────────────────────────────────
    # Standard usage: genre + mood + energy all provided.
    print_recommendations(
        "BASELINE: pop + happy + 0.8 energy",
        {"genre": "pop", "mood": "happy", "energy": 0.8},
        songs,
    )

    # ── BUG PROBE 1: likes_acoustic is silently ignored ──────────────────────────
    # UserProfile has a likes_acoustic field, but score_song never uses it.
    # Both profiles below should get different results — but they won't.
    # Expectation: acoustic songs rank higher for the acoustic lover.
    # Reality: scores are identical; likes_acoustic has zero effect.
    print_recommendations(
        "BUG 1a: Acoustic lover (likes_acoustic=True has no effect)",
        {"genre": "folk", "mood": "relaxed", "energy": 0.35, "likes_acoustic": True},
        songs,
    )
    print_recommendations(
        "BUG 1b: Same prefs but likes_acoustic=False — should rank differently, won't",
        {"genre": "folk", "mood": "relaxed", "energy": 0.35, "likes_acoustic": False},
        songs,
    )

    # ── BUG PROBE 2: energy out of range causes negative scores ──────────────────
    # energy_similarity = 1.0 - abs(user_energy - song_energy)
    # If user energy > 1.0, high-energy songs receive a NEGATIVE contribution.
    # Songs with energy closest to the user's inflated value "win" by losing less.
    # Expectation: high-energy songs rank #1 for an "ultra-high energy" user.
    # Reality: every song gets penalised; the lowest-energy songs suffer most.
    print_recommendations(
        "BUG 2a: Energy = 1.5 (above valid range — negative scores expected)",
        {"genre": "rock", "mood": "intense", "energy": 1.5},
        songs,
    )
    print_recommendations(
        "BUG 2b: Energy = -0.5 (below valid range — high-energy songs penalised)",
        {"genre": "lofi", "mood": "chill", "energy": -0.5},
        songs,
    )

    # ── BUG PROBE 3: case-sensitive string matching ──────────────────────────────
    # genre and mood comparisons use ==, so "Pop" never matches "pop".
    # Expectation: same results as the baseline.
    # Reality: genre contributes 0 to every song's score.
    print_recommendations(
        "BUG 3: Capitalised genre/mood — 'Pop'/'Happy' never match catalog values",
        {"genre": "Pop", "mood": "Happy", "energy": 0.8},
        songs,
    )

    # ── BUG PROBE 4: impossible genre+mood combination ───────────────────────────
    # No song in the catalog is both genre=lofi AND mood=intense.
    # No song will ever reach the maximum score of 3.0.
    # The recommender silently returns its best guesses with no warning.
    print_recommendations(
        "BUG 4: Impossible combo — no lofi+intense song exists in catalog",
        {"genre": "lofi", "mood": "intense", "energy": 0.9},
        songs,
    )

    # ── BUG PROBE 5: energy-only profile (genre/mood omitted) ────────────────────
    # When genre and mood are missing, score_song falls through those checks
    # (get() returns None, which never equals a song value).
    # The entire ranking is driven solely by energy proximity.
    # Expectation: a musically coherent recommendation.
    # Reality: pure arithmetic — the closest-energy song wins regardless of fit.
    print_recommendations(
        "BUG 5: Energy-only prefs — genre/mood omitted, ranking is pure proximity",
        {"energy": 0.5},
        songs,
    )

    # ── BUG PROBE 6: ignored audio features (valence, danceability, tempo) ───────
    # valence, danceability, and tempo_bpm are loaded from the CSV but never
    # factored into score_song. Two users with opposite preferences for these
    # dimensions will receive identical recommendations.
    print_recommendations(
        "BUG 6a: High-valence / high-danceability user (these prefs are ignored)",
        {"genre": "electronic", "mood": "energetic", "energy": 0.9,
         "valence": 0.95, "danceability": 0.95, "tempo_bpm": 160},
        songs,
    )
    print_recommendations(
        "BUG 6b: Same genre/mood/energy but low valence/danceability — should differ, won't",
        {"genre": "electronic", "mood": "energetic", "energy": 0.9,
         "valence": 0.10, "danceability": 0.10, "tempo_bpm": 80},
        songs,
    )

    # ── BUG PROBE 7: mood label mismatch — 'energetic' vs 'intense' ─────────────
    # The catalog uses both "energetic" (Neon Pulse) and "intense" (Storm Runner,
    # Gym Hero, Metal Frenzy) as distinct mood labels. A user who intuitively
    # types "energetic" expecting to match "intense" songs (or vice versa) gets
    # an incomplete result — no cross-label matching exists.
    print_recommendations(
        "BUG 7a: mood='energetic' — only Neon Pulse matches; intense songs are missed",
        {"genre": "electronic", "mood": "energetic", "energy": 0.9},
        songs,
    )
    print_recommendations(
        "BUG 7b: mood='intense' — misses Neon Pulse entirely despite similar feel",
        {"genre": "rock", "mood": "intense", "energy": 0.9},
        songs,
    )

    # ── BUG PROBE 8: tie-breaking is arbitrary (stable sort on CSV order) ────────
    # When two songs have the same score, their relative order depends on their
    # position in the CSV file. There is no secondary sort key (e.g., popularity,
    # recency), so the "winner" between tied songs is effectively random.
    print_recommendations(
        "BUG 8: Tie-breaker — genre/mood that matches multiple songs equally",
        {"genre": "lofi", "mood": "chill", "energy": 0.385},  # midpoint of 0.42 and 0.35
        songs,
    )


if __name__ == "__main__":
    main()
