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


/*--- Handle Review Rating form ---*/
$(document).on('click', '#ajax_review', function (e){
  e.preventDefault();
  var rating = document.querySelector('input[name="rating"]:checked').value;
  document.getElementById('rating').value = rating;
  var form_id = $('#review-rating-form');


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
            $("#review_form_title").hide();
            $("#rating-stars").hide();
            handleAlerts('alert-rating-success', 'success',
            "Дякуємо за Ваш відгук!<br/>Він з'явиться одразу після модерації." );
        } else {
            form_id.replaceWith(data['html']);
            if (rating == 0) {
                fixAlerts('alert-prod-rating', 'danger', 'Будь ласка, встановіть рейтинг');
            } else {
                document.getElementById('alert-prod-rating').innerHTML = ''
            }
        }
      },
      error: function(xhr, errmsg, err) {
        handleAlerts('alert-prod-details', 'danger', 'ой... щось пішло не так');
      }
  });
});


/*---Show/hide post comments---*/
function showHideComments() {
  var commentBlock = document.getElementById("comment-box-full");
  var showBtn = document.getElementById("show-button")

  if (commentBlock.style.display === "none") {
    commentBlock.style.display = "block";
    showBtn.innerHTML = "Менше коментарів";
  } else {
    commentBlock.style.display = "none";
    showBtn.innerHTML = "Більше коментарів";
  }
}


/*--- Show temporary flash message ---*/
function handleAlerts(alertId, type, text) {
  const alertBox = document.getElementById(alertId);
  alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">
                              ${text}
                            </div>`
  setTimeout(()=>{
      alertBox.innerHTML = ''
  }, 3000)
};

/*--- Show standing flash message ---*/
function fixAlerts(alertId, type, text) {
  const alertBox = document.getElementById(alertId);
  alertBox.innerHTML = `<div class="alert alert-${type} alert-rating" role="alert">
                              ${text}
                            </div>`
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