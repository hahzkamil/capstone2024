from datetime import datetime, timedelta
from supabase import create_client, Client

# Initialize Supabase connection
SUPABASE_URL = "https://soxzzfsiaxelwbkgodtn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNveHp6ZnNpYXhlbHdia2dvZHRuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzU3OTI1OTQsImV4cCI6MjA1MTM2ODU5NH0.rjXaXycaCIh7nvGAzkAfejx5EN33oXjUA1H9Z2JkNMc"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def calculate_usage():
    try:
        now = datetime.now()  # Current timestamp (naive, no timezone)
        print(f"Current time: {now}")

        # Fetch all data from Supabase
        data = supabase.table('energy_consumption').select("*").execute().data
        print(f"Fetched {len(data)} records from Supabase.")

        # Initialize accumulators
        daily_usage_kwh = 0
        weekly_usage_kwh = 0
        monthly_usage_kwh = 0

        # Process each record
        for record in data:
            try:
                # Convert timestamp from Supabase to a naive datetime object
                timestamp = datetime.fromisoformat(record['timestamp'])
                consumption = record['consumption']
                print(f"Processing record - Timestamp: {timestamp}, Consumption: {consumption}")

                # Calculate daily, weekly, monthly usage based on timestamp
                if now - timedelta(days=1) <= timestamp:
                    daily_usage_kwh += consumption
                if now - timedelta(weeks=1) <= timestamp:
                    weekly_usage_kwh += consumption
                if now - timedelta(days=30) <= timestamp:
                    monthly_usage_kwh += consumption

            except Exception as record_error:
                print(f"Error processing record {record}: {record_error}")

        daily_usage_kwh = round(daily_usage_kwh, 2)
        weekly_usage_kwh = round(weekly_usage_kwh, 2)
        monthly_usage_kwh = round(monthly_usage_kwh, 2)
        
        # Convert kWh to GWh by dividing by 1,000,000 and round to 6 decimal places
        daily_usage_gwh = round(daily_usage_kwh / 1_000_000, 6)
        weekly_usage_gwh = round(weekly_usage_kwh / 1_000_000, 6)
        monthly_usage_gwh = round(monthly_usage_kwh / 1_000_000, 6)

        avg_weekly = round(weekly_usage_gwh / 7, 6)
        avg_monthly = round(monthly_usage_gwh / 30, 6)

        # Print the final accumulated values for debugging
        print(f"Daily usage: {daily_usage_gwh} GWh, Weekly usage: {weekly_usage_gwh} GWh, Monthly usage: {monthly_usage_gwh} GWh, avg week: {avg_weekly} GWh, avg month: {avg_monthly}")

        # Return the calculated values
        return {
            'daily_usage': consumption,
            'weekly_usage': weekly_usage_gwh,
            'monthly_usage': monthly_usage_gwh,
            'avg_monthly': avg_monthly,  # Example static data, replace with actual data
            'avg_weekly': avg_weekly,  # Example static data
            'edel': daily_usage_gwh,

        }

    except Exception as e:
        print(f"Error calculating usage: {e}")
        return None
