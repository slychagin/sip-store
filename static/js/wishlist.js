/*---Add or delete product to the wishlist after press HEART button---*/
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
        handleAlerts('alert-home', 'success', 'Додано до обраного');
      },
      error: function(xhr, errmsg, err) {
        handleAlerts('alert-home', 'danger', 'ой... щось пішло не так');
      }
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
      error: function(xhr, errmsg, err) {
        handleAlerts('alert-prod-details', 'danger', 'ой... щось пішло не так');
      }
  });
});

/*--- Change button name when product was added to wishlist ---*/
function toggleText(button_id) {
   var wishBtn = document.getElementById(button_id);
   if (wishBtn.firstChild.data == "+ Додати до обраного")
   {
       wishBtn.firstChild.data = "- Видалити з обраного";
       handleAlerts('alert-prod-details', 'success', 'Додано до обраного');
   }
   else
   {
     wishBtn.firstChild.data = "+ Додати до обраного";
     handleAlerts('alert-prod-details', 'success', 'Видалено з обраного');
   }
}


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
        handleAlerts('alert-wish', 'success', 'Додано до кошику');
      },
      error: function(xhr, errmsg, err) {
        andleAlerts('alert-wish', 'danger', 'ой... щось пішло не так');
      }
  });
});


/*---Delete product from the wishlist by press X icon---*/
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