/**
 * Station autocomplete initialization
 */
document.addEventListener('DOMContentLoaded', function() {
  // Check if we have stationData variable available
  if (typeof window.stationData !== 'undefined' && window.stationData.length > 0) {
    setupStationAutocomplete(window.stationData);
  } else {
    // Fetch stations data from API as fallback
    fetch('/api/stations')
      .then(response => response.json())
      .then(stations => {
        setupStationAutocomplete(stations);
      })
      .catch(error => {
        console.error('Error loading stations:', error);
      });
  }

  // Setup autocomplete for source and destination fields
  function setupStationAutocomplete(stations) {
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
        onSelectItem: ({ label }) => {
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
        onSelectItem: ({ label }) => {
          console.log("Destination selected:", label);
        }
      });
    }
  }
});