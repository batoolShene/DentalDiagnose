import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Testing environment variables:")
print(f"DB_HOST: '{os.getenv('DB_HOST')}'")
print(f"DB_USER: '{os.getenv('DB_USER')}'")
print(f"DB_PASSWORD: '{os.getenv('DB_PASSWORD')}'")
print(f"DB_NAME: '{os.getenv('DB_NAME')}'")
print(f"DB_PORT: '{os.getenv('DB_PORT')}'")

# Check if .env file exists
if os.path.exists('.env'):
    print("\n✓ .env file found")
    with open('.env', 'r') as f:
        print("Content:")
        print(f.read())
else:
    print("\n✗ .env file not found")