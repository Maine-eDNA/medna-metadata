// https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
const attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
const map = L.map('map')
// create the map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: attribution
}).addTo(map);

var markersGroup = new L.markerClusterGroup();

// grab markers context from ProjectSurveyListView
const markers = JSON.parse(document.getElementById('markers-data').textContent);

var geoJsonLayer = L.geoJSON(markers, {
          onEachFeature: function (feature, layer) {
              layer.bindPopup(feature.properties.site_name);
              }
          });

markersGroup.addLayer(geoJsonLayer);

map.addLayer(markersGroup);

map.fitBounds(geoJsonLayer.getBounds(), { padding: [100, 100] });