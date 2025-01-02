from supabase import create_client, Client
import random
from datetime import datetime
import time

# Initialize Supabase connection
SUPABASE_URL = "https://soxzzfsiaxelwbkgodtn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNveHp6ZnNpYXhlbHdia2dvZHRuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU3OTI1OTQsImV4cCI6MjA1MTM2ODU5NH0.rjXaXycaCIh7nvGAzkAfejx5EN33oXjUA1H9Z2JkNMc"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Function to insert random data into Supabase
def insert_random_data():
    consumption = random.uniform(20, 50)  # Simulate random energy consumption in kWh
    timestamp = datetime.now().isoformat()  # Current timestamp in ISO format
    data = {
        "timestamp": timestamp,
        "consumption": consumption
    }

    try:
        response = supabase.table('energy_consumption').insert(data).execute()
        if response.data:
            print("Data inserted successfully:", response.data)
        else:
            print("No data returned. Check if insertion succeeded.")
    except Exception as e:
        print(f"Error inserting data: {e}")

# Periodic data insertion every 5 seconds
def insert_data_periodically():
    while True:
        insert_random_data()
        time.sleep(5)
