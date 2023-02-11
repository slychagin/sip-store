/*---Add product to the wishlist after press heart button---*/
$(document).on('click', '.wishlist-button', function (e){
  e.preventDefault();
  var prodid = $(this).data('index');

  $.ajax({
      type: 'POST',
      url: add_wishlist,
      data: {
          product_id: prodid,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        document.getElementById('wishlist_icon_count').innerHTML = json.qty;
      },
      error: function(xhr, errmsg, err) {}
  });
});

/*---Add product to the cart after press Add button in the wishlist---*/
$(document).on('click', '#wish-add-button', function (e){
  e.preventDefault();
  var prodid = $(this).data('index');

  $.ajax({
      type: 'POST',
      url: add_cart,
      data: {
          product_id: prodid,
          quantity: 1,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        document.getElementById('cart_icon_count').innerHTML = json.qty;
      },
      error: function(xhr, errmsg, err) {}
  });
});

/*---Delete product from the wishlist---*/
$(document).on('click', '#wish-delete-button', function (e){
  e.preventDefault();
  var prodid = $(this).data('index');
  $.ajax({
      type: 'POST',
      url: wishlist_delete,
      data: {
          product_id: prodid,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        $('.product-wishlist-item[data-index="'+ prodid +'"]').remove();
        document.getElementById('wishlist_icon_count').innerHTML = json.qty;
      },
      error: function(xhr, errmsg, err) {}
  });
});

/*---Add product to the wishlist after press button in product details---*/
$(document).on('click', '#wishlist-add-button', function (e){
  e.preventDefault();
  var prodid = $(this).data('index');

  $.ajax({
      type: 'POST',
      url: add_wishlist,
      data: {
          product_id: prodid,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        document.getElementById('wishlist_icon_count').innerHTML = json.qty;
      },
      error: function(xhr, errmsg, err) {}
  });
});

/*---Delete product from the wishlist when press delete in the product details---*/
$(document).on('click', '#wishlist-delete', function (e){
  e.preventDefault();
  var prodid = $(this).data('index');
  $.ajax({
      type: 'POST',
      url: wishlist_delete,
      data: {
          product_id: prodid,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        $('.product-wishlist-item[data-index="'+ prodid +'"]').remove();
        document.getElementById('wishlist_icon_count').innerHTML = json.qty;
      },
      error: function(xhr, errmsg, err) {}
  });
});