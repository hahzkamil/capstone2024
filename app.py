from flask import Flask, jsonify
import threading
from data_processor import calculate_usage  # Import the function to process data
from data_sender import insert_data_periodically  # Import the function to run periodically
from flask_cors import CORS
app = Flask(__name__)

CORS(app)

@app.route('/get-usage', methods=['GET'])
def get_usage():
    try:
        usage_data = calculate_usage()  # Get the calculated data
        if usage_data:
            return jsonify({
                "avg_weekly": usage_data['avg_weekly'],  # Example static data, update as needed
                "avg_monthly": usage_data['avg_monthly'],  # Example static data, update as needed
                "energy_consumption_month": usage_data['monthly_usage'],  # Use real data
                "edel": usage_data['edel'],  # Example static data, update as needed
                "daily_energy_consumption": usage_data['daily_usage'],  # Real data
                "daily_energy_apparent": 1.2,  # Example static data, update as needed
                "max_demand": 10,  # Example static data, update as needed
                "daily_energy_reactive": 0.8,  # Example static data, update as needed
                "energy_consumption_week": usage_data['weekly_usage'],  # Real data
            }), 200
        else:
            return jsonify({"error": "Unable to calculate usage data"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start background thread to insert data periodically
def start_periodic_insertion():
    threading.Thread(target=insert_data_periodically, daemon=True).start()

if __name__ == '__main__':
    start_periodic_insertion()  # Start background insertion before running Flask
    app.run(debug=True)
