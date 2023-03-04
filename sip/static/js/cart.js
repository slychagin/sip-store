/*---Add product to the cart after press Add button in product details page---*/
$(document).on('click', '#add-button', function (e){
  e.preventDefault();
  var prodid = $('#add-button').val();

  $.ajax({
      type: 'POST',
      url: add_cart,
      data: {
          product_id: prodid,
          quantity: $('#qty').val(),
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        document.getElementById('cart_icon_count').innerHTML = json.qty;
        handleAlerts('alert-prod-details', 'success', 'Додано до кошику');
      },
      error: function(xhr, errmsg, err) {
        handleAlerts('alert-prod-details', 'danger', 'ой... щось пішло не так');
      }
  });
});

/*---Delete product from the basket---*/
$(document).on('click', '.delete-button', function (e){
  e.preventDefault();
  var prodid = $(this).data('index');
  $.ajax({
      type: 'POST',
      url: cart_delete,
      data: {
          product_id: prodid,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        $('.product-item[data-index="'+ prodid +'"]').remove();
        document.getElementById('total').innerHTML = json.total;
        document.getElementById('cart_icon_count').innerHTML = json.qty;
        if (json.qty === 0) {
            window.location.reload();
        }
      },
      error: function(xhr, errmsg, err) {}
  });
});

/*---Delete product from the mini cart by press delete icon---*/
$(document).on('click', '.delete-icon', function (e){
    e.preventDefault();
    var prodid = $(this).data('index');
    $.ajax({
        type: 'POST',
        url: mini_cart_delete,
        data: {
            product_id: prodid,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            action: 'POST'
        },
        success: function (json) {
          $('.cart_item[data-index="'+ prodid +'"]').remove();
          document.getElementById('mini-cart-total').innerHTML = json.mini_cart_total;
          document.getElementById('cart_icon_count').innerHTML = json.qty;
        },
        error: function(xhr, errmsg, err) {}
    });
});

/*---Add quantity by press plus button in the cart page---*/
$(document).on('click', '.button-plus', function (e){
      e.preventDefault();
      var prodid = $(this).data('index');
      $.ajax({
          type: 'POST',
          url: plus_quantity,
          data: {
              product_id: prodid,
              csrfmiddlewaretoken: window.CSRF_TOKEN,
              action: 'POST'
          },
          success: function (json) {
            document.getElementById(prodid + 'item-qty').value = json.item_qty;
            document.getElementById(prodid + 'item_total').innerHTML = json.item_total_price + ' ₴';
            document.getElementById('cart_icon_count').innerHTML = json.qty;
            document.getElementById('total').innerHTML = json.total;
            document.getElementById('total-with-discount').innerHTML = json.total;
          },
          error: function(xhr, errmsg, err) {}
      });
  });

/*---Subtract quantity in the cart by press minus button---*/
$(document).on('click', '.button-minus', function (e){
      e.preventDefault();
      var prodid = $(this).data('index');
      $.ajax({
          type: 'POST',
          url: minus_quantity,
          data: {
              product_id: prodid,
              csrfmiddlewaretoken: window.CSRF_TOKEN,
              action: 'POST'
          },
          success: function (json) {
            if (json.item_qty < 1) {
              $('.product-item[data-index="'+ prodid +'"]').remove();
              document.getElementById('total').innerHTML = json.total;
              $(".shopping_cart_area").load(location.href + " .shopping_cart_area");
              document.getElementById('cart_icon_count').innerHTML = json.qty;
              if (json.qty === 0) {
                window.location.reload();
            }
            }
            document.getElementById(prodid + 'item-qty').value = json.item_qty;
            document.getElementById(prodid + 'item_total').innerHTML = json.item_total_price +  ' ₴';
            document.getElementById('cart_icon_count').innerHTML = json.qty;
            document.getElementById('total').innerHTML = json.total;
            document.getElementById('total-with-discount').innerHTML = json.total;
          },
          error: function(xhr, errmsg, err) {}
      });
  });

/*---Refresh mini cart by press cart icon---*/
$("#mini-cart").click(function () {
    $("#mini").load(location.href + " #mini");
    $("#mini-cart-total").load(location.href + " #mini-cart-total");
});

