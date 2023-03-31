/*---Delete product from the basket---*/
$(document).on('click', '.delete-button', function (e){
  e.preventDefault();
  var prodId = $(this).data('index');
  var spinnerBox = $(`#${prodId}spinner-cart-box`);

  spinnerBox.removeClass('not-visible');
  
  $.ajax({
      type: 'POST',
      url: cart_delete,
      data: {
          product_id: prodId,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        setTimeout(()=>{
            $('.product-item[data-index="'+ prodId +'"]').remove();
         }, 500);
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
    var prodId = $(this).data('index');
    $.ajax({
        type: 'POST',
        url: mini_cart_delete,
        data: {
            product_id: prodId,
            csrfmiddlewaretoken: window.CSRF_TOKEN,
            action: 'POST'
        },
        success: function (json) {
          $('.cart_item[data-index="'+ prodId +'"]').remove();
          document.getElementById('mini-cart-total').innerHTML = json.mini_cart_total;
          document.getElementById('cart_icon_count').innerHTML = json.qty;
        },
        error: function(xhr, errmsg, err) {}
    });
});


/*---Add quantity by press plus button in the cart page---*/
$(document).on('click', '.button-plus', function (e){
      e.preventDefault();
      var prodId = $(this).data('index');
      var qtyCartDiv = $(`#${prodId}quantity-cart`);
      var inputQty = $(`#${prodId}item-qty`).val();
      var maxQty = $(`#${prodId}item-qty`).attr('max') - 1;

      $(this).prop('disabled', true);
      qtyCartDiv.fadeOut(300);

      $.ajax({
          type: 'POST',
          url: plus_quantity,
          data: {
              product_id: prodId,
              csrfmiddlewaretoken: window.CSRF_TOKEN,
              action: 'POST'
          },
          success: function (json) {
            document.getElementById(prodId + 'item-qty').value = json.item_qty;
            document.getElementById(prodId + 'item_total').innerHTML = json.item_total_price + ' ₴';
            document.getElementById('cart_icon_count').innerHTML = json.qty;
            document.getElementById('total').innerHTML = json.total;
            document.getElementById('total-with-discount').innerHTML = json.total;
          },
          error: function(xhr, errmsg, err) {}
      });

      setTimeout(()=>{
        if (inputQty >= maxQty){
            $(this).prop('disabled', true);
        } else {
            $(this).prop('disabled', false);
        }
      }, 600);
      qtyCartDiv.fadeIn(300);
  });

/*---Subtract quantity in the cart by press minus button---*/
$(document).on('click', '.button-minus', function (e){
      e.preventDefault();
      var prodId = $(this).data('index');
      var qtyCartDiv = $(`#${prodId}quantity-cart`);

      $(this).prop('disabled', true);
      qtyCartDiv.fadeOut(300);

      $.ajax({
          type: 'POST',
          url: minus_quantity,
          data: {
              product_id: prodId,
              csrfmiddlewaretoken: window.CSRF_TOKEN,
              action: 'POST'
          },
          success: function (json) {
            if (json.item_qty < 1) {
              $('.product-item[data-index="'+ prodId +'"]').remove();
              document.getElementById('total').innerHTML = json.total;
              $(".shopping_cart_area").load(location.href + " .shopping_cart_area");
              document.getElementById('cart_icon_count').innerHTML = json.qty;
                  if (json.qty === 0) {
                    window.location.reload();
                }
            } else {
            document.getElementById(prodId + 'item-qty').value = json.item_qty;
            document.getElementById(prodId + 'item_total').innerHTML = json.item_total_price +  ' ₴';
            document.getElementById('cart_icon_count').innerHTML = json.qty;
            document.getElementById('total').innerHTML = json.total;
            document.getElementById('total-with-discount').innerHTML = json.total;
            }
          },
          error: function(xhr, errmsg, err) {}
      });

      setTimeout(()=>{
        $(this).prop('disabled', false);
      }, 600);
      qtyCartDiv.fadeIn(300);
  });

/*---Refresh mini cart by press cart icon---*/
$("#mini-cart").click(function () {
    $("#mini").load(location.href + " #mini");
    $("#mini-cart-total").load(location.href + " #mini-cart-total");
});

/*---Add product to the cart after press ACTION LINK BASKET add to cart---*/
$(document).on('click', '.quick-add-button', function (e){
      e.preventDefault();
      var prodId = $(this).data('index');
//      var basketLi = $('.add_to_cart[data-index="'+ prodId +'"]');
      var quickBasketBtn = $('.quick-add-button[data-index="'+ prodId +'"]');
      var spinner = $('.spinner-cart-box[data-index="'+ prodId +'"]');

      quickBasketBtn.prop("disabled", true);
      spinner.removeClass('not-visible');
      setTimeout(()=>{
          spinner.addClass('not-visible');
          quickBasketBtn.prop("disabled", false);
      }, 600)

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
  var prodId = $(this).data('index');

  $.ajax({
      type: 'POST',
      url: get_single_product,
      data: {
          product_id: prodId,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        document.getElementById('quick-add-button').value = prodId;
        document.getElementById('quick_title').innerHTML = json.title;
        document.getElementById('title_url').href = json.product_url;
        document.getElementById('quick_new_price').innerHTML = json.price;
        document.getElementById('unit_price').innerHTML = json.price + ' ' + json.unit;
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


/*---Add product to the cart after press TO CART В ПРОПОЗИЦІЇ ТИЖНЯ---*/
$(document).on('click', '.quick-add-button-offer-banner', function (e){
      e.preventDefault();
      var prodId = $(this).data('index');
      var bannerAddDiv = $('.addto_cart_btn[data-index="'+ prodId +'"]');
      var weekOfferAddBtn = $('#week-offer-button[data-index="'+ prodId +'"]')

      weekOfferAddBtn.prop("disabled", true);
      bannerAddDiv.fadeOut(300);
      setTimeout(()=>{
          weekOfferAddBtn.prop("disabled", false);
      }, 600)
      bannerAddDiv.fadeIn(300);

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