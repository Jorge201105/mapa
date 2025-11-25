var map;
var markers = [];
var directionsService;
var directionsRenderer;

function initMap() {
    // Coordenadas de Santiago de Chile como centro por defecto
    var santiago = {lat: -33.4489, lng: -70.6693}; 
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: santiago
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({map: map});

    // Añadir marcadores existentes
    puntos_entrega_data.forEach(function(punto) {
        addMarker({lat: punto.latitud, lng: punto.longitud}, punto.nombre);
    });

    // Si hay puntos para dibujar una ruta (después de la optimización)
    if (puntos_entrega_data.length > 1) {
        drawOptimizedRoute();
    }
}

function addMarker(location, title) {
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        title: title
    });
    markers.push(marker);
}

function drawOptimizedRoute() {
    // Necesitas al menos 2 puntos para dibujar una ruta
    if (puntos_entrega_data.length < 2) return;

    // Asume que el primer punto de entrega es el inicio temporal para la ruta visual
    // En la optimización real, tendrías un punto de inicio fijo.
    var start = puntos_entrega_data[0];
    var end = puntos_entrega_data[puntos_entrega_data.length - 1];

    var waypoints = [];
    for (var i = 1; i < puntos_entrega_data.length -1 ; i++) {
        waypoints.push({
            location: {lat: puntos_entrega_data[i].latitud, lng: puntos_entrega_data[i].longitud},
            stopover: true
        });
    }

    directionsService.route({
        origin: {lat: start.latitud, lng: start.longitud},
        destination: {lat: end.latitud, lng: end.longitud},
        waypoints: waypoints,
        optimizeWaypoints: false, // La optimización ya la hiciste con tu IA
        travelMode: google.maps.TravelMode.DRIVING
    }, function(response, status) {
        if (status === 'OK') {
            directionsRenderer.setDirections(response);
            // Aquí puedes calcular la distancia total y el tiempo para mostrarlo al usuario
            // response.routes[0].legs.forEach(function(leg) {
            //     console.log('Distancia:', leg.distance.text, 'Duración:', leg.duration.text);
            // });
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}