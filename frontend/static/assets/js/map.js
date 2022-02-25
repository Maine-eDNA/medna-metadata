const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
const map = L.map('map')
// create the map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: attribution
}).addTo(map);
/*
var geojsonMarkerOptions = {
    radius: 8,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};
*/
// grab markers context from ProjectSurveyListView
const markers = JSON.parse(document.getElementById('markers-data').textContent);

let feature = L.geoJSON(markers, {
    pointToLayer: function(feature, latlng) {
    return L.MarkerClusterGroup();
    }
}).bindPopup(function (layer) { return layer.feature.properties.site_name; }).addTo(map);

map.fitBounds(feature.getBounds(), { padding: [1000, 1000] });