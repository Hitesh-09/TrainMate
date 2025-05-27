/**
 * Simple autocomplete library for TrainMate
 */
class Autocomplete {
  constructor(field, options) {
    this.field = field;
    this.options = Object.assign({
      data: [],
      maximumItems: 5,
      threshold: 2,
      onSelectItem: () => {}
    }, options);
    
    // Wrap field in container for proper positioning if not already wrapped
    if (!this.field.parentElement.classList.contains('autocomplete-container')) {
      const container = document.createElement('div');
      container.className = 'autocomplete-container';
      this.field.parentNode.insertBefore(container, this.field);
      container.appendChild(this.field);
    }
    
    this.dropdown = null;
    this.currentItems = [];
    this.init();
  }
  
  init() {
    // Create the dropdown container
    this.dropdown = document.createElement('div');
    this.dropdown.className = 'autocomplete-dropdown';
    this.dropdown.style.display = 'none';
    
    // Insert dropdown after the field
    this.field.parentNode.insertBefore(this.dropdown, this.field.nextSibling);
    
    // Position the dropdown
    const updatePosition = () => {
      const rect = this.field.getBoundingClientRect();
      this.dropdown.style.top = `${rect.bottom + window.scrollY}px`;
      this.dropdown.style.left = `${rect.left + window.scrollX}px`;
      this.dropdown.style.width = `${rect.width}px`;
    };
    
    // Attach event listeners
    this.field.addEventListener('input', () => {
      this.onInput();
      updatePosition();
    });
    
    this.field.addEventListener('focus', () => {
      if (this.currentItems.length > 0) {
        this.dropdown.style.display = 'block';
        updatePosition();
      }
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
      if (e.target !== this.field && e.target !== this.dropdown) {
        this.dropdown.style.display = 'none';
      }
    });
    
    // Additional listeners to handle arrow keys and enter
    this.field.addEventListener('keydown', (e) => {
      if (this.dropdown.style.display === 'none') return;
      
      const items = this.dropdown.querySelectorAll('.autocomplete-item');
      let activeIndex = Array.from(items).findIndex(item => item.classList.contains('active'));
      
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          if (activeIndex >= 0) {
            items[activeIndex].classList.remove('active');
          }
          activeIndex = (activeIndex + 1) % items.length;
          items[activeIndex].classList.add('active');
          items[activeIndex].scrollIntoView({ block: 'nearest' });
          break;
          
        case 'ArrowUp':
          e.preventDefault();
          if (activeIndex >= 0) {
            items[activeIndex].classList.remove('active');
          }
          activeIndex = activeIndex <= 0 ? items.length - 1 : activeIndex - 1;
          items[activeIndex].classList.add('active');
          items[activeIndex].scrollIntoView({ block: 'nearest' });
          break;
          
        case 'Enter':
          if (activeIndex >= 0) {
            e.preventDefault();
            this.selectItem(this.currentItems[activeIndex]);
          }
          break;
          
        case 'Escape':
          this.dropdown.style.display = 'none';
          break;
      }
    });
  }
  
  onInput() {
    const value = this.field.value.trim().toLowerCase();
    
    // Hide dropdown if value is too short
    if (value.length < this.options.threshold) {
      this.dropdown.style.display = 'none';
      return;
    }
    
    // Filter data based on input
    this.currentItems = this.options.data.filter(item => {
      return item.toLowerCase().includes(value);
    }).slice(0, this.options.maximumItems);
    
    if (this.currentItems.length === 0) {
      this.dropdown.style.display = 'none';
      return;
    }
    
    // Render dropdown items
    this.renderDropdown();
    this.dropdown.style.display = 'block';
  }
  
  renderDropdown() {
    this.dropdown.innerHTML = '';
    
    this.currentItems.forEach((item, index) => {
      const element = document.createElement('div');
      element.className = 'autocomplete-item';
      element.style.padding = '8px 12px';
      element.style.cursor = 'pointer';
      element.style.borderBottom = index < this.currentItems.length - 1 ? '1px solid #eee' : 'none';
      
      // Highlight the matching part of the text
      const value = this.field.value.trim().toLowerCase();
      const itemText = item;
      const lowerItemText = itemText.toLowerCase();
      const matchIndex = lowerItemText.indexOf(value);
      
      if (matchIndex >= 0) {
        const before = itemText.substring(0, matchIndex);
        const match = itemText.substring(matchIndex, matchIndex + value.length);
        const after = itemText.substring(matchIndex + value.length);
        element.innerHTML = `${before}<strong>${match}</strong>${after}`;
      } else {
        element.textContent = itemText;
      }
      
      element.addEventListener('mouseenter', () => {
        this.dropdown.querySelectorAll('.autocomplete-item').forEach(el => el.classList.remove('active'));
        element.classList.add('active');
      });
      
      element.addEventListener('click', () => {
        this.selectItem(item);
      });
      
      element.addEventListener('mouseleave', () => {
        element.classList.remove('active');
      });
      
      this.dropdown.appendChild(element);
    });
    
    // Add styles for active state
    const style = document.createElement('style');
    style.textContent = `
      .autocomplete-item.active {
        background-color: #f0f0f0;
      }
    `;
    document.head.appendChild(style);
  }
  
  selectItem(item) {
    this.field.value = item;
    this.dropdown.style.display = 'none';
    this.options.onSelectItem({ label: item, value: item });
  }
}