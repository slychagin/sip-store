/*---Increment or decrement product quantity in product details---*/
function incrementProdDetail() {
      document.getElementById('qty').stepUp();
   }
function decrementProdDetail() {
  document.getElementById('qty').stepDown();
};


/*---Increment or decrement product quantity in product quick show popup---*/
function incrementQuickPopup() {
      document.getElementById('qty-quick-popup').stepUp();
   }
function decrementQuickPopup() {
  document.getElementById('qty-quick-popup').stepDown();
};


/*---Show or hide delivery method---*/
$(document).on('change', '#delivery-method', function (e){
  e.preventDefault();

  let method = $('#delivery-method option:selected').val()
  let address = document.getElementById('courier');
  let post = document.getElementById('new-post');

  if (method == 'DELIVERY COMPANY') {
    address.style.display = 'none';
    post.removeAttribute("hidden");
    post.style.display = 'block';
  } else if (method == 'COURIER') {
    address.style.display = 'block';
    post.style.display = 'none';
  }

  $.ajax({
      type: 'POST',
      url: order_form,
      data: {
          delivery_method: method,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
      },
      error: function(xhr, errmsg, err) {}
  });
});






/*---Fade message---*/
//setTimeout(function(){
//    $('#messages-list').fadeOut('slow')
//}, 3000)


/*---Fade out message alerts---*/
function fade_alerts() {
    alerts = document.getElementsByClassName("alert msg");
        var i = alerts.length;
        for (let elem of alerts) {
            i--;
            time = 3250+(1000*i);
            setTimeout(function() {
                $(elem).fadeOut("slow");
            }, time);
        }
}

// call fade out after DOMContentLoaded
window.addEventListener('DOMContentLoaded', (event) => {
    fade_alerts();
});