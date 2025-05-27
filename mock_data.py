trains = [
    {"train_no": "10001", "train_name": "Jalgaon Express", "from": "Jalgaon", "to": "Chennai", "availability": "WL 45"},
    {"train_no": "10002", "train_name": "Jalgaon Pune Special", "from": "Jalgaon", "to": "Pune", "availability": "Available 5"},
    {"train_no": "10003", "train_name": "Pune Chennai SF", "from": "Pune", "to": "Chennai", "availability": "WL 20"},
    {"train_no": "10004", "train_name": "Pune Chennai SF 2", "from": "Pune", "to": "Chennai", "availability": "Available 12"},
    {"train_no": "10005", "train_name": "Jalgaon Bhusaval", "from": "Jalgaon", "to": "Bhusaval", "availability": "Available 2"},
    {"train_no": "10006", "train_name": "Bhusaval Chennai", "from": "Bhusaval", "to": "Chennai", "availability": "WL 50"},
    {"train_no": "10007", "train_name": "Bhusaval Chennai Fast", "from": "Bhusaval", "to": "Chennai", "availability": "Available 8"},
]

# Station graph mapping each station to its nearby/connected stations
station_graph = {
    "Jalgaon": ["Pune", "Bhusaval"],
    "Pune": ["Mumbai"],
    "Chennai": ["Tambaram"],
    "Bhusaval": ["Jalgaon", "Burhanpur"],
    "Mumbai": ["Pune", "Thane", "Karjat"]
}
