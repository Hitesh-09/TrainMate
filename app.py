from flask import Flask, render_template, request, url_for, jsonify
from data_manager import DataManager
import os
import json
import jinja2

# Initialize the data manager with path to data folder
data_dir = os.path.join(os.path.dirname(__file__), 'data')
data_manager = DataManager(data_dir)

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Add tojson filter to Jinja2 environment
app.jinja_env.filters['tojson'] = lambda v: json.dumps(v)

# Helper functions to load data directly if needed
def load_trains():
    """Load trains data directly from JSON file"""
    with open(os.path.join(data_dir, 'trains.json')) as f:
        return json.load(f)

def load_stations():
    """Load stations data directly from JSON file"""
    with open(os.path.join(data_dir, 'stations.json')) as f:
        return json.load(f)

@app.route('/')
def home():
    # Pass stations data for use in the autocomplete
    stations = data_manager.get_all_stations()
    return render_template('index.html', stations=stations)

@app.route('/plans')
def plans():
    return render_template('plans.html')
    
@app.route('/api/stations')
def api_stations():
    """API endpoint to get all stations"""
    stations = data_manager.get_all_stations()
    return jsonify(stations)

@app.route('/api/trains')
def api_trains():
    """API endpoint to get all trains"""
    trains = data_manager.get_all_trains()
    return jsonify(trains)

@app.route('/api/search')
def api_search():
    """API endpoint to search for trains"""
    source = request.args.get('source', '')
    destination = request.args.get('destination', '')
    date = request.args.get('date', '')
    
    if not source or not destination:
        return jsonify({"error": "Source and destination are required"}), 400
        
    # Get station codes from names if needed
    source_code = data_manager.get_station_code(source) or source.upper()
    dest_code = data_manager.get_station_code(destination) or destination.upper()
    
    trains = data_manager.find_trains(source_code, dest_code, date)
    return jsonify(trains)

@app.route('/results', methods=['GET', 'POST'])
def results():
    print("Request received:", request.method)
    
    if request.method == 'POST':
        print("Form data received:", request.form)
        source = request.form.get('source', '').strip()
        destination = request.form.get('destination', '').strip()
        date = request.form.get('date', '')
    else:  # GET request
        source = request.args.get('source', '').strip()
        destination = request.args.get('destination', '').strip()
        date = request.args.get('date', '')
    
    print(f"Processing search: {source} to {destination} on {date}")
    
    # Convert date to format expected in our data (YYYY-MM-DD)
    try:
        # Parse and reformat the date if needed
        if date:
            from datetime import datetime
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date = date_obj.strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Error parsing date: {e}")

    # Get station codes from names if needed
    source_code = data_manager.get_station_code(source)
    if not source_code:
        source_code = source.upper()
        print(f"Warning: Could not find station code for '{source}', using {source_code}")
    
    dest_code = data_manager.get_station_code(destination)
    if not dest_code:
        dest_code = destination.upper()
        print(f"Warning: Could not find station code for '{destination}', using {dest_code}")
    
    print(f"Using station codes: {source_code} to {dest_code}")

    # Find direct trains
    matched_trains = data_manager.find_trains(source_code, dest_code, date)

    # Check if all direct trains are waitlisted
    all_waitlisted = (
        matched_trains and
        all("WL" in train["availability_status"] for train in matched_trains)
    )

    # Find alternate source stations with available trains to destination
    suggestions = []
    if not matched_trains or all_waitlisted:
        # Find trains to the same destination from other stations
        for train in data_manager.get_all_trains():
            if (train["to"] == dest_code and 
                train["from"] != source_code and 
                "WL" not in train["availability"].get(date, "WL")):
                
                train_info = train.copy()
                train_info["from_name"] = data_manager.get_station_name(train["from"])
                train_info["to_name"] = data_manager.get_station_name(train["to"])
                train_info["availability_status"] = train["availability"].get(date, "No information")
                suggestions.append(train_info)

    # Find break journey options (multi-leg journeys)
    break_journeys = []
    if not matched_trains or all_waitlisted:
        break_journeys = data_manager.find_break_journey(source_code, dest_code, date)
    
    # Debug log to confirm data
    print("Matched Trains:", len(matched_trains))
    print("Suggestions:", len(suggestions))
    print("Break Journeys:", len(break_journeys))
    
    # Format source and destination for display
    source_name = data_manager.get_station_name(source_code)
    dest_name = data_manager.get_station_name(dest_code)

    return render_template('results.html',
                           source=source_name,
                           destination=dest_name,
                           date=date,
                           matched_trains=matched_trains,
                           suggestions=suggestions,
                           break_journeys=break_journeys)

