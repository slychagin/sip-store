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


/*---Subscribe user---*/
$(document).on('click', '#mc-submit', function (e){
  e.preventDefault();
  var user_email = $('#mc-email').val();

  $.ajax({
      type: 'POST',
      url: subscribe,
      data: {
          email: user_email,
          csrfmiddlewaretoken: window.CSRF_TOKEN,
          action: 'POST'
      },
      success: function (json) {
        if (json.success) {
            handleAlerts('alert-prod-details', 'success', json.success);
            document.getElementById("mc-email").value = '';
        } else {
            handleAlerts('alert-prod-details', 'danger', json.error);
        }

      },
      error: function(xhr, errmsg, err) {
        handleAlerts('alert-prod-details', 'danger', 'ой... щось пішло не так');
      }
  });
});


/*--- Handle Comments form ---*/
$(document).on('click', '#ajax_comment', function (e){
  e.preventDefault();
  var form_id = $('#post-comment-form');

  $.ajax({
      type: 'POST',
      data: form_id.serialize(),
      dataType: 'json',
      header: window.CSRF_TOKEN,

      success: function (data) {
        var success = data['success']
        if (success) {
            form_id.trigger("reset");
            form_id.replaceWith(data['html']);
            $("#comment-form-title").hide();
            handleAlerts('alert-prod-details', 'success',
            "Дякуємо за Ваш коментар!<br/>Він з'явиться одразу після модерації." );
        } else {
            form_id.replaceWith(data['html']);
        }
      },
      error: function(xhr, errmsg, err) {
        handleAlerts('alert-prod-details', 'danger', 'ой... щось пішло не так');
      }
  });
});


/*--- Show flash message ---*/
function handleAlerts(alertId, type, text) {
  const alertBox = document.getElementById(alertId);
  alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">
                              ${text}
                            </div>`
  setTimeout(()=>{
      alertBox.innerHTML = ''
  }, 3000)
};




/*---Fade message---*/
//setTimeout(function(){
//    $('#messages-list').fadeOut('slow')
//}, 3000)


/*---Fade out message alerts---*/
//function fade_alerts() {
//    alerts = document.getElementsByClassName("alert msg");
//        var i = alerts.length;
//        for (let elem of alerts) {
//            i--;
//            time = 3250+(1000*i);
//            setTimeout(function() {
//                $(elem).fadeOut("slow");
//            }, time);
//        }
//}
//
//// call fade out after DOMContentLoaded
//window.addEventListener('DOMContentLoaded', (event) => {
//    fade_alerts();
//});