# Musicloud

A Streamlit-based music recommendation system with playlist and event management features.  
Users can recommend songs, add them to playlists, manage events, participate in events, and even delete events with a live UI.

---

## Features

- 🎵 **Music Recommender** — Get song recommendations with album covers using Spotify API.
- 🎶 **Playlist Management** — View, add, and clear playlists.
- 📅 **Event Management** — Add events, participate in events, view participants, increase capacity dynamically, and delete events.


## Project Structure

```
├── app.py # Main Streamlit application
├── data_cleaning.py # Data cleaning and preprocessing script
├── df.pkl # Preprocessed dataset
├── similarity.pkl # Similarity matrix
├── playlists.json # Playlist storage
├── events.json # Events storage
├── .env # Environment variables for Spotify API keys
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```