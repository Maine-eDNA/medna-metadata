// site functionality
$(window).on('map:init', function (e) {
    var detail = e.originalEvent ?
                 e.originalEvent.detail : e.detail;
    drawnItems = L.featureGroup().addTo(detail.map);

    // subclass L.GeometryField.extend in leaflet.forms.js within django-leaflet app to allow
    // edit of drawnItems. This makes it so that markers can be programmatically
    // added to the map - e.g., by user submitted text field.
    allowEditLeaflet = L.GeometryField.extend({
        _controlDrawOptions: function () {
            return {
                edit: {
                    featureGroup: drawnItems,
                    remove: true
                },
                draw: {
                    polyline: this.options.is_linestring,
                    polygon: this.options.is_polygon,
                    circle: false, // Turns off this drawing tool
                    rectangle: this.options.is_polygon,
                    marker: this.options.is_point,
                }
            };
        }
    });

    // when manual-latlng button is clicked ("Jump there"), call updateLatlng() function
    document.getElementById("manual-latlng").addEventListener("click", function() {
      updateLatLng();
    } , false);

    function updateLatLng() {
        //grab lat, lon from text fields
        var lat = document.getElementById('id_lat').value;
        var lng = document.getElementById('id_lng').value;
        //grab number of layers at lat, lon location
        var num_layers = drawnItems.getLayers().length;
        if (num_layers>0) {
            // if the number of layers is greater than 0, then there is a watershed
            // at the point
            //console.log(num_layers);
            //console.log([lat,lng]);
            drawnItems.eachLayer(function(layer){
                layer.setLatLng([lat,lng]);
                content = getPopupContent(layer);
                watershed_content = getWatershedContent(layer);
                combined_content = content + '<br> ' + watershed_content;
                layer.setPopupContent(combined_content);
                // update geom submission based on user supplied lat/lngs
                geom_txt = '{"type":"Point","coordinates":['+lng+','+lat+']}';
                document.getElementById('id_geom').value = geom_txt;
                document.getElementById('readonly_id_geom').value = geom_txt;
                detail.map.panTo([lat,lng]);
            });
            } else {
                //console.log(num_layers);
                //console.log([lat,lng]);
                var marker = new L.Marker([lat,lng]);
                drawnItems.addLayer(marker);
                drawnItems.eachLayer(function(layer){
                    var content = getPopupContent(layer);
                    var watershed_content = getWatershedContent(layer);
                    var combined_content = content + '<br> ' + watershed_content;
                    layer.bindPopup(combined_content);
                    // update geom submission based on user supplied lat/lngs
                    geom_txt = '{"type":"Point","coordinates":['+lng+','+lat+']}';
                    document.getElementById('id_geom').value = geom_txt;
                    document.getElementById('readonly_id_geom').value = geom_txt;
                    detail.map.panTo([lat,lng]);
                });
            }
    }

    function style (feature) {
        return {
        // some style here
        };
    }

    // Truncate value based on number of decimals
    var _round = function(num, len) {
        return Math.round(num*(Math.pow(10, len)))/(Math.pow(10, len));
    };
    // Helper method to format LatLng object (x.xxxxxx, y.yyyyyy)
    var strLatLng = function(latlng) {
        return "("+_round(latlng.lat, 6)+", "+_round(latlng.lng, 6)+")";
    };

    // Generate popup content based on layer type
    // - Returns HTML string, or null if unknown object
    var getPopupContent = function(layer) {
        // Marker - add lat/long
        if (layer instanceof L.Marker || layer instanceof L.CircleMarker) {
            return strLatLng(layer.getLatLng());
        // Circle - lat/long, radius
        } else if (layer instanceof L.Circle) {
            var center = layer.getLatLng(),
                radius = layer.getRadius();
            return "Center: "+strLatLng(center)+"<br />"
                  +"Radius: "+_round(radius, 2)+" m";
        // Rectangle/Polygon - area
        } else if (layer instanceof L.Polygon) {
            var latlngs = layer._defaultShape ? layer._defaultShape() : layer.getLatLngs(),
                area = L.GeometryUtil.geodesicArea(latlngs);
            return "Area: "+L.GeometryUtil.readableArea(area, true);
        // Polyline - distance
        } else if (layer instanceof L.Polyline) {
            var latlngs = layer._defaultShape ? layer._defaultShape() : layer.getLatLngs(),
                distance = 0;
            if (latlngs.length < 2) {
                return "Distance: N/A";
            } else {
                for (var i = 0; i < latlngs.length-1; i++) {
                    distance += latlngs[i].distanceTo(latlngs[i+1]);
                }
                return "Distance: "+_round(distance, 2)+" m";
            }
        }
        return null;
    };

    $.ajax({
        url: window.location.origin+"/dashboard/geom/fieldsite/",
        success: function (data) {
            var geojsonMarkerOptions = {
                radius: 5,
                fillColor: "#ff7800",
                color: "#000",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8
            };
            var geoJsonLayer = L.geoJSON(data, {
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng, geojsonMarkerOptions);
                },
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(feature.properties.site_id);
                }
            });
            // add watershed query to map
            drawnItems.addLayer(geoJsonLayer);
        }
    });

        function httpGet(Url)
        {
            // https://stackoverflow.com/questions/247483/http-get-request-in-javascript
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", Url, false ); // false for synchronous request
            xmlHttp.send( null );
            var data = JSON.parse(xmlHttp.responseText)
            return data;
        }

    var getWatershedContent = function(layer) {
        // get latitude and longitude of point
        var latlng = layer.getLatLng();
        var srid = 4326;
        var geturl = window.location.origin+"/dashboard/intersect/point/watershed/"+latlng.lat+"/"+latlng.lng+"/"+srid+"/";
        // find all intersections with the point within the watershedLayer

        var watershed_results = httpGet(geturl);
        //console.log(watershed_results);

        var geoJsonLayer = L.geoJSON(watershed_results, {
            onEachFeature: function (feature, layer) {
                layer.bindPopup(feature.properties.watershed_label);
            }
        });
                // add watershed query to map
                //drawnItems.addLayer(geoJsonLayer);

                //var watershed_results = leafletPip.pointInLayer(latlng, watershedLayer);
                var reg_click = "---------";
                var num_results = geoJsonLayer.getLayers().length;
                //console.log(num_results);
                if (num_results>0) {
                    //if(detail.map.hasLayer(watershedLayer)){
                    // find the feature (watershed) that the point intersects
                    var click_reg_code = geoJsonLayer.getLayers()[0].feature.properties.watershed_code.toString();
                    var click_reg_lab = geoJsonLayer.getLayers()[0].feature.properties.watershed_label.toString();
                    reg_click = click_reg_code + ": " + click_reg_lab;
                    //}

                    // find the id of the drop-down menu that matches the label based
                    // on clicking on the map
                    var dd = document.getElementById('id_watershed');
                    for (var i = 0; i < dd.options.length; i++) {
                        if (dd.options[i].text === reg_click) {
                            //dd.selectedIndex = i;
                            $('#id_watershed').val(i).trigger('change');
                            break;
                        }
                    }
                } else {
                    clearSelectedWatershed();
                    reg_click = "NW: No Watershed";
                }
        return(reg_click);
    }

    var clearSelectedWatershed = function(){
    /*
        var dd = document.getElementById('id_watershed');
        for (var i = 0; i < dd.options.length; i++) {
          dd.options[i].selected = false;
        }
    */
        $('#id_watershed').val(null).trigger('change');
    }

    detail.map.on('draw:created', function (e) {
        var num_layers = drawnItems.getLayers().length;
        if (num_layers>0) {
            drawnItems.clearLayers();
        }
        var layer = e.layer;
        var content = getPopupContent(layer);
        var watershed_content = getWatershedContent(layer);
        var combined_content = content + '<br> ' + watershed_content
        if (content !== null) {
            layer.bindPopup(combined_content);
            var lat = _round(layer.getLatLng().lat, 6);
            var lng = _round(layer.getLatLng().lng, 6);
            document.getElementById('id_lat').value = lat;
            document.getElementById('id_lng').value = lng;
            // update geom submission based on user supplied lat/lngs
            geom_txt = '{"type":"Point","coordinates":['+lng+','+lat+']}';
            document.getElementById('id_geom').value = geom_txt;
            document.getElementById('readonly_id_geom').value = geom_txt;
        }
        drawnItems.addLayer(layer);
    });


    // Object(s) edited - update popups
    detail.map.on('draw:edited', function (e) {
        var layers = e.layers,
            content = null,
            watershed_content = null,
            combined_content = null;
        layers.eachLayer(function(layer) {
        // if a layer is edited, update the content of the popup
            content = getPopupContent(layer);
            watershed_content = getWatershedContent(layer);
            combined_content = content + '<br> ' + watershed_content
            if (content !== null) {
                layer.setPopupContent(combined_content);
                var lat = _round(layer.getLatLng().lat, 6);
                var lng = _round(layer.getLatLng().lng, 6);
                document.getElementById('id_lat').value = lat;
                document.getElementById('id_lng').value = lng;
                // update geom submission based on user supplied lat/lngs
                geom_txt = '{"type":"Point","coordinates":['+lng+','+lat+']}';
                document.getElementById('id_geom').value = geom_txt;
                document.getElementById('readonly_id_geom').value = geom_txt;
            }
        });
    });

    detail.map.on('draw:deleted', function(e) {
        var layers = e.layers,
            content = null,
            watershed_content = null,
            combined_content = null;
        layers.eachLayer(function(layer){
            // if the drawn point is deleted, then clear the watershed selection
            // from the drop-down menu. If save with no delete, do nothing.
            clearSelectedWatershed();
            document.getElementById('id_lat').value = null;
            document.getElementById('id_lng').value = null;
            document.getElementById('readonly_id_geom').value = null;
            document.getElementById('id_geom').value = null;
            drawnItems.removeLayer(layer);
         });
    });
});