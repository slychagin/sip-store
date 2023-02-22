/*---Search New Post---*/
$(document).on('keyup', '#post-city', function (e){
  e.preventDefault();

  $.ajax({
      type: 'POST',
      url: post_search,
      data: {
          ss: $('#post-city').val(),
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'post'
      },
      success: function (json) {
        console.log('json.search_string')
      },
      error: function(xhr, errmsg, err) {}
  });
});