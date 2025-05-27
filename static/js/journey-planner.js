// Journey Planning and Saving Functionality
document.addEventListener('DOMContentLoaded', function() {
  // Initialize saved plans
  let savedPlans = JSON.parse(localStorage.getItem('trainmateSavedPlans') || '[]');
  
  // Plan Journey Modal Functionality
  const planJourneyModal = document.getElementById('planJourneyModal');
  const saveJourneyBtn = document.getElementById('saveJourneyBtn');
  const saveJourneyToast = document.getElementById('saveJourneyToast');
  const savedCounter = document.getElementById('savedCounter');
  
  // Setup modal data when opened
  if (planJourneyModal) {
    planJourneyModal.addEventListener('show.bs.modal', function(event) {
      // Get button that triggered the modal
      const button = event.relatedTarget;
      
      // Extract journey data from button data attributes
      const journeyIndex = button.getAttribute('data-journey-index');
      
      // Set source, via, destination
      document.getElementById('modal-source').textContent = button.getAttribute('data-source');
      document.getElementById('modal-via').textContent = button.getAttribute('data-via');
      document.getElementById('modal-destination').textContent = button.getAttribute('data-destination');
      document.getElementById('modal-connection-station').textContent = button.getAttribute('data-via');
      
      // Leg 1 data
      document.getElementById('modal-train1-name').textContent = button.getAttribute('data-leg1-train-name');
      document.getElementById('modal-train1-no').textContent = button.getAttribute('data-leg1-train-no');
      document.getElementById('modal-train1-from').textContent = button.getAttribute('data-leg1-from');
      document.getElementById('modal-train1-to').textContent = button.getAttribute('data-leg1-to');
      
      // Set availability badge for first leg
      const train1Badge = document.getElementById('modal-train1-availability');
      const leg1Availability = button.getAttribute('data-leg1-availability');
      train1Badge.textContent = leg1Availability;
      if (leg1Availability.includes('WL')) {
        train1Badge.className = 'badge bg-danger';
      } else {
        train1Badge.className = 'badge bg-success';
      }
      
      // Leg 2 data
      document.getElementById('modal-train2-name').textContent = button.getAttribute('data-leg2-train-name');
      document.getElementById('modal-train2-no').textContent = button.getAttribute('data-leg2-train-no');
      document.getElementById('modal-train2-from').textContent = button.getAttribute('data-leg2-from');
      document.getElementById('modal-train2-to').textContent = button.getAttribute('data-leg2-to');
      
      // Set availability badge for second leg
      const train2Badge = document.getElementById('modal-train2-availability');
      const leg2Availability = button.getAttribute('data-leg2-availability');
      train2Badge.textContent = leg2Availability;
      if (leg2Availability.includes('WL')) {
        train2Badge.className = 'badge bg-danger';
      } else {
        train2Badge.className = 'badge bg-success';
      }
      
      // Store journey index for saving
      saveJourneyBtn.setAttribute('data-journey-index', journeyIndex);
    });
  }
  
  // Update saved counter badge
  function updateSavedCounter() {
    if (savedCounter) {
      savedCounter.textContent = savedPlans.length;
      if (savedPlans.length > 0) {
        savedCounter.style.display = 'flex';
      } else {
        savedCounter.style.display = 'none';
      }
    }
    
    // Also update navbar badge if exists
    const navPlansBadge = document.getElementById('navPlansBadge');
    if (navPlansBadge) {
      if (savedPlans.length > 0) {
        navPlansBadge.textContent = savedPlans.length;
        navPlansBadge.style.display = 'inline';
      } else {
        navPlansBadge.style.display = 'none';
      }
    }
  }
  
  // Initialize counter
  updateSavedCounter();
  
  // Save journey to local storage
  if (saveJourneyBtn) {
    saveJourneyBtn.addEventListener('click', function() {
      const journeyIndex = this.getAttribute('data-journey-index');
      
      // Get journey data from data attributes
      const source = document.getElementById('modal-source').textContent;
      const via = document.getElementById('modal-via').textContent;
      const destination = document.getElementById('modal-destination').textContent;
      const date = document.getElementById('modal-date').textContent;
      const notes = document.getElementById('journeyNotes').value;
      
      // Get leg 1 data
      const leg1 = {
        trainNo: document.getElementById('modal-train1-no').textContent,
        trainName: document.getElementById('modal-train1-name').textContent,
        from: document.getElementById('modal-train1-from').textContent,
        to: document.getElementById('modal-train1-to').textContent,
        availability: document.getElementById('modal-train1-availability').textContent
      };
      
      // Get leg 2 data
      const leg2 = {
        trainNo: document.getElementById('modal-train2-no').textContent,
        trainName: document.getElementById('modal-train2-name').textContent,
        from: document.getElementById('modal-train2-from').textContent,
        to: document.getElementById('modal-train2-to').textContent,
        availability: document.getElementById('modal-train2-availability').textContent
      };
      
      // Create a plan object
      const plan = {
        id: Date.now(),
        date: date,
        source: source,
        via: via,
        destination: destination,
        legs: [leg1, leg2],
        notes: notes,
        savedAt: new Date().toISOString()
      };
      
      // Add to saved plans
      savedPlans.push(plan);
      localStorage.setItem('trainmateSavedPlans', JSON.stringify(savedPlans));
      
      // Update counter
      updateSavedCounter();
      
      // Show toast notification
      const toastElement = new bootstrap.Toast(saveJourneyToast);
      toastElement.show();
      
      // Clear notes field
      document.getElementById('journeyNotes').value = '';
      
      // Close modal after a short delay
      setTimeout(() => {
        const modalInstance = bootstrap.Modal.getInstance(planJourneyModal);
        modalInstance.hide();
      }, 1500);
    });
  }
});