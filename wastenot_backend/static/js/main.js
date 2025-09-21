// Main JavaScript for WasteNot

// Image preview functionality
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imagePreview').src = e.target.result;
            document.getElementById('imagePreview').style.display = 'block';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Form validation
function validateForm() {
    const title = document.getElementById('itemTitle').value;
    const description = document.getElementById('itemDescription').value;
    const category = document.getElementById('itemCategory').value;

    if (!title || !description || !category) {
        alert('Please fill in all required fields');
        return false;
    }
    return true;
}

// Dynamic location handling
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                document.getElementById('latitude').value = position.coords.latitude;
                document.getElementById('longitude').value = position.coords.longitude;
            },
            error => {
                console.error('Error getting location:', error);
            }
        );
    }
}

// Item search functionality
function searchItems(query) {
    fetch(`/api/items/?search=${query}`)
        .then(response => response.json())
        .then(data => {
            updateItemsList(data);
        })
        .catch(error => console.error('Error:', error));
}

// Update items list in the DOM
function updateItemsList(items) {
    const container = document.getElementById('itemsContainer');
    container.innerHTML = '';
    
    items.forEach(item => {
        const itemElement = createItemElement(item);
        container.appendChild(itemElement);
    });
}

// Create item card element
function createItemElement(item) {
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `
        <img src="${item.images[0]?.image || '/static/images/placeholder.png'}" 
             alt="${item.title}" class="card-img">
        <div class="card-body">
            <h3>${item.title}</h3>
            <p>${item.description}</p>
            <span class="badge">${item.category_name}</span>
            <button onclick="contactOwner(${item.id})" class="btn-primary">
                Contact Owner
            </button>
        </div>
    `;
    return div;
} 