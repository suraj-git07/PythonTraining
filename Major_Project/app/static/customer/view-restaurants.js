document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing restaurant filters...');
    
    // Make debugging functions available globally
    window.debugFilters = function() {
        const applyButton = document.getElementById('applyFilters');
        const cuisineFilter = document.getElementById('cuisineFilter');
        const locationFilter = document.getElementById('locationFilter');
        
        console.log('Debug info:', {
            applyButton: applyButton,
            cuisineFilter: cuisineFilter,
            locationFilter: locationFilter,
            choicesObjects: window.filterChoices
        });
    };
    
    // Initialize Choices.js for select elements
    const selectElements = document.querySelectorAll('select[data-choices]');
    const choices = {};
    window.filterChoices = choices; // Make available for debugging
    
    selectElements.forEach(select => {
        try {
            choices[select.id] = new Choices(select, {
                removeItemButton: true,
                searchEnabled: true,
                searchPlaceholderValue: 'Type to search...',
                placeholder: true,
                placeholderValue: 'Select options...',
            });
            console.log(`Initialized Choices.js for ${select.id}`);
        } catch (error) {
            console.error(`Failed to initialize Choices.js for ${select.id}:`, error);
        }
    });

    // Handle filter application
    const applyButton = document.getElementById('applyFilters');
    console.log('Apply button found:', applyButton);
    
    if (applyButton) {
        applyButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('Apply filters clicked - this should appear in console');
            
            // Add a visual confirmation
            const originalText = applyButton.innerHTML;
            applyButton.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Applying...';
            applyButton.disabled = true;
            
            setTimeout(() => {
                try {
                    // Get filter values - try both Choices.js and direct select access
                    let cuisines = [];
                    let locations = [];
                    let rating = '';
                    
                    // Try Choices.js first, then fallback to direct select
                    if (choices['cuisineFilter']) {
                        cuisines = choices['cuisineFilter'].getValue().map(item => item.value) || [];
                    } else {
                        const cuisineSelect = document.getElementById('cuisineFilter');
                        if (cuisineSelect) {
                            cuisines = Array.from(cuisineSelect.selectedOptions).map(option => option.value);
                        }
                    }
                    
                    if (choices['locationFilter']) {
                        locations = choices['locationFilter'].getValue().map(item => item.value) || [];
                    } else {
                        const locationSelect = document.getElementById('locationFilter');
                        if (locationSelect) {
                            locations = Array.from(locationSelect.selectedOptions).map(option => option.value);
                        }
                    }
                    
                    if (choices['ratingFilter']) {
                        rating = choices['ratingFilter'].getValue(true) || '';
                    } else {
                        const ratingSelect = document.getElementById('ratingFilter');
                        if (ratingSelect) {
                            rating = ratingSelect.value;
                        }
                    }
                    
                    const minPrice = document.getElementById('minPriceFilter')?.value || '';

                    console.log('Filter values collected:', { cuisines, locations, rating, minPrice });

                    // Build query parameters
                    const params = new URLSearchParams();
                    
                    // Add selected cuisines
                    cuisines.forEach(cuisine => {
                        if (cuisine) params.append('cuisine', cuisine);
                    });
                    
                    // Add selected locations
                    locations.forEach(location => {
                        if (location) params.append('location', location);
                    });
                    
                    // Add rating if selected
                    if (rating) {
                        params.append('min_rating', rating);
                    }
                    
                    // Add minimum price if specified
                    if (minPrice) {
                        params.append('min_price', minPrice);
                    }

                    // Preserve existing search term if any
                    const searchInput = document.getElementById('restSearch');
                    const searchTerm = searchInput ? searchInput.value : '';
                    if (searchTerm) {
                        params.append('name_filter', searchTerm);
                    }

                    // Navigate to filtered results
                    const url = `${window.location.pathname}?${params.toString()}`;
                    console.log('Final URL to navigate to:', url);
                    
                    // Force navigation
                    console.log('About to navigate...');
                    window.location.href = url;
                    
                } catch (error) {
                    console.error('Error applying filters:', error);
                    alert('Error applying filters: ' + error.message);
                    // Reset button state
                    applyButton.innerHTML = originalText;
                    applyButton.disabled = false;
                }
            }, 100); // Small delay to show the loading state
        });
    } else {
        console.error('Apply filters button not found! Available buttons:', 
            Array.from(document.querySelectorAll('button')).map(btn => ({
                id: btn.id, 
                text: btn.textContent.trim(),
                type: btn.type
            })));
    }

    // Handle filter reset
    const resetButton = document.querySelector('button[type="reset"]');
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            console.log('Reset filters clicked');
            
            // Reset all Choices.js instances
            Object.values(choices).forEach(choice => {
                choice.removeActiveItems();
            });

            // Reset price input
            const priceInput = document.getElementById('minPriceFilter');
            if (priceInput) priceInput.value = '';
            
            // Reset search input
            const searchInput = document.getElementById('restSearch');
            if (searchInput) searchInput.value = '';

            // Navigate to unfiltered view
            window.location.href = window.location.pathname;
        });
    }

    // Initialize filters from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    console.log('URL parameters:', urlParams.toString());
    
    // Set cuisines from URL
    const urlCuisines = urlParams.getAll('cuisine');
    if (urlCuisines.length && choices['cuisineFilter']) {
        choices['cuisineFilter'].setChoiceByValue(urlCuisines);
        console.log('Set cuisines from URL:', urlCuisines);
    }
    
    // Set locations from URL
    const urlLocations = urlParams.getAll('location');
    if (urlLocations.length && choices['locationFilter']) {
        choices['locationFilter'].setChoiceByValue(urlLocations);
        console.log('Set locations from URL:', urlLocations);
    }
    
    // Set rating from URL
    const urlRating = urlParams.get('min_rating');
    if (urlRating && choices['ratingFilter']) {
        choices['ratingFilter'].setChoiceByValue(urlRating);
        console.log('Set rating from URL:', urlRating);
    }
    
    // Set price from URL
    const urlPrice = urlParams.get('min_price');
    if (urlPrice) {
        const priceInput = document.getElementById('minPriceFilter');
        if (priceInput) {
            priceInput.value = urlPrice;
            console.log('Set price from URL:', urlPrice);
        }
    }
});
