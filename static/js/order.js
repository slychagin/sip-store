/*---Show or hide delivery method---*/
$(document).on('change', '#delivery-method', function (e){
  e.preventDefault();

  let method = $('#delivery-method option:selected').val()

  let city = document.getElementById('city-address');
  let street = document.getElementById('street-address');
  let house = document.getElementById('house-address');
  let room = document.getElementById('room-address');
  let post = document.getElementById('new-post');

    if (method == 'DELIVERY COMPANY') {
    city.style.display = 'none';
    street.style.display = 'none';
    house.style.display = 'none';
    room.style.display = 'none';
    post.removeAttribute("hidden");
    post.style.display = 'block';
  } else if (method == 'COURIER') {
    city.style.display = 'block';
    street.style.display = 'block';
    house.style.display = 'block';
    room.style.display = 'block';
    post.style.display = 'none';
  }

  $.ajax({
      type: 'POST',
      url: order_form,
      data: {
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {

        if (method == 'DELIVERY COMPANY') {
            $('#city').val('-');
            $('#street').val('-');
            $('#house').val('-');
            $('#room').val('-');
            $('#post-city').val('');
            $('#post-terminal').val('');
        } else if (method == 'COURIER') {
            $('#post-city').val('-');
            $('#post-terminal').val('-');
            $('#city').val('');
            $('#street').val('');
            $('#house').val('');
            $('#room').val('');
  }
      },
      error: function(xhr, errmsg, err) {}
  });
});