function vote(type, id, direction, csrf_token) {
    $.post('/'+type+'/'+id+'/'+direction+'vote/', {HTTP_X_REQUESTED:'XMLHttpRequest', csrfmiddlewaretoken:csrf_token},
           function(data) {
               if (data.success == true) {
                   $('#score').text(data.score.score);
//                   $('#num_votes').text(data.score.num_votes);
               } else {
                   alert('ERROR: ' + data.error_message);
               }
           }, 'json'
          );
}


$(function() {
	$(".votes a.vote").click(
		function(event) {
			type = $(this).parent().find('input[name=type]').val()
			object_id = $(this).parent().find('input[name=object_id]').val()
			csrf_token = $(this).parent().find('input[name=csrf_token]').val()
			vote(type, object_id, 'up', csrf_token);
			$(this).removeClass('vote-up-off').addClass('vote-up-on');
			$(this).removeClass('vote-up-off').addClass('vote-up-on');
		}
	);
});
