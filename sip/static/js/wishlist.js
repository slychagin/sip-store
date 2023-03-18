/*---Add product to the wishlist after press HEART button---*/
$(document).on('click', '.add-wishlist-button', function (e){
  e.preventDefault();
  var prodId = $(this).data('index');
  var heartBtn = $('.add-wishlist-button[data-index="'+ prodId +'"]');

  $.ajax({
      type: 'POST',
      url: add_wishlist,
      data: {
          product_id: prodId,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        document.getElementById('wishlist_icon_count').innerHTML = json.qty;
        heartBtn.removeClass('add-wishlist-button');
        heartBtn.addClass('delete-wishlist-button');
        handleAlerts('alert-home', 'success', 'Додано до обраного');
      },
      error: function(xhr, errmsg, err) {
        handleAlerts('alert-home', 'danger', 'ой... щось пішло не так');
      }
  });
});


/*---Delete product from the wishlist after press HEART button---*/
$(document).on('click', '.delete-wishlist-button', function (e){
  e.preventDefault();
  var prodId = $(this).data('index');
  var heartBtn = $('.delete-wishlist-button[data-index="'+ prodId +'"]');

  $.ajax({
      type: 'POST',
      url: wishlist_delete,
      data: {
          product_id: prodId,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        document.getElementById('wishlist_icon_count').innerHTML = json.qty;
        heartBtn.removeClass('delete-wishlist-button');
        heartBtn.addClass('add-wishlist-button');
        handleAlerts('alert-home', 'success', 'Видалено з обраного');
      },
      error: function(xhr, errmsg, err) {
        handleAlerts('alert-home', 'danger', 'ой... щось пішло не так');
      }
  });
});


/*--- Add product to the wishlist after press ADD/DELETE button in product details ---*/
$(document).on('click', '.add-wish-btn', function (e){
  e.preventDefault();
  var prodId = $(this).data('index');
  var element = $('.add-wish-btn[data-index="'+ prodId +'"]');

  $.ajax({
      type: 'POST',
      url: add_wishlist,
      data: {
          product_id: prodId,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        document.getElementById('wishlist_icon_count').innerHTML = json.qty;
        element.addClass('del-wish-btn');
        element.removeClass('add-wish-btn');
      },
      error: function(xhr, errmsg, err) {
        handleAlerts('alert-home', 'danger', 'ой... щось пішло не так');
      }
  });
});


/*---Delete product from the wishlist after press ADD/DELETE button in product details ---*/
$(document).on('click', '.del-wish-btn', function (e){
  e.preventDefault();
  var prodId = $(this).data('index');
  var element = $('.del-wish-btn[data-index="'+ prodId +'"]');

  $.ajax({
      type: 'POST',
      url: wishlist_delete,
      data: {
          product_id: prodId,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        document.getElementById('wishlist_icon_count').innerHTML = json.qty;
        element.addClass('add-wish-btn');
        element.removeClass('del-wish-btn');
      },
      error: function(xhr, errmsg, err) {
        handleAlerts('alert-home', 'danger', 'ой... щось пішло не так');
      }
  });
});


/*--- Change button name in product details when product was added to wishlist ---*/
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


/*---Add product to the cart after press ADD button in the wishlist---*/
$(document).on('click', '#wish-add-button', function (e){
  e.preventDefault();
  var prodId = $(this).data('index');
  var wishAddDiv = $(`#${prodId}wish-add-cart`);
  var wishAddBtn = $('#wish-add-button[data-index="'+ prodId +'"]')

  wishAddBtn.prop("disabled", true);
  wishAddDiv.fadeOut(300);
  setTimeout(()=>{
        wishAddBtn.prop("disabled", false);
  }, 600)
  wishAddDiv.fadeIn(300);

  $.ajax({
      type: 'POST',
      url: add_cart,
      data: {
          product_id: prodId,
          quantity: 1,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        document.getElementById('cart_icon_count').innerHTML = json.qty;
        handleAlerts('alert-wish', 'success', 'Додано до кошику');
      },
      error: function(xhr, errmsg, err) {
        handleAlerts('alert-wish', 'danger', 'ой... щось пішло не так');
      }
  });
});


/*---Delete product from the wishlist by press X icon---*/
$(document).on('click', '#wish-delete-button', function (e){
  e.preventDefault();
  var prodId = $(this).data('index');
  var spinnerBox = $(`#${prodId}spinner-wish-box`);

  spinnerBox.removeClass('not-visible');
  
  $.ajax({
      type: 'POST',
      url: wishlist_delete,
      data: {
          product_id: prodId,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
      setTimeout(()=>{
        $('.product-wishlist-item[data-index="'+ prodId +'"]').remove();
        }, 500);
        document.getElementById('wishlist_icon_count').innerHTML = json.qty;
      },
      error: function(xhr, errmsg, err) {}
  });
});