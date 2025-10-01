import joblib
import pandas as pd
import pickle
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download tokenizer if not already installed
nltk.download('punkt')
nltk.download('punkt_tab')

# Initialize stemmer
stemmer = PorterStemmer()

# Tokenization function
def tokenization(txt):
    tokens = nltk.word_tokenize(txt)
    stemming = [stemmer.stem(w) for w in tokens]
    return " ".join(stemming)

# 1. Load dataset
df = pd.read_csv("spotify_millsongdata.csv")

# 2. Sample 5000 rows and drop the 'link' column
df = df.sample(5000).drop('link', axis=1).reset_index(drop=True)

# 3. Clean text (lowercase + remove newlines)
df['text'] = df['text'].str.lower().replace(r'^\w\s', ' ').replace(r'\n', ' ', regex=True)

# 4. Apply tokenization + stemming
df['text'] = df['text'].apply(lambda x: tokenization(x))

# 5. TF-IDF Vectorization
tfidvector = TfidfVectorizer(analyzer='word', stop_words='english')
matrix = tfidvector.fit_transform(df['text'])

# 6. Similarity matrix
similarity = cosine_similarity(matrix)

# 7. Save as pickle files

joblib.dump(df, 'df.pkl', compress=3)
joblib.dump(similarity, 'similarity.pkl', compress=9)

