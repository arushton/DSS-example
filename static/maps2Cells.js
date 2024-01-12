const map = L.map('map').setView([55, -3], 5);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

let currentCells = [];
let lastBounds = null;
const zoomLevelDisplay = document.getElementById('zoom-level-display');

function updateZoomLevelDisplay() {
    zoomLevelDisplay.textContent = `Zoom Level: ${map.getZoom()}`;
}

function boundsSignificantlyChanged(newBounds) {
    if (!lastBounds) return true;
    return !lastBounds.equals(newBounds);
}

function loadS2Cells() {
    const bounds = map.getBounds();
    if (!boundsSignificantlyChanged(bounds)) return;

    lastBounds = bounds;
    currentCells.forEach(cell => map.removeLayer(cell));
    currentCells = [];

    fetch(`/get_s2_cells_data/${map.getZoom()}/${bounds.getSouthWest().lat}/${bounds.getSouthWest().lng}/${bounds.getNorthEast().lat}/${bounds.getNorthEast().lng}`)
        .then(response => response.json())
        .then(cells => cells.forEach(cellData => drawCell(cellData)))
        .catch(error => console.error('Error loading S2 cells:', error));
}

function drawCell(cellData) {
    const cellVertices = cellData.vertices.map(v => [v.lat, v.lng]);
    const cellPolygon = L.polygon(cellVertices, {
        color: 'red',
        weight: 1,
        fillOpacity: 0.2
    }).addTo(map);
    currentCells.push(cellPolygon);
}

function updatePolygonStyles() {
    currentCells.forEach(cell => {
        cell.setStyle({
            fillOpacity: 0.2
        });
    });
}

map.on('zoomend', function() {
    updateZoomLevelDisplay();
    updatePolygonStyles();
});

map.on('moveend', function() {
    updatePolygonStyles();
    loadS2Cells();
});

updateZoomLevelDisplay();
loadS2Cells();
