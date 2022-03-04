// https://www.paulox.net/2020/12/08/maps-with-django-part-1-geodjango-spatialite-and-leaflet/
// https://stackoverflow.com/questions/29824478/leaflet-markercluster-with-geojson
// https://github.com/Leaflet/Leaflet.markercluster
// https://leafletjs.com/examples/geojson/
$(function () {

    var $map = $("#map");

    $.ajax({
        url: $map.data("url"),
        success: function (data) {

        var markers = JSON.parse(data);
        var geoJsonLayer = L.geoJSON(markers, {
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.site_name);
            }
        });

        // the information in this tag is no longer being used, so remove the content from the page
        //document.getElementById('markers-data').remove()

        //console.log(geoJsonLayer.getLayers().length);
        if (geoJsonLayer.getLayers().length == 0) {
            document.getElementById('map').remove()
            // update the page to notify the user that there are no records
            document.getElementById('map_empty').textContent="This project does not have any survey records.";
        } else {
            document.getElementById('map_empty').remove()
            var markersGroup = new L.markerClusterGroup();
            var attribution = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            var map = L.map('map')

            // create the map
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: attribution
            }).addTo(map);

            markersGroup.addLayer(geoJsonLayer);

            map.addLayer(markersGroup);

            map.fitBounds(geoJsonLayer.getBounds(), { padding: [100, 100] });
        };

    }
  });

});