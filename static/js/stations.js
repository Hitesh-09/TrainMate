// Station autocomplete functionality

document.addEventListener('DOMContentLoaded', function() {
  // Check if we have stationData variable from the template
  if (typeof stationData !== 'undefined') {
    setupAutocomplete(stationData);
  } else {
    // Fetch stations data from our API as fallback
    fetch('/api/stations')
      .then(response => response.json())
      .then(stations => {
        setupAutocomplete(stations);
      })
      .catch(error => {
        console.error('Error loading stations:', error);
        // Use fallback stations in case API fails
        setupAutocomplete(fallbackStations);
      });
    
  // Setup autocomplete functionality on the form fields
  function setupAutocomplete(stations) {
    const sourceInput = document.getElementById('source');
    const destInput = document.getElementById('destination');
    
    if (!sourceInput || !destInput) return;
    
    // Create station name array for autocomplete
    const stationNames = stations.map(station => station.name);
    
    // Setup autocomplete for source field
    if (sourceInput) {
      new Autocomplete(sourceInput, {
        data: stationNames,
        maximumItems: 7,
        threshold: 2,
        onSelectItem: ({ label, value }) => {
          console.log("Source selected:", label);
        }
      });
    }
    
    // Setup autocomplete for destination field
    if (destInput) {
      new Autocomplete(destInput, {
        data: stationNames,
        maximumItems: 7,
        threshold: 2,
        onSelectItem: ({ label, value }) => {
          console.log("Destination selected:", label);
        }
      });
    }
  }
  
  // Fallback stations in case API fails
  const fallbackStations = [
    { name: "New Delhi", code: "NDLS" },
    { name: "Mumbai Central", code: "BCT" },
    { name: "Mumbai CST", code: "CSTM" },
    { name: "Chennai Central", code: "MAS" },
    { name: "Bengaluru", code: "SBC" },
    { name: "Howrah", code: "HWH" },
    { name: "Pune Junction", code: "PUNE" },
    { name: "Ahmedabad Junction", code: "ADI" },
    { name: "Jaipur", code: "JP" },
    { name: "Lucknow", code: "LKO" }
  ];
});