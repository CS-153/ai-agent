import os
from google.cloud import firestore
import json

# Set authentication key (if not set globally)
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "tomaba-sa.json"

# Initialize Firestore client
db = firestore.Client()


# Set Firestore project ID
# PROJECT_ID = "tomaba"

# Initialize Firestore Client
db = firestore.Client()


def fetch_recipe():
    """Fetches the first available recipe from Firestore and prints it."""
    try:
        # Get all documents in the 'recipe' collection
        recipes = db.collection("recipe").stream()

        # Fetch the first document
        for doc in recipes:
            recipe_data = doc.to_dict()
            recipe_data["id"] = doc.id  # Include Firestore document ID
            print("✅ Firestore connection successful! Recipe:")
            print(json.dumps(recipe_data, indent=4))
            return

        print("❌ No recipes found in Firestore.")
    except Exception as e:
        print("❌ Firestore connection failed:", e)


if __name__ == "__main__":
    fetch_recipe()
