$(function(){

	// Loop through all the sets of then and now pics
	$(".thennow").each(function(){
	
		// Set the container's size to the size of the image
		$(this).width($(this).find("img[rel=then]").attr("width")).height($(this).find("img[rel=then]").attr("height"));
	
		// Convert the images into background images on layered divs
		$(this).append("<div class='now'></div>").find(".now").css({"background": "url(" + $(this).find("img[rel=now]").attr("src") + ")", "width": $(this).find("img[rel=now]").attr("width") + "px", "height": $(this).find("img[rel=now]").attr("height")-10 + "px"});
		$(this).append("<div class='then'></div>").find(".then").css({"background": "url(" + $(this).find("img[rel=then]").attr("src") + ")", "width": $(this).find("img[rel=then]").attr("width") - 40 + "px", "height": $(this).find("img[rel=then]").attr("height")-10 + "px"});
		
		// Add a helpful message
		$(this).append("<div class='help'>Hover over the image to toggle then/now</div>");
		
		// Remove the original images
		$(this).find("img").remove();
		
		// Event handler for the mouse moving over the image
		$(this).mousemove(function(event){
			
			// Need to know the X position of the parent as people may have their browsers set to any width
			var offset = $(this).offset().left;
			
			// Don't let the reveal go any further than 20 pixels less than the width of the image
			// or 20 pixels on the left hand side
			if ((event.clientX - offset) < ($(this).find(".now").width() -20) && (event.clientX - offset) > 20) {
				// Adjust the width of the top image to match the cursor position
				$(this).find(".then").width(event.clientX - offset);
			}
			
		});
		
		// Fade out the help message now the first hover
		$(this).hover(function(){
		
			$(this).find(".help").animate({"opacity": 0}, 400, function(){ $(this).find(".help").remove(); });
			
		});
		
	});

	$(".thennowfade").each(function(){
		$(this).append("<div class='help'>Hover over the image (left to right) to fade between then/now</div>");

		$(this).mousemove(function(event){
			// Need to know the X position of the parent as people may have their browsers set to any width
			var offset = $(this).offset().left;
			amount = (event.clientX - offset)/$(this).find(".nowfade").width();
			$(this).find(".nowfade").css("opacity", amount);
			
		});
	});	
});

	
$(function(){
    function add_point() {
        $('#control_points').attr('selectedIndex', -1);                  
        $('#control_points').append('<option value="?,?,?,?" selected>?, ? -- ?, ?</option>');
    }
	add_point();

    $('#delete_points').click(function() {
        $('#control_points option:selected').remove();
    });
    
    $('.control_pointable').click(function(e) {
        current_point = $('#control_points option:selected');
        if (current_point.length == 0) {
            add_point();
            current_point = $('#control_points option:selected');
        } else if (current_point.length > 1) {
            alert("Multiple points selected, please choose 1 point and try again");
            return;
        }
		var index = $('#control_points')[0].selectedIndex;
        var offset = $(this).offset();
        clickx = e.clientX - offset.left;
        clicky = e.clientY - offset.top;
        current_values = current_point.attr('value').split(',');
		$(this).parent().find('.point-'+index).remove();
		$(this).parent().append('<span class="ui-icon ui-icon-arrowthick-1-nw point-' + index + '" style="position:absolute;left:' + clickx + 'px;top:' + clicky + 'px;"></span>');
        if ($(this).hasClass('then_edit')) {
            current_values[0] = clickx;
            current_values[1] = clicky;
        } else {
            current_values[2] = clickx;
            current_values[3] = clicky;
        }
        current_point.attr('value', current_values.join(','));
        current_point.html(current_values[0] + ', ' + current_values[1] + ' -- ' + current_values[2] + ', ' + current_values[3]);
		if (current_values[0] != '?' && current_values[2] != '?') {
			$('#fusion_form input[name="points"]').attr('value', $('#control_points option').not('[value*="?"]').map(function() {
  				return $(this).attr('value');
			}).get().join(','));
			if ($('#control_points option:last[value*="?"]').size() == 0) {
				add_point();
			}
		}
    });
});

