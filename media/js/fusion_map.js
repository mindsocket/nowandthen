var initialLocation;
var sydney = new google.maps.LatLng(-33.852, 151.199);
var browserSupportFlag =  new Boolean();
var map;
var infowindow = new google.maps.InfoWindow();

function addMarker(lat,lng,desc,thumb,url) {
	myLatLng = new google.maps.LatLng(lat, lng);
	var marker = new google.maps.Marker({
	  position: myLatLng, 
	  map: map,
	  title: desc
	});
	var infowindow = new google.maps.InfoWindow({
        content: '<a href="' + url + '">' + desc + '<br/><img src="' + thumb + '" /></a>'
    });
	google.maps.event.addListener(marker, 'click', function() {
    	infowindow.open(map,marker);
    });
	return marker;  
}

function addMarkers(type) {
		$.ajax({
		url: '/' + type + '/map/xml',
		dataType: 'xml',
		error: function(jqXHR, textStatus, errorThrown) {alert('fail:' + textStatus)},
		success: function(data, textStatus, jqHXR) {
			$(data).find("object").each(function() {
				id = $(this).attr('pk');
				desc = $(this).find('field[name="description"]').text();
				lat = $(this).find('field[name="latitude"]').text();
				lng = $(this).find('field[name="longitude"]').text();
				thumb = $(this).find('field[name="thumburl"]').text();
				url = '/' + type + '/view/' + id + '/';
				addMarker(lat,lng,desc,thumb,url);
			});
		}
	});

}
function initialise() {
	
	var myOptions = {
		zoom: 14,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
    map.setCenter(sydney);
    infowindow.setPosition(sydney);
    infowindow.open(map);

	addMarkers('image');
//	addMarkers('fusion');
}
$(initialise);

/*  // Try W3C Geolocation method (Preferred)
  if(navigator.geolocation) {
    browserSupportFlag = true;
    navigator.geolocation.getCurrentPosition(function(position) {
      initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
      contentString = "Location found using W3C standard";
      map.setCenter(initialLocation);
      infowindow.setContent(contentString);
      infowindow.setPosition(initialLocation);
      infowindow.open(map);
      getData(position.coords.longitude,position.coords.latitude);
    }, function() {
      handleNoGeolocation(browserSupportFlag);
    });
  } else if (google.gears) {
    // Try Google Gears Geolocation
    browserSupportFlag = true;
    var geo = google.gears.factory.create('beta.geolocation');
    geo.getCurrentPosition(function(position) {
      initialLocation = new google.maps.LatLng(position.latitude,position.longitude);
      contentString = "Location found using Google Gears";
      map.setCenter(initialLocation);
      infowindow.setContent(contentString);
      infowindow.setPosition(initialLocation);
      infowindow.open(map);
      getData(position.coords.longitude,position.coords.latitude);
    }, function() {
      handleNoGeolocation(browserSupportFlag);
    });
  } else {
    // Browser doesn't support Geolocation
    browserSupportFlag = false;
    handleNoGeolocation(browserSupportFlag);
  }*/
/*
function handleNoGeolocation(errorFlag) {
  contentString = "Couldn't determine your location";

  map.setCenter(sydney);
  infowindow.setContent(contentString);
  infowindow.setPosition(sydney);
  infowindow.open(map);
  getData(151.179,-33.842);
  
}
*/