function vote(type, id, direction, csrf_token) {
    $.post('/'+type+'/'+id+'/'+direction+'vote/', {HTTP_X_REQUESTED:'XMLHttpRequest', csrfmiddlewaretoken:csrf_token},
           function(data) {
               if (data.success == true) {
                   $('#score').text(data.score.score);
                   $('#num_votes').text(data.score.num_votes);
               } else {
                   alert('ERROR: ' + data.error_message);
               }
           }, 'json'
          );
}
