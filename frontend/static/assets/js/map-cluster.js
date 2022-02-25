// https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
// https://stackoverflow.com/questions/29824478/leaflet-markercluster-with-geojson
// https://github.com/Leaflet/Leaflet.markercluster
// https://leafletjs.com/examples/geojson/

// grab markers context from ProjectSurveyTemplateView
var markers = JSON.parse(document.getElementById('markers-data').textContent);
console.log(markers.length);
if (markers.length == 0) {
    document.getElementById('markers-data').textContent="";
} else {
    console.log(markers.length);
    console.log(markers);
    var markersGroup = new L.markerClusterGroup();
    var attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    var map = L.map('map')
    // create the map
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: attribution
    }).addTo(map);

    var geoJsonLayer = L.geoJSON(markers, {
        onEachFeature: function (feature, layer) {
            layer.bindPopup(feature.properties.site_name);
        }
    });

    markersGroup.addLayer(geoJsonLayer);

    map.addLayer(markersGroup);

    map.fitBounds(geoJsonLayer.getBounds(), { padding: [100, 100] });
};