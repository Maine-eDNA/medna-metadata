// site functionality
$(window).on('map:init', function (e) {
    var detail = e.originalEvent ?
                 e.originalEvent.detail : e.detail;
    drawnItems = L.featureGroup().addTo(detail.map);
    // draw region layer on map
    regionLayer = L.geoJson(regionData);

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
            // if the number of layers is greater than 0, then there is a region
            // at the point
            //console.log(num_layers);
            //console.log([lat,lng]);
            drawnItems.eachLayer(function(layer){
                layer.setLatLng([lat,lng]);
                content = getPopupContent(layer);
                region_content = getRegionContent(layer);
                combined_content = content + '<br> ' + region_content;
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
                    var region_content = getRegionContent(layer);
                    var combined_content = content + '<br> ' + region_content;
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

    var getRegionContent = function(layer) {
        // get latitude and longitude of point
        var latlng = layer.getLatLng();
        // find all intersections with the point within the regionLayer
        var region_results = leafletPip.pointInLayer(latlng, regionLayer);
        var reg_click = "---------";
        var num_results = region_results.length;
        //console.log(num_results);
        if (num_results>0) {
            //if(detail.map.hasLayer(regionLayer)){
            // find the feature (region) that the point intersects
            var click_reg_code = region_results[0].feature.properties.region_code.toString();
            var click_reg_lab = region_results[0].feature.properties.region_label.toString();
            reg_click = click_reg_code + ": " + click_reg_lab;
            //}

            // find the id of the drop-down menu that matches the label based
            // on clicking on the map
            var dd = document.getElementById('id_region');
            for (var i = 0; i < dd.options.length; i++) {
                if (dd.options[i].text === reg_click) {
                    dd.selectedIndex = i;
                    break;
                }
            }
        } else {
            clearSelectedRegion();
            reg_click = "NR: No Region";
        }
       return(reg_click);
    }

    var clearSelectedRegion = function(){
        var dd = document.getElementById('id_region');
        for (var i = 0; i < dd.options.length; i++) {
          dd.options[i].selected = false;
        }
    }

    detail.map.on('draw:created', function (e) {
        var num_layers = drawnItems.getLayers().length;
        if (num_layers>0) {
            drawnItems.clearLayers();
        }
        var layer = e.layer;
        var content = getPopupContent(layer);
        var region_content = getRegionContent(layer);
        var combined_content = content + '<br> ' + region_content
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
            region_content = null,
            combined_content = null;
        layers.eachLayer(function(layer) {
        // if a layer is edited, update the content of the popup
            content = getPopupContent(layer);
            region_content = getRegionContent(layer);
            combined_content = content + '<br> ' + region_content
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
            region_content = null,
            combined_content = null;
        layers.eachLayer(function(layer){
            // if the drawn point is deleted, then clear the region selection
            // from the drop-down menu. If save with no delete, do nothing.
            clearSelectedRegion();
            document.getElementById('id_lat').value = null;
            document.getElementById('id_lng').value = null;
            document.getElementById('readonly_id_geom').value = null;
            document.getElementById('id_geom').value = null;
            drawnItems.removeLayer(layer);
         });
    });

    function onEachFeature(feature, layer) {
        // on hover show region code and region label
        var hover_reg_code = feature.properties.region_code.toString();
        var hover_reg_lab = feature.properties.region_label.toString();
        var reg_hover = hover_reg_code + ": " + hover_reg_lab;
        layer.bindTooltip(reg_hover);
        /*
        //bind click
        layer.on('click', function (e) {
          // e = event
          var click_reg_code = e.target.feature.properties.region_code.toString();
          var click_reg_lab = e.target.feature.properties.region_label.toString();
          var reg_click = click_reg_code + ": " + click_reg_lab;
          // find the id of the drop-down menu that matches the label based
          // on clicking on the map
          var dd = document.getElementById('id_region');
          for (var i = 0; i < dd.options.length; i++) {
            if (dd.options[i].text === reg_click) {
                dd.selectedIndex = i;
                break;
            }
          }
          //alert(reg_click);
          // You can make your ajax call declaration here
          //$.ajax(...
        });
        */
    }

    L.geoJson(regionData, {
    style: style,
    onEachFeature: onEachFeature
    }).addTo(detail.map);
});