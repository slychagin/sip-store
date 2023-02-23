/*---Search New Post Cities---*/
$( function() {
    $( "#post-city" ).autocomplete({
      source: post_city_search,
      minLength: 1,

      select: function (event, ui) {
				$("#post-city").val(ui.item.label);
				var getCity=ui.item.value;
				callback2Function(getCity);
			}
      })
    });

/*---Send city name to python view---*/
function callback2Function(value){
	var city = value;
	$.ajax({
      type: 'POST',
      url: post_terminal_search,
      data: {
          city_name: city,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
      },
      error: function(xhr, errmsg, err) {}
  });

}

/*---Search New Post Terminals---*/
$(function() {
    $( "#post-terminal" ).autocomplete({
      source: post_terminal_search,
      minLength: 0,
      maxShowItems: 10,
    }).focus(function() {
        $(this).autocomplete('search', '');
    });
  });
