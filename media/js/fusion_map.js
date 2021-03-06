var FusionMap = { map: null,  infoWindow: null, unique_loc: {}, markers: [], markerClusterer: null
};

FusionMap.centerMap = function() {
	var bounds = new google.maps.LatLngBounds();
	//  Go through each...
	$.each(FusionMap.markers, function(index, marker){
		bounds.extend(marker.position);
	});
	FusionMap.map.fitBounds(bounds);
},

FusionMap.createMarker = function(lat, lng, desc, thumb, url, fusioncount) {
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
	  content: 
	  	'<a href="' + url + '">' + 
		desc + 
		'<br/><img src="' + thumb + '" />' + 
		((fusioncount > 0) ? '<br/><b>' + fusioncount + ' fusion' + ((fusioncount > 1) ? 's' :'') + '</b>' : '') + 
		'</a>'
	});
	marker.setIcon(thumb);
	if (fusioncount > 0) {
		marker.hasFusion = true;
		marker.setAnimation(google.maps.Animation.BOUNCE);
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
				thumb = $(this).find('field[name="thumburl"]').text();
				hasfusionnode = $(this).find('field[name="hasfusion"]')
				fusioncount = hasfusionnode.attr('fusioncount');
				if (fusioncount > 0) {
					lat = hasfusionnode.attr('latitude');
					lng = hasfusionnode.attr('longitude');
				}
				url = '/' + type + '/view/' + id + '/';
				markers.push(FusionMap.createMarker(lat, lng, desc, thumb, url, fusioncount));
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
	FusionMap.markerClusterer = new MarkerClusterer(FusionMap.map, FusionMap.markers, { maxZoom: 16 });
	FusionMap.centerMap();

}

$(FusionMap.init());
$(
	$('#hideunfused').click(function() {
		if (FusionMap.markerClusterer) {
			FusionMap.markerClusterer.clearMarkers();
		}
		if (!this.checked) {
			FusionMap.markerClusterer = new MarkerClusterer(FusionMap.map, FusionMap.markers, { maxZoom: 16 });
		} else {
			fusionsonly = $.grep(FusionMap.markers, function(el, i){
  				return el.hasFusion;
			});
			FusionMap.markerClusterer = new MarkerClusterer(FusionMap.map, fusionsonly, { maxZoom: 16 });
		}
//		FusionMap.centerMap();
	})
); 
