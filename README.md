# 🎵 Musicloud

A Python-based music recommendation system using **Streamlit**, **Spotify API**, and **Machine Learning** (TF-IDF & Cosine Similarity).

## ✨ Features

- **🎵 Music Recommendations**: Content-based filtering using TF-IDF and cosine similarity
- **📝 Playlist Management**: Create, manage, and delete custom playlists (stored in JSON)
- **🎫 Event Management**: Create music events with capacity limits, charges, and participant registration (stored in JSON)
- **🎨 Album Covers**: Fetch album art using Spotify API (optional)

## 📁 Project Structure

```
├── app.py                      # Main Streamlit application
├── data_cleaning.py            # Preprocesses CSV and generates pkl files
├── spotify_millsongdata.csv    # Music dataset
├── df.pkl                      # Processed dataframe (generated)
├── similarity.pkl              # Similarity matrix (generated)
├── playlists.json              # Playlist storage
├── events.json                 # Event storage
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create from .env.example)
└── README.md                   # This file
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd music-recommendation-system
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables (Optional - for album covers)

Create a `.env` file in the project root:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

To get Spotify API credentials:
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy Client ID and Client Secret

### 4. Generate pickle files

**IMPORTANT**: Before running the app, you must preprocess the data:

```bash
python data_cleaning.py
```

This will generate:
- `df.pkl` - Cleaned and processed dataframe
- `similarity.pkl` - Cosine similarity matrix for recommendations

### 5. Run the application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🎯 Usage

### Music Recommendations
1. Browse songs by genre or search by name/artist
2. Select a song and click "Get Recommendations" to find similar songs
3. Add songs to your playlists

### Playlist Management
1. Create playlists with names and descriptions
2. Add songs from recommendations
3. View and manage songs in each playlist
4. Delete playlists when no longer needed

### Event Management
1. Create music events with:
   - Event name
   - Date
   - Capacity
   - Entry charges
2. Register participants (auto-closes when capacity is full)
3. View participant lists
4. Delete events

## 📊 Dataset

The project uses `spotify_millsongdata.csv` containing:
- Song names
- Artist names
- Genre/category (link column)
- Lyrics/text features

## 🔧 Technologies Used

- **Python 3.8+**
- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **Scikit-learn** - TF-IDF & Cosine Similarity
- **NLTK** - Text preprocessing
- **Spotipy** - Spotify API integration
- **Pickle/Joblib** - Model persistence

## 📝 Data Storage

- **Playlists**: Stored in `playlists.json`
- **Events**: Stored in `events.json`
- **Processed Data**: Stored in `df.pkl` and `similarity.pkl`

## 🌐 Hosting

- **Render**: Go to  `https://render.com/`
- **Link**: Click `https://musicloud-7zus.onrender.com`
# Note
- It may take some time to load the site as render is third-party hosting site.
  
## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Acknowledgments

- Spotify Million Song Dataset
- Streamlit community
- Spotify Web API
