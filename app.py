from flask import Flask, render_template, request, url_for
from mock_data import trains

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plans')
def plans():
    return render_template('plans.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    print("Request received:", request.method)
    
    if request.method == 'POST':
        print("Form data received:", request.form)
        source = request.form.get('source', '').strip().lower()
        destination = request.form.get('destination', '').strip().lower()
        date = request.form.get('date', '')
    else:  # GET request
        source = request.args.get('source', '').strip().lower()
        destination = request.args.get('destination', '').strip().lower()
        date = request.args.get('date', '')
    
    print(f"Processing search: {source} to {destination} on {date}")

    matched_trains = [
        train for train in trains
        if train['from'].lower() == source and train['to'].lower() == destination
    ]

    all_waitlisted = (
        matched_trains and
        all("WL" in train["availability"].upper() for train in matched_trains)
    )

    suggestions = []
    if not matched_trains or all_waitlisted:
        suggestions = [
            train for train in trains
            if train['to'].lower() == destination and train['from'].lower() != source
        ]

    # Find break journey options (multi-leg journeys)
    break_journeys = []
    if not matched_trains or all_waitlisted:
        break_journeys = find_break_journey(source, destination, trains)
    
    # Debug log to confirm data
    print("Matched Trains:", matched_trains)
    print("Suggestions:", suggestions)
    print("Break Journeys:", break_journeys)
    
    # Detailed verification of break journeys
    print("Filtered Break Journeys:")
    for leg1, leg2 in break_journeys:
        print(f"{leg1['from']} → {leg1['to']} | {leg2['from']} → {leg2['to']} | Avail: {leg1['availability']} / {leg2['availability']}")

    return render_template('results.html',
                           source=source.title(),
                           destination=destination.title(),
                           date=date,
                           matched_trains=matched_trains,
                           suggestions=suggestions,
                           break_journeys=break_journeys)

def availability_score(status):
    """
    Calculates a numerical score for availability status.
    Lower is better (0 for available, high numbers for waitlist).
    """
    status = status.lower()
    if "available" in status:
        return 0
    elif "wl" in status:
        # Extract WL number if present
        import re
        match = re.search(r"wl\s*(\d+)", status)
        return int(match.group(1)) if match else 999
    return 999

def find_break_journey(source, destination, trains_data, max_segments=2):
    """
    Find multi-leg journeys between source and destination with available seats.
    
    Args:
        source: Source station
        destination: Destination station
        trains_data: List of train dictionaries
        max_segments: Maximum number of train changes allowed
    
    Returns:
        List of possible journeys, where each journey is a list of train segments
    """
    from mock_data import station_graph
    
    possible_journeys = []
    
    # Helper function to find trains between two stations with availability
    def find_available_trains(src, dst):
        return [
            train for train in trains_data
            if train['from'].lower() == src.lower() and 
               train['to'].lower() == dst.lower() and
               "WL" not in train['availability'].upper()
        ]
    
    # Try single-stop journeys first (2 segments)
    if max_segments >= 2:
        # Get all stations that have trains from source
        intermediate_stations = set()
        for train in trains_data:
            if train['from'].lower() == source.lower() and "WL" not in train['availability'].upper():
                intermediate_stations.add(train['to'].lower())
        
        # For each intermediate station, check if there's a train to final destination
        for middle in intermediate_stations:
            # Skip circular or redundant routes
            if middle.lower() == source.lower() or middle.lower() == destination.lower():
                continue  # Skip circular or redundant routes
                
            segment1 = find_available_trains(source, middle)
            segment2 = find_available_trains(middle, destination)
            
            if segment1 and segment2:
                for s1 in segment1:
                    for s2 in segment2:
                        possible_journeys.append([s1, s2])
    
    # Sort break journeys by combined availability score (lower is better)
    possible_journeys.sort(key=lambda pair: (
        availability_score(pair[0]["availability"]) + availability_score(pair[1]["availability"])
    ))
    
    return possible_journeys

# ✅ Main entry point
if __name__ == '__main__':
    app.run(debug=True)
