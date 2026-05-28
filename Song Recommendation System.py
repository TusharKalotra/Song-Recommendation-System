import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


CLIENT_ID = '6c4b79ea191444f6ad815077d1b8e5e6' 
CLIENT_SECRET = '5da09b2ff4904fbe90f1df4e828384a3'  


client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

mood_features = {
    "happy": {"danceability": 0.7, "energy": 0.8},
    "sad": {"danceability": 0.3, "energy": 0.3},
    "energetic": {"danceability": 0.8, "energy": 0.9},
    "romantic": {"danceability": 0.5, "energy": 0.6},
    "chill": {"danceability": 0.4, "energy": 0.5},
    "party": {"danceability": 0.9, "energy": 0.9}
}


def recommend_songs_by_mood(mood):
    mood = mood.lower()

  
    if mood not in mood_features:
        return [f"Invalid mood: {mood}. Try one of the following: {', '.join(mood_features.keys())}."]
    
    mood_feature = mood_features[mood]
    
    try:
      
        results = sp.recommendations(
            seed_genres=["pop", "rock"],  
            limit=5,
            target_danceability=mood_feature["danceability"],
            target_energy=mood_feature["energy"]
        )

       
        songs = [track["name"] for track in results['tracks']]
        return songs
    except Exception as e:
        return [f"Error fetching recommendations: {str(e)}"]


def recommend_songs_by_artist(artist_name):
    try:
      
        result = sp.search(q='artist:' + artist_name, type='artist', limit=1)
        if not result['artists']['items']:
            return [f"Artist {artist_name} not found. Please check the name and try again."]
        
        artist_id = result['artists']['items'][0]['id']
        
        top_tracks = sp.artist_top_tracks(artist_id)['tracks']
        
     
        songs = [track["name"] for track in top_tracks]
        return songs
    except Exception as e:
        return [f"Error fetching top tracks: {str(e)}"]


def main():
    print("Welcome to the Song Recommendation System!\n")
    choice = input("Do you want recommendations based on mood or artist? (Enter 'mood' or 'artist'): ").strip().lower()

    if choice == 'mood':
        mood = input("Enter your mood (happy, sad, energetic, romantic, chill, party): ").strip().lower()
        recommended_songs = recommend_songs_by_mood(mood)
        print("\nRecommended Songs for your Mood:")
        for song in recommended_songs:
            print(song)

    elif choice == 'artist':
        artist_name = input("Enter the artist's name: ").strip()
        recommended_songs = recommend_songs_by_artist(artist_name)
        print(f"\nTop 10 Songs by {artist_name}:")
        for song in recommended_songs:
            print(song)

    else:
        print("Invalid choice! Please enter 'mood' or 'artist'.")

if __name__ == "__main__":
    main()