/*---Add product to the cart after press action link in the Home page add to cart---*/
$(document).on('click', '.quick-add-button', function (e){
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
            handleAlerts('alert-home', 'success', 'Додано до кошику');
          },
          error: function(xhr, errmsg, err) {
            handleAlerts('alert-home', 'danger', 'ой... щось пішло не так');
          }
      });
});

/*---Open product popup card after press action link quick show product details---*/
$(document).on('click', '.quick-show-button', function (e){
  e.preventDefault();
  var prodid = $(this).data('index');

  $.ajax({
      type: 'POST',
      url: get_single_product,
      data: {
          product_id: prodid,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        document.getElementById('quick-add-button').value = prodid;
        document.getElementById('quick_title').innerHTML = json.title;
        document.getElementById('title_url').href = json.product_url;
        document.getElementById('quick_new_price').innerHTML = json.price;
        document.getElementById('quick_description').innerHTML = json.description;
        document.getElementById('quick_main').src = json.image_main;
        document.getElementById('quick_main_link').src = json.image_main;
        document.getElementById('quick_img1').src = json.img1;
        document.getElementById('quick_img1_link').src = json.img1;
        document.getElementById('quick_img2').src = json.img2;
        document.getElementById('quick_img2_link').src = json.img2;

        document.getElementById('quick_video').href = json.video1;
        document.getElementById('quick_video').target = json.target;

        document.getElementById('quick_main_href').href = json.product_url;
        document.getElementById('quick_img1_href').href = json.product_url;
        document.getElementById('quick_img2_href').href = json.product_url;

        if (json.old_price) {
            document.getElementById('quick_old_price').innerHTML = json.old_price + ' ₴';
        } else {
        document.getElementById('quick_old_price').innerHTML = json.old_price;
        };

      },
      error: function(xhr, errmsg, err) {}
  });
});

/*---Add product to the cart after press quick add button in product quick show popup---*/
$(document).on('click', '#quick-add-button', function (e){
  e.preventDefault();
  var prodid = $('#quick-add-button').val();

  $.ajax({
      type: 'POST',
      url: add_cart,
      data: {
          product_id: prodid,
          quantity: $('#qty-quick-popup').val(),
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        document.getElementById('cart_icon_count').innerHTML = json.qty;
        handleAlerts('alert-pop-up', 'success', 'Додано до кошику');
      },
      error: function(xhr, errmsg, err) {
        handleAlerts('alert-pop-up', 'danger', 'ой... щось пішло не так');
      }
  });
});


/*---Add product to the cart after press TO CART В ПРОПОЗИЦІЇ ТИЖНЯ---*/
$(document).on('click', '.quick-add-button', function (e){
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
            handleAlerts('alert-home', 'success', 'Додано до кошику');
          },
          error: function(xhr, errmsg, err) {
            handleAlerts('alert-home', 'danger', 'ой... щось пішло не так');
          }
      });
});


/*---Set quantity to one after close product quick show popup---*/
$("#close-quick-button").click(function () {
    document.getElementById("qty-quick-popup").value = 1;
});

/*---Calculate basket total and discount after press coupon button---*/
$(document).on('click', '#coupon-button', function (e){
  e.preventDefault();

  $.ajax({
      type: 'POST',
      url: get_coupon,
      data: {
          coupon: $('#coupon-input').val(),
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        document.getElementById('cart-discount').innerHTML = json.cart_discount;
        document.getElementById('total-with-discount').innerHTML = json.total;

        if (json.cart_discount) {
            handleAlerts(
                'alert-prod-details',
                'success',
                `Ви отримали знижку <strong>${json.coupon_discount}%</strong>`
            );
        } else {
            handleAlerts('alert-prod-details', 'success', 'Нажаль цей промокод не дійсний');
        }
      },
      error: function(xhr, errmsg, err) {
        handleAlerts('alert-prod-details', 'danger', 'ой... щось пішло не так');
      }
  });
});


/*---Reload cart page after press refresh button---*/
function refreshCartPage(){
    window.location.reload();
}