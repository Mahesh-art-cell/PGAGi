from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from .env
MONGO_URI = os.getenv("MONGO_URI")

# Create MongoDB client
client = MongoClient(MONGO_URI)

# Access the database
db = client["talentscout"]
interviews_collection = db["interviews"]

def save_interview_data(user_data, questions, answers, feedback, rating):
    """Save interview session data to MongoDB."""
    interview_document = {
        "user": user_data,
        "questions": questions,
        "answers": answers,
        "feedback": feedback,
        "rating": rating
    }

    try:
        result = interviews_collection.insert_one(interview_document)
        print(f"✅ Interview data saved with ID: {result.inserted_id}")
    except Exception as e:
        print(f"❌ Error saving data to MongoDB: {e}")
