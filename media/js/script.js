$(function() {
	
	$('#tabs').tabs();

	$(".votes a.vote").click(
		function(event) {
			parent = $(this).parent();
			type = parent.find('input[name=type]').val();
			current_score = $('#score').text;
			if ($(this).hasClass("vote-up-off")) {
				direction = 'up';
			} else if ($(this).hasClass("vote-up-on") || $(this).hasClass("vote-down-on")) {
				direction = 'clear';
			} else if ($(this).hasClass("vote-down-off")) {
				direction = 'down';
			}
			object_id = parent.find('input[name=object_id]').val();
			csrf_token = parent.find('input[name=csrf_token]').val();
			$.post('/'+type+'/'+object_id+'/'+direction+'vote/', {HTTP_X_REQUESTED:'XMLHttpRequest', csrfmiddlewaretoken:csrf_token},
				function(data) {
					if (data.success) {
						$('#score').text(data.score.score);
					// $('#num_votes').text(data.score.num_votes);
						if (direction === "up") {
							parent.find('.vote-up-off').removeClass('vote-up-off').addClass('vote-up-on');
							parent.find('.vote-down-on').removeClass('vote-down-on').addClass('vote-down-off');
						} else if (direction === "down") {
							parent.find('.vote-up-on').removeClass('vote-up-on').addClass('vote-up-off');
							parent.find('.vote-down-off').removeClass('vote-down-off').addClass('vote-down-on');
						} else  {
							parent.find('.vote-up-on').removeClass('vote-up-on').addClass('vote-up-off');
							parent.find('.vote-down-on').removeClass('vote-down-on').addClass('vote-down-off');
						}
					} else {
						alert('ERROR: ' + data.error_message);
					}
				}, 'json'
        	);
		}
	);
});
