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
      },
      error: function(xhr, errmsg, err) {}
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
            document.getElementById(prodid + 'item_total').innerHTML = json.item_total_price;
            document.getElementById('cart_icon_count').innerHTML = json.qty;
            document.getElementById('total').innerHTML = json.total;
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
            }
            document.getElementById(prodid + 'item-qty').value = json.item_qty;
            document.getElementById(prodid + 'item_total').innerHTML = json.item_total_price;
            document.getElementById('cart_icon_count').innerHTML = json.qty;
            document.getElementById('total').innerHTML = json.total;
          },
          error: function(xhr, errmsg, err) {}
      });
  });

/*---Refresh mini cart by press cart icon---*/
$("#mini-cart").click(function () {
    $("#mini").load(location.href + " #mini");
    $("#mini-cart-total").load(location.href + " #mini-cart-total");
});

/*---Add product to the cart after press action link add to cart---*/
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
          },
          error: function(xhr, errmsg, err) {}
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
        document.getElementById('quick_new_price').innerHTML = json.price;
        document.getElementById('quick_description').innerHTML = json.description;
        document.getElementById('quick_img').src = json.image;

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
      },
      error: function(xhr, errmsg, err) {}
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
      },
      error: function(xhr, errmsg, err) {}
  });
});