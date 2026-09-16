import pickle

# Load your heavy 180MB file
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Convert data type to float16 (instantly drops size to ~45MB)
similarity_optimized = similarity.astype('float16')

# Overwrite the old similarity.pkl with this optimized one
with open("similarity.pkl", "wb") as f:
    pickle.dump(similarity_optimized, f)

print("Done! Your similarity.pkl is now optimized and ready for GitHub Desktop.")