@app.route('/debug')
def debug_data():
    """Debug route to check data loading"""
    stations = data_manager.get_all_stations()
    trains = data_manager.get_all_trains()
    
    # Try a specific search to debug
    source_code = "JL"  # Jalgaon
    dest_code = "MAS"   # Chennai
    date = "2024-05-27"
    
    direct_trains = data_manager.find_trains(source_code, dest_code, date)
    break_journeys = data_manager.find_break_journey(source_code, dest_code, date)
    
    return render_template('debug.html', 
                           stations=stations[:10],  # Show first 10 stations
                           trains=trains[:10],      # Show first 10 trains
                           source=source_code,
                           destination=dest_code,
                           date=date,
                           direct_trains=direct_trains,
                           break_journeys=break_journeys)

@app.route('/test/<source>/<destination>/<date>')
def test_data(source, destination, date):
    """Test route with specific parameters to debug data"""
    # Get station codes from names if needed
    source_code = data_manager.get_station_code(source) or source.upper()
    dest_code = data_manager.get_station_code(destination) or destination.upper()
    
    # Find direct trains
    direct_trains = data_manager.find_trains(source_code, dest_code, date)
    
    # Find break journey options
    break_journeys = data_manager.find_break_journey(source_code, dest_code, date)
    
    # Get all stations and trains for debugging
    stations = data_manager.get_all_stations()
    trains = data_manager.get_all_trains()
    
    # Format source and destination for display
    source_name = data_manager.get_station_name(source_code)
    dest_name = data_manager.get_station_name(dest_code)
    
    return render_template('data_test.html',
                          source=source_name,
                          source_code=source_code,
                          destination=dest_name,
                          dest_code=dest_code,
                          date=date,
                          direct_trains=direct_trains,
                          break_journeys=break_journeys,
                          stations=stations,
                          trains=trains)

@app.route('/find-trains')
def find_trains_direct():
    """Simple route to directly find trains between Jalgaon and Chennai"""
    source_code = "JL"  # Jalgaon code
    dest_code = "MAS"   # Chennai code
    date = "2025-05-27"
    
    # Find direct trains
    direct_trains = data_manager.find_trains(source_code, dest_code, date)
    
    # Get station names for display
    source_name = data_manager.get_station_name(source_code)
    dest_name = data_manager.get_station_name(dest_code)
    
    # Return plain text response with the findings
    response = f"Search: {source_name} ({source_code}) to {dest_name} ({dest_code}) on {date}\n\n"
    response += f"Found {len(direct_trains)} direct trains:\n\n"
    
    for train in direct_trains:
        response += f"Train: {train['train_number']} - {train['name']}\n"
        response += f"Departure: {train['departure']}, Arrival: {train.get('arrival', 'Unknown')}\n"
        response += f"Availability: {train['availability_status']}\n\n"
    
    # Return as plain text
    return response, 200, {'Content-Type': 'text/plain'}

@app.route('/test-search')
def test_search():
    """Simple test search form with direct station selection"""
    stations = data_manager.get_all_stations()
    return render_template('test_search.html', stations=stations)

@app.route('/test-results')
def test_results():
    """Simple test results page"""
    source = request.args.get('source', '').strip()
    destination = request.args.get('destination', '').strip()
    date = request.args.get('date', '')
    
    # Find direct trains
    direct_trains = data_manager.find_trains(source, destination, date)
    
    # Format source and destination for display
    source_name = data_manager.get_station_name(source) or source
    dest_name = data_manager.get_station_name(destination) or destination
    
    return render_template('test_results.html',
                           source=source_name,
                           source_code=source,
                           destination=dest_name,
                           dest_code=destination,
                           date=date,
                           trains=direct_trains)

# ✅ Main entry point
if __name__ == '__main__':
    app.run(debug=True)
