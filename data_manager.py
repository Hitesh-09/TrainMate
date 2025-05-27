import json
import os
from datetime import datetime, timedelta

class DataManager:
    """
    Handles loading and managing data from JSON files
    """
    
    def __init__(self, data_dir="data"):
        """Initialize with the directory containing data files"""
        self.data_dir = data_dir
        self.stations = []
        self.trains = []
        self.station_map = {}  # Maps station codes to names
        self.load_data()
    
    def load_data(self):
        """Load data from JSON files"""
        try:
            # Load stations
            stations_file = os.path.join(self.data_dir, "stations.json")
            with open(stations_file, 'r') as f:
                self.stations = json.load(f)
                
            # Create station code to name mapping
            self.station_map = {station["code"]: station["name"] for station in self.stations}
                
            # Load trains
            trains_file = os.path.join(self.data_dir, "trains.json")
            with open(trains_file, 'r') as f:
                self.trains = json.load(f)
                
            print(f"Loaded {len(self.stations)} stations and {len(self.trains)} trains")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_all_stations(self):
        """Return all stations"""
        return self.stations
    
    def get_station_name(self, code):
        """Get station name from code"""
        return self.station_map.get(code, code)
    
    def get_station_code(self, name):
        """Get station code from name (case insensitive)"""
        if not name:
            return None
            
        name = name.lower().strip()
        
        # Check for exact match first
        for station in self.stations:
            if station["name"].lower() == name:
                return station["code"]
        
        # Also check if the provided name is already a station code
        for station in self.stations:
            if station["code"].lower() == name:
                return station["code"]
                
        # Try partial matching for common variations
        for station in self.stations:
            station_name = station["name"].lower()
            # Check if input is a substring or if station name is a substring of input
            if name in station_name or station_name in name:
                return station["code"]
                
        # Special case for common names
        if "jalgaon" in name:
            return "JL"
        elif "chennai" in name:
            return "MAS"
            
        return None
    
    def get_all_trains(self):
        """Return all trains"""
        return self.trains
    
    def find_trains(self, source, destination, date=None):
        """Find trains between source and destination stations"""
        # Normalize inputs
        source = source.upper() if source else ""
        destination = destination.upper() if destination else ""
        
        # If date is not provided, use today's date
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        print(f"DEBUG: Searching for trains from {source} to {destination} on {date}")
        
        # Show available data for debugging
        date_trains = []
        for train in self.trains:
            if date in train["availability"]:
                date_trains.append(f"{train['train_number']} ({train['from']}-{train['to']}): {train['availability'][date]}")
        
        if not date_trains:
            print(f"WARNING: No trains have availability data for {date}")
        else:
            print(f"DEBUG: {len(date_trains)} trains have data for {date}: {', '.join(date_trains[:3])}...")
        
        # Find matching trains
        matching_trains = []
        
        for train in self.trains:
            if train["from"] == source and train["to"] == destination:
                # Check availability for the given date
                availability = train["availability"].get(date, "No information")
                print(f"DEBUG: Found train {train['train_number']} with availability: {availability}")
                
                # Create a copy of the train data with processed station names
                train_info = train.copy()
                train_info["from_name"] = self.get_station_name(train["from"])
                train_info["to_name"] = self.get_station_name(train["to"])
                train_info["availability_status"] = availability
                
                matching_trains.append(train_info)
        
        print(f"DEBUG: Found {len(matching_trains)} matching trains")
        return matching_trains
    
    def find_break_journey(self, source, destination, date=None):
        """Find multi-leg journeys between source and destination stations"""
        source = source.upper()
        destination = destination.upper()
        
        # If date is not provided, use today's date
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
            
        print(f"DEBUG: Searching for break journeys from {source} to {destination} on {date}")
        possible_journeys = []
        
        # Find all trains departing from source
        from_source_trains = {}
        for train in self.trains:
            if train["from"] == source:
                avail = train["availability"].get(date, "Unknown")
                print(f"DEBUG: Source train {train['train_number']} to {train['to']} - availability: {avail}")
                # Only consider non-waitlisted trains
                if "WL" not in avail.upper():
                    via = train["to"]
                    if via not in from_source_trains:
                        from_source_trains[via] = []
                    from_source_trains[via].append(train)
        
        print(f"DEBUG: Found {len(from_source_trains)} intermediate stations from source")
        
        # For each intermediate station, find trains to destination
        for via, trains1 in from_source_trains.items():
            if via != destination:  # Skip if intermediate is actually the destination
                print(f"DEBUG: Checking for connections from {via} to {destination}")
                for train2 in self.trains:
                    if train2["from"] == via and train2["to"] == destination:
                        avail2 = train2["availability"].get(date, "Unknown")
                        print(f"DEBUG: Connection train {train2['train_number']} - availability: {avail2}")
                        # Check availability for the given date
                        if "WL" not in avail2.upper():
                            for train1 in trains1:
                                journey = {
                                    "first_leg": {
                                        "train_number": train1["train_number"],
                                        "name": train1["name"],
                                        "from": train1["from"],
                                        "from_name": self.get_station_name(train1["from"]),
                                        "to": train1["to"],
                                        "to_name": self.get_station_name(train1["to"]),
                                        "departure": train1["departure"],
                                        "arrival": "Estimated",  # Would need more data for actual arrival
                                        "availability": train1["availability"].get(date, "No information")
                                    },
                                    "second_leg": {
                                        "train_number": train2["train_number"],
                                        "name": train2["name"],
                                        "from": train2["from"],
                                        "from_name": self.get_station_name(train2["from"]),
                                        "to": train2["to"],
                                        "to_name": self.get_station_name(train2["to"]),
                                        "departure": train2["departure"],
                                        "arrival": "Estimated",  # Would need more data for actual arrival
                                        "availability": train2["availability"].get(date, "No information")
                                    },
                                    "via": via,
                                    "via_name": self.get_station_name(via)
                                }
                                possible_journeys.append(journey)
        
        # Sort journeys by availability (fewer waitlists first)
        def availability_score(journey):
            leg1 = "WL" in journey["first_leg"]["availability"]
            leg2 = "WL" in journey["second_leg"]["availability"]
            return leg1 + leg2  # 0, 1, or 2 waitlisted legs
            
        possible_journeys.sort(key=availability_score)
        
        return possible_journeys

# Example usage
if __name__ == "__main__":
    dm = DataManager()
    
    # Test station lookup
    print("Station lookup test:")
    print(f"NDLS = {dm.get_station_name('NDLS')}")
    
    # Test train search
    print("\nDirect train search test (Delhi to Mumbai):")
    trains = dm.find_trains("NDLS", "BCT", "2024-08-24")
    for train in trains:
        print(f"{train['train_number']} - {train['name']}: {train['from_name']} to {train['to_name']} - {train['availability_status']}")
    
    # Test break journey search
    print("\nBreak journey search test (Jalgaon to Chennai):")
    journeys = dm.find_break_journey("JL", "MAS", "2024-08-24")
    for journey in journeys[:3]:  # Show top 3 options
        print(f"Option: {journey['from_name']} → {journey['via_name']} → {journey['to_name']}")
        print(f"  First leg: {journey['first_leg']['name']} ({journey['first_leg']['train_number']}) - {journey['first_leg']['availability']}")
        print(f"  Second leg: {journey['second_leg']['name']} ({journey['second_leg']['train_number']}) - {journey['second_leg']['availability']}")