// India railway map visualization
document.addEventListener('DOMContentLoaded', function() {
  const mapContainer = document.getElementById('india-railway-map');
  if (!mapContainer) return;

  // Major railway junctions in India with coordinates
  const majorStations = [
    { name: "Delhi", lat: 28.7041, lng: 77.1025, size: 12 },
    { name: "Mumbai", lat: 19.0760, lng: 72.8777, size: 12 },
    { name: "Chennai", lat: 13.0827, lng: 80.2707, size: 12 },
    { name: "Kolkata", lat: 22.5726, lng: 88.3639, size: 12 },
    { name: "Bangalore", lat: 12.9716, lng: 77.5946, size: 10 },
    { name: "Hyderabad", lat: 17.3850, lng: 78.4867, size: 10 },
    { name: "Ahmedabad", lat: 23.0225, lng: 72.5714, size: 9 },
    { name: "Pune", lat: 18.5204, lng: 73.8567, size: 9 },
    { name: "Jaipur", lat: 26.9124, lng: 75.7873, size: 8 },
    { name: "Lucknow", lat: 26.8467, lng: 80.9462, size: 8 },
    { name: "Kanpur", lat: 26.4499, lng: 80.3319, size: 7 },
    { name: "Nagpur", lat: 21.1458, lng: 79.0882, size: 9 },
    { name: "Jalgaon", lat: 21.0077, lng: 75.5626, size: 8 },
    { name: "Bhusaval", lat: 21.0418, lng: 75.7850, size: 7 }
  ];

  // Create the map
  const map = L.map(mapContainer).setView([23.5937, 78.9629], 5); // Center of India

  // Add tile layer (OpenStreetMap)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  // Add stations as markers
  majorStations.forEach(station => {
    const marker = L.circleMarker([station.lat, station.lng], {
      radius: station.size,
      fillColor: '#4f46e5',
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.8
    }).addTo(map);

    marker.bindTooltip(station.name, {
      permanent: false,
      direction: 'top',
      className: 'station-tooltip'
    });
  });

  // Connect major stations with lines
  const railConnections = [
    ["Mumbai", "Pune"],
    ["Mumbai", "Ahmedabad"],
    ["Delhi", "Jaipur"],
    ["Delhi", "Lucknow"],
    ["Lucknow", "Kanpur"],
    ["Chennai", "Bangalore"],
    ["Hyderabad", "Bangalore"],
    ["Pune", "Nagpur"],
    ["Nagpur", "Kolkata"],
    ["Jalgaon", "Bhusaval"],
    ["Jalgaon", "Pune"],
    ["Bhusaval", "Nagpur"]
  ];

  // Draw railway connections
  railConnections.forEach(connection => {
    const from = majorStations.find(s => s.name === connection[0]);
    const to = majorStations.find(s => s.name === connection[1]);
    
    if (from && to) {
      L.polyline([
        [from.lat, from.lng],
        [to.lat, to.lng]
      ], {
        color: '#6366f1',
        weight: 3,
        opacity: 0.6,
        dashArray: '5, 8'
      }).addTo(map);
    }
  });
  
  // Add source and destination markers if available
  const sourceStation = document.getElementById('source-station-name')?.textContent;
  const destStation = document.getElementById('dest-station-name')?.textContent;
  
  if (sourceStation && destStation) {
    const source = majorStations.find(s => s.name === sourceStation);
    const dest = majorStations.find(s => s.name === destStation);
    
    if (source) {
      L.circleMarker([source.lat, source.lng], {
        radius: 10,
        fillColor: '#22c55e',
        color: '#fff',
        weight: 2,
        opacity: 1,
        fillOpacity: 1
      }).addTo(map).bindTooltip('Source: ' + sourceStation, {
        permanent: true,
        direction: 'top',
        className: 'source-tooltip'
      });
    }
    
    if (dest) {
      L.circleMarker([dest.lat, dest.lng], {
        radius: 10,
        fillColor: '#f43f5e',
        color: '#fff',
        weight: 2,
        opacity: 1,
        fillOpacity: 1
      }).addTo(map).bindTooltip('Destination: ' + destStation, {
        permanent: true,
        direction: 'top',
        className: 'dest-tooltip'
      });
    }
  }
});