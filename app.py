import os
import joblib
import requests
from dotenv import load_dotenv
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from datetime import datetime


# URLs for .pkl files

URL_DF = "https://drive.google.com/uc?export=download&id=1CRDB401zws9N7lLycOrXzOSDH7GSuLZS"
URL_SIMILARITY = "https://drive.google.com/uc?export=download&id=1vA4AeZu8eTLc6b1H1aCiOS32WLT4a47A"


# Download function

def download_file(url, local_path):
    if not os.path.exists(local_path):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(local_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        else:
            st.error(f"Failed to download {local_path}")
            st.stop()

download_file(URL_DF, "df.pkl")
download_file(URL_SIMILARITY, "similarity.pkl")

if not os.path.exists("df.pkl") or not os.path.exists("similarity.pkl"):
    st.error("Required model files not downloaded.")
    st.stop()

music = joblib.load("df.pkl")
similarity = joblib.load("similarity.pkl")
music_list = music['song'].values



# Load environment variables

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    st.error("⚠ CLIENT_ID and CLIENT_SECRET not found in .env file")
    st.stop()


# Spotify Client

client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Music Recommender Functions

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track", limit=1)
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        return track["album"]["images"][0]["url"]
    return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    names, posters = [], []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        names.append(music.iloc[i[0]].song)
    return names, posters


# Playlist Functions

PLAYLIST_FILE = "playlists.json"

def load_playlist():
    try:
        with open(PLAYLIST_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_playlist(playlist):
    with open(PLAYLIST_FILE, "w") as f:
        json.dump(playlist, f, indent=4)

def add_to_playlist(song_name, artist_name):
    playlist = load_playlist()
    playlist.append({"song": song_name, "artist": artist_name})
    save_playlist(playlist)
    st.session_state["playlist"] = load_playlist()

def remove_from_playlist(index):
    playlist = load_playlist()
    if 0 <= index < len(playlist):
        playlist.pop(index)
        save_playlist(playlist)
        st.session_state["playlist"] = load_playlist()


# Event Management Functions

EVENT_FILE = "events.json"

def load_events():
    try:
        with open(EVENT_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_events(events):
    with open(EVENT_FILE, "w") as f:
        json.dump(events, f, indent=4)

def add_event(name, time, capacity, charges):
    events = load_events()
    event_id = len(events) + 1
    events.append({
        "event_id": event_id,
        "event_name": name,
        "event_time": time,
        "capacity": capacity,
        "charges": charges,
        "participants": []
    })
    save_events(events)
    st.session_state["events"] = events

def participate(event_id, user_name):
    events = st.session_state.get("events", load_events())
    for event in events:
        if event["event_id"] == event_id:
            if user_name in event["participants"]:
                return False
            if len(event["participants"]) >= event["capacity"]:
                return False
            event["participants"].append(user_name)
            save_events(events)
            st.session_state["events"] = events
            return True
    return False

def delete_event(event_id):
    events = st.session_state.get("events", load_events())
    events = [event for event in events if event["event_id"] != event_id]
    for idx, event in enumerate(events):
        event["event_id"] = idx + 1
    save_events(events)
    st.session_state["events"] = events


# Streamlit UI

st.set_page_config(page_title="Musicloud", layout="wide")
st.title("Musicloud")

if "playlist" not in st.session_state:
    st.session_state["playlist"] = load_playlist()
if "events" not in st.session_state:
    st.session_state["events"] = load_events()

menu = st.sidebar.selectbox("Menu", ["Music Recommender", "Playlist Management", "Event Management"])


# Music Recommender Section

if menu == "Music Recommender":
    selected_song = st.selectbox("Search or type a song", music_list)
    if st.button("Show Recommendation"):
        names, posters = recommend(selected_song)
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            col.text(names[idx])
            col.image(posters[idx])
            if col.button(f"Add to Playlist", key=f"playlist_{idx}"):
                artist = music[music['song'] == names[idx]]["artist"].values[0]
                add_to_playlist(names[idx], artist)
                st.success(f"'{names[idx]}' added to your playlist!")


# Playlist Management Section

elif menu == "Playlist Management":
    st.header("Playlist Management")
    action = st.radio("Choose Action", ["View Playlist", "Clear Playlist"])
    if action == "View Playlist":
        playlist = st.session_state["playlist"]
        if playlist:
            st.subheader("Your Playlist")
            for idx, item in enumerate(playlist):
                st.write(f"**{idx+1}. {item['song']}** — {item['artist']} 🎧 [Listen on Spotify](https://open.spotify.com/search/{item['song']}%20{item['artist']})")
        else:
            st.info("Your playlist is empty.")
    elif action == "Clear Playlist":
        if st.button("Clear All Playlist"):
            save_playlist([])
            st.session_state["playlist"] = []
            st.success("Playlist cleared successfully!")


# Event Management Section

elif menu == "Event Management":
    st.header("Event Management System")
    action = st.radio("Choose Action", ["Add Event", "View Events"])

    if action == "Add Event":
        st.subheader("Add New Event")
        # FIX: Wrap in st.form to prevent reload until submission
        with st.form(key="add_event_form"):
            name = st.text_input("Event Name")
            time = st.text_input("Event Time (YYYY-MM-DD HH:MM)")
            capacity = st.number_input("Capacity", min_value=1, step=1)
            charges = st.number_input("Charges", min_value=0, step=1)
            submitted = st.form_submit_button("Add Event")

        if submitted:
            if name and time:
                try:
                    datetime.strptime(time, "%Y-%m-%d %H:%M")
                    add_event(name, time, capacity, charges)
                    st.success("Event added successfully!")
                except ValueError:
                    st.error("⚠ Invalid date format. Use YYYY-MM-DD HH:MM")
            else:
                st.error("⚠ Please fill all fields")

    elif action == "View Events":
        st.subheader("Available Events")
        events = st.session_state.get("events", load_events())
        if not events:
            st.info("No events available.")
        else:
            for event in events:
                st.markdown(f"### {event['event_name']}")
                st.write(f"Time: {event['event_time']}")
                st.write(f"Capacity: {event['capacity']}")
                st.write(f"Participants: {len(event['participants'])}")
                st.write(f"Charges: ${event['charges']}")
                is_full = len(event["participants"]) >= event["capacity"]

                with st.form(key=f"participate_form_{event['event_id']}"):
                    user_name = st.text_input("Enter your name to participate", key=f"name_{event['event_id']}")
                    submitted = st.form_submit_button(f"Participate in {event['event_name']}", disabled=is_full)
                    if submitted:
                        if user_name:
                            if participate(event["event_id"], user_name):
                                st.success(f"You joined {event['event_name']}!")
                            else:
                                st.error("You are already participating or event is full!")
                        else:
                            st.warning("⚠ Please enter your name to participate")

                if is_full:
                    st.warning("⚠ This event is full. No more participants can join.")

                if st.button(f"Delete {event['event_name']}", key=f"delete_{event['event_id']}"):
                    delete_event(event["event_id"])
                    st.success(f"Event '{event['event_name']}' deleted successfully!")
