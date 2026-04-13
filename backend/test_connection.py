"""
Quick MongoDB connection test with certifi
"""
from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
print(f"Testing connection to: {MONGO_URI[:50]}...")

try:
    # Try with certifi certificates
    print(f"Using CA file: {certifi.where()}")
    
    # Attempt 1: With TLS
    print("\nAttempt 1: With TLS enabled...")
    client = MongoClient(
        MONGO_URI,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000
    )
    client.admin.command('ping')
    print("✅ SUCCESS! MongoDB connection works with TLS!")
    print(f"Connected to: {client.get_database().name}")
    
except Exception as e1:
    print(f"❌ Attempt 1 failed: {e1}")
    
    try:
        # Attempt 2: Without TLS (for testing only)
        print("\nAttempt 2: Without TLS (testing only)...")
        MONGO_URI_NO_TLS = MONGO_URI.replace('mongodb+srv://', 'mongodb://').split('?')[0]
        # This won't work with Atlas but let's see the error
        client = MongoClient(
            MONGO_URI,
            tls=False,
            serverSelectionTimeoutMS=5000
        )
        client.admin.command('ping')
        print("✅ Connected without TLS")
    except Exception as e2:
        print(f"❌ Attempt 2 failed: {e2}")
        print("\n⚠️  This appears to be a network-level SSL issue.")
        print("\nRECOMMENDED SOLUTIONS:")
        print("1. RESTART YOUR COMPUTER (clears SSL cache)")
        print("2. Try running on a different network (mobile hotspot)")
        print("3. Check if antivirus/firewall is intercepting SSL")
        print("4. Try deploying to Render - it might work there!")
