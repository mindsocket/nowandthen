var FusionMap = { map: null,  infoWindow: null, unique_loc: {}, markers: []
};

FusionMap.centerMap = function() {
	var bounds = new google.maps.LatLngBounds();
	//  Go through each...
	$.each(FusionMap.markers, function(index, marker){
		bounds.extend(marker.position);
	});
	FusionMap.map.fitBounds(bounds);
},

FusionMap.createMarker = function(lat, lng, desc, thumb, url, type) {
//	console.log("creating" + lat + lng + desc);
	var key = lat + ',' + lng;
	// Move markers a little if they overlap
	while (FusionMap.unique_loc[key]) {
//		console.log("deduping" + lat + lng + desc);
		lng = parseFloat(lng) + 0.0001;
		key = lat + ',' + lng;
	}
	FusionMap.unique_loc[key] = true;
	myLatLng = new google.maps.LatLng(lat, lng);
	var marker = new google.maps.Marker({
	  position: myLatLng, 
	  title: desc,
	  content: '<a href="' + url + '">' + desc + '<br/><img src="' + thumb + '" /></a>'
	});
	if (type == 'fusion') {
		marker.setIcon(thumb);
	}

	google.maps.event.addListener(marker, 'click', function() {
		FusionMap.infoWindow.setContent(marker.content);
    	FusionMap.infoWindow.open(FusionMap.map,marker);
    });
	return marker;  
};

FusionMap.createMarkers = function(type) {
	var markers = new Array();
	$.ajax({
		url: '/' + type + '/map/xml',
		dataType: 'xml',
		async: false,
		error: function(jqXHR, textStatus, errorThrown) {alert('fail:' + textStatus)},
		success: function(data, textStatus, jqHXR) {
			$(data).find("object").each(function() {
				id = $(this).attr('pk');
				desc = $(this).find('field[name="description"]').text();
				lat = $(this).find('field[name="latitude"]').text();
				lng = $(this).find('field[name="longitude"]').text();
				if (type == 'fusion') {
					// TODO	thumb = $(this).find('field[name="thumburl"]').text();
				} else {
					thumb = $(this).find('field[name="thumburl"]').text();
				}
				url = '/' + type + '/view/' + id + '/';
				markers.push(FusionMap.createMarker(lat, lng, desc, thumb, url));
			});
		}
	});

	return markers;
},


/**
 * Called when clicking anywhere on the map and closes the info window.
 */
FusionMap.closeInfoWindow = function() {
  FusionMap.infoWindow.close();
},

/**
 * Opens the shared info window, anchors it to the specified marker, and
 * displays the marker's position as its content.
 */
FusionMap.openInfoWindow = function(marker) {
  FusionMap.infoWindow.setContent(marker.content);
  FusionMap.infoWindow.open(FusionMap.map, marker);
},

/**
 * Called only once on initial page load to initialize the map.
 */
FusionMap.init = function() {
	console.log("init");
	var sydney = new google.maps.LatLng(-33.852, 151.199);
	var myOptions = {
		zoom: 14,
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		center: sydney
	};
	FusionMap.map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

  // Create a single instance of the InfoWindow object which will be shared
  // by all Map objects to display information to the user.
  FusionMap.infoWindow = new google.maps.InfoWindow();

  // Make the info window close when clicking anywhere on the map.
  google.maps.event.addListener(FusionMap.map, 'click', FusionMap.closeInfoWindow);

//	FusionMap.markers = FusionMap.markers.concat(FusionMap.createMarkers('fusion'));
	FusionMap.markers = FusionMap.markers.concat(FusionMap.createMarkers('image'));
	var mc = new MarkerClusterer(FusionMap.map, FusionMap.markers, { maxZoom: 16 });
	FusionMap.centerMap();

}

$(FusionMap.init());
