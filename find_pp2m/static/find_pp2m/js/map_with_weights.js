

// document.write(best_pick.concat(" (", weighting_min.toFixed(0), ")"));



// Hexacolor from number
function componentToHex(c) {
    var hex = Math.floor(c).toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function getHexaColorFromWeighting(value, value_min) {
    if (value == value_min) {
        var valcolor = 0;
    } else if (value > 1.5 * value_min) {
        var valcolor = 255;
    } else {
        var valcolor = 25 + 450 * Math.floor(20 * (value - value_min)/value_min)/20;
    }
    return hexacolor = rgbToHex(255, valcolor, valcolor);
}

function addPolygonToCard(macarte, coords, value, value_min) {
    var markerOptions = {opacity: 1};
    var hexacolor = getHexaColorFromWeighting(value, value_min);
    markerOptions.color = hexacolor;

    var poly_latlon = JSON.parse(coords["polygon"]);
    var polygon = L.polygon(poly_latlon, {color: hexacolor, stroke: false, fill: true, fillOpacity: 0.7}).addTo(macarte);
    var popup = polygon.bindPopup(coords["name"].concat(" (", value.toFixed(2), ")"));  //
}

// Marker function
function addMarkerToCard(macarte, initial_city) {
    var marker = L.marker([initial_city["latitude"], initial_city["longitude"]]).addTo(macarte);
    var popup = marker.bindPopup(initial_city["name"]);  //
}

// Fonction pour retourner le chiffre en fonction de la méthode
function composeValue(entity, weighting, method) {
    var value = retrieveFormatedValue(weighting, method)

    var composed_value = entity + ' (' + value + ')';

    return composed_value;
}

function retrieveFormatedValue(weighting, method) {
    if (method == 'route_duration') {
        if (weighting < 1) {
            var str_mins = (weighting*60).toFixed(0);
            var value = str_mins + ' min';
        } else {
            var str_hour = Math.floor(weighting).toFixed(0);
            var str_mins = ((weighting - Math.floor(weighting))*60).toFixed(0);
            if (str_mins == '60') {
                str_hour = (Math.floor(weighting) + 1).toFixed(0);
                str_mins = '00';
            }
            if (str_mins.length == 1) {
                str_mins = '0' + str_mins;
            }
            var value = str_hour + 'h' + str_mins;
        }
    } else if (method == 'route_distance') {
        var value = weighting.toFixed(1) + ' km';
    } else if (method == 'route_distance') {
        var value = weighting.toFixed(1) + ' km';
    }

    return value;
}

// Fonction d'initialisation de la carte
function initMap(entities, weightings, initial_cities) {  
    var weighting_min = 36000;
    var weighting_max = 0;
    var best_pick = '';
    for(var i = 0; i < weightings.length; i++) {
        if (weightings[i] < weighting_min) {
            weighting_min = weightings[i]
            best_pick = entities[i]["fields"]["name"]
        }
        if (weightings[i] > weighting_max) {
            weighting_max = weightings[i]
        }
    }

    // Polygons
    for(var i = 0; i < entities.length; i++) {
        addPolygonToCard(macarte, entities[i]["fields"], weightings[i], weighting_min);
    }

    // Markers
    for(var i = 0; i < initial_cities.length; i++) {
        addMarkerToCard(macarte, initial_cities[i]["fields"]);
    }

    return macarte;
}


function changeMap(entities, weightings, initial_cities) {  
    var weighting_min = 36000;
    var weighting_max = 0;
    var best_pick = '';
    for(var i = 0; i < weightings.length; i++) {
        if (weightings[i] < weighting_min) {
            weighting_min = weightings[i]
            best_pick = entities[i]["fields"]["name"]
        }
        if (weightings[i] > weighting_max) {
            weighting_max = weightings[i]
        }
    }

    macarte.eachLayer(function (layer) {
        macarte.removeLayer(layer);
    });

    // Get maps data on openstreetmap.fr
    L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
        attribution: 'données © <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
        minZoom: 1,
        maxZoom: 10
    }).addTo(macarte);

    // Polygons
    for(var i = 0; i < entities.length; i++) {
        addPolygonToCard(macarte, entities[i]["fields"], weightings[i], weighting_min);
    }

    // Markers
    for(var i = 0; i < initial_cities.length; i++) {
        addMarkerToCard(macarte, initial_cities[i]["fields"]);
    }
}