/*---Increment or decrement product quantity in product details---*/
const plusBtn = $('#incrementProdDetail');
const minusBtn = $('#decrementProdDetail');
const addBtn = $('#add-button');
const qty = $('#qty');
const qtyDiv = $("#prod_detail_quantity");
const min = parseInt(qty.attr('min'));
const max = parseInt(qty.attr('max'));

/*---Decrement---*/
$(document).ready(function(){
    minusBtn.click(function(){
        plusBtn.prop("disabled", false);

        if (qty.val() == min) {
            minusBtn.prop("disabled", true);
        } else {
            minusBtn.prop("disabled", true);
            qtyDiv.fadeOut(300);

            setTimeout(()=>{
                qty.val(function(i, oldVal) {return --oldVal});
                minusBtn.prop("disabled", false)
        }, 600)

            qtyDiv.fadeIn(300);
        }
	});
});


/*---Increment---*/
$(document).ready(function(){
    plusBtn.click(function(){
         minusBtn.prop("disabled", false);

        if (qty.val() >= max) {
            plusBtn.prop("disabled", true);
        } else {
            plusBtn.prop("disabled", true);
            qtyDiv.fadeOut(300);

            setTimeout(()=>{
                qty.val(function(i, oldVal) {return ++oldVal});
                plusBtn.prop("disabled", false)
        }, 600)

            qtyDiv.fadeIn(300);
        }
	});
});


/*---Add product to the cart after press Add button in product details page---*/
$(document).on('click', '#add-button', function (e){
  e.preventDefault();
  var prodId = $('#add-button').val();

  addBtn.prop("disabled", true);
  qtyDiv.fadeOut(300);

  setTimeout(()=>{
        addBtn.prop("disabled", false);
  }, 600)

  qtyDiv.fadeIn(300);

  $.ajax({
      type: 'POST',
      url: add_cart,
      data: {
          product_id: prodId,
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



/*---Increment or decrement product quantity in product quick show popup---*/
const plusBtnPopup = $('#incrementQuickPopup');
const minusBtnPopup = $('#decrementQuickPopup');
const addBtnPopup = $('#quick-add-button');
const qtyPopup = $('#qty-quick-popup');
const qtyDivPopup = $("#modal-add-to-cart");
const minPopup = parseInt(qtyPopup.attr('min'));
const maxPopup = parseInt(qtyPopup.attr('max'));

/*---Decrement---*/
$(document).ready(function(){
    minusBtnPopup.click(function(){
        if (qtyPopup.val() == minPopup) {
            minusBtnPopup.prop("disabled", true);
        } else {
            minusBtnPopup.prop("disabled", true);
            qtyDivPopup.fadeOut(300);

            setTimeout(()=>{
                qtyPopup.val(function(i, oldVal) {return --oldVal});
                minusBtnPopup.prop("disabled", false)
        }, 600)

            qtyDivPopup.fadeIn(300);
        }
	});
});


/*---Increment---*/
$(document).ready(function(){
    plusBtnPopup.click(function(){
         minusBtnPopup.prop("disabled", false);

        if (qtyPopup.val() >= max) {
            plusBtnPopup.prop("disabled", true);
        } else {
            plusBtnPopup.prop("disabled", true);
            qtyDivPopup.fadeOut(300);

            setTimeout(()=>{
                qtyPopup.val(function(i, oldVal) {return ++oldVal});
                plusBtnPopup.prop("disabled", false)
        }, 600)

            qtyDivPopup.fadeIn(300);
        }
	});
});


/*---Add product to the cart after press quick add button in product quick show popup---*/
$(document).on('click', '#quick-add-button', function (e){
  e.preventDefault();
  var prodId = $('#quick-add-button').val();

  addBtnPopup.prop("disabled", true);
  qtyDivPopup.fadeOut(300);

  setTimeout(()=>{
        addBtnPopup.prop("disabled", false);
  }, 600)

  qtyDivPopup.fadeIn(300);

  $.ajax({
      type: 'POST',
      url: add_cart,
      data: {
          product_id: prodId,
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
        var update = data['update']

        if (success) {
            form_id.trigger("reset");
            form_id.replaceWith(data['html']);
            $("#comment-form-title").hide();
            handleCommentAlerts('alert-prod-details', 'success',
            "Дякуємо за Ваш коментар!<br/>Він з'явиться одразу після модерації." );
        } else if (update) {
            form_id.trigger("reset");
            form_id.replaceWith(data['html']);
            $("#comment-form-title").hide();
            handleCommentAlerts('alert-prod-details', 'success',
            "Ваш коментар було оновлено!<br/>Він з'явиться одразу після модерації." );
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
        var info = data['info']
        var update = data['update']

        if (success) {
            form_id.trigger("reset");
            form_id.replaceWith(data['html']);
            $("#review_form_title").hide();
            $("#rating-stars").hide();
            handleReviewAlerts('alert-rating-success', 'success',
            "Дякуємо за Ваш відгук!<br/>Він з'явиться одразу після модерації." );
        } else if (info) {
            form_id.trigger("reset");
            form_id.replaceWith(data['html']);
            $("#review_form_title").hide();
            $("#rating-stars").hide();
            fixAlerts('alert-prod-info', 'danger', 'Щоб залишити відгук,<br/>вам потрібно купити даний продукт.');
        } else if (update) {
            form_id.trigger("reset");
            form_id.replaceWith(data['html']);
            $("#review_form_title").hide();
            $("#rating-stars").hide();
            handleReviewAlerts('alert-rating-success', 'success',
            "Ваш відгук було оновлено!<br/>Він з'явиться одразу після модерації." );
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

/*--- Show more comments ---*/
$(document).ready(function() {
    let visible = 0
    $('#show-more-comments').on('click', function (){

    const commentBox = document.getElementById('comment-box')
    const spinnerBox = document.getElementById('spinner-comments-box')
    const loadBtn = document.getElementById('show-more-comments')
    const loadBox = document.getElementById('loading-comments-box')

    let postId = $('#show-more-comments').val();

    visible += 10

        $.ajax({
        url: load_more_comments,
        type: 'POST',
        data: {
              post_id: postId,
              visible_comments: visible,
              csrfmiddlewaretoken: window.CSRF_TOKEN,
              action: 'POST'
        },
        dataType: 'json',

        success: function(response){
            maxSize = response.max
            const data = response.data
            spinnerBox.classList.remove('not-visible')
            setTimeout(()=>{
                spinnerBox.classList.add('not-visible')
                data.map(comment=>{
                    commentBox.innerHTML += `
                    <div class="comment_list">
                        <div class="comment_content">
                            <div class="comment_meta">
                                <h5>${comment.name}</h5>
                                <span>${comment.modified_date}</span>
                            </div>
                            <p>${comment.content}</p>
                        </div>
                    </div>`
                })
                if(maxSize){
                    loadBox.innerHTML = '<br><h4>Більше немає коментарів</h4>'
                }
            }, 500)
          },
            error: function(error){
                handleAlerts('alert-home', 'danger', 'ой... щось пішло не так');
            }
        });
    });
});


/*--- Show more reviews ---*/
$(document).ready(function() {
    let visible = 0
    $('#show-more-reviews').on('click', function (){

    const reviewsBox = document.getElementById('reviews-box')
    const spinnerBox = document.getElementById('spinner-reviews-box')
    const loadBtn = document.getElementById('show-more-reviews')
    const loadBox = document.getElementById('loading-reviews-box')

    let productId = $('#show-more-reviews').val();

    visible += 10

        $.ajax({
        url: load_more_reviews,
        type: 'POST',
        data: {
              product_id: productId,
              visible_reviews: visible,
              csrfmiddlewaretoken: window.CSRF_TOKEN,
              action: 'POST'
        },
        dataType: 'json',

        success: function(response){
            maxSize = response.max
            const data = response.data
            spinnerBox.classList.remove('not-visible')
            setTimeout(()=>{
                spinnerBox.classList.add('not-visible')
                data.map(review=>{
                    let stars = ``
                    let hole_star = `<label aria-label="1 star" class="rating__label small_star">
                                    <i class="rating__icon rating__icon--star fa fa-star"></i></label>`
                    let half_star = `<label aria-label="0.5 stars" class="rating__label small_star small_star--half">
                                    <i class="rating__icon rating__icon--star fa fa-star-half"></i></label>`

                    if(Math.trunc(review.rating) == review.rating) {
                        stars = hole_star.repeat(review.rating);
                    } else {
                        stars = hole_star.repeat(Math.trunc(review.rating)) + half_star;
                    }

                    reviewsBox.innerHTML += `
                    <div class="reviews_comment_box">
                        <div class="comment_text">
                            <div class="reviews_meta">
                                <div class="star_rating">
                                    <div class="rating-group">`

                                    + stars +

                                 `</div>
                                </div>
                                <p><strong>${review.name}</strong> - ${review.modified_date}</p>
                                <span>${review.review}</span>
                            </div>
                        </div>
                    </div>`
                })
                if(maxSize){
                    loadBox.innerHTML = '<br><h4>Більше немає відгуків</h4>'
                }
            }, 500)
          },
            error: function(error){
                handleAlerts('alert-home', 'danger', 'ой... щось пішло не так');
            }
        });
    });
});


/*--- Link to review tab by pressing rating stars in product details ---*/
$('.link-to-reviews').click(function(){
    $('html, body').animate({ scrollTop:$("#reviews-tab").offset().top}, 500);
    document.getElementById("reviews-tab").click();
});


/*--- Show temporary flash message with 3 seconds timeout ---*/
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


/*--- Show temporary flash message with 9 seconds timeout for post comments ---*/
function handleCommentAlerts(alertId, type, text) {
  const alertBox = document.getElementById(alertId);
  alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">
                              ${text}
                            </div>`
  setTimeout(()=>{
      alertBox.innerHTML = ''
  }, 9000)
};


/*--- Show temporary flash message with 9 seconds timeout for product reviews ---*/
function handleReviewAlerts(alertId, type, text) {
  const alertBox = document.getElementById(alertId);
  alertBox.innerHTML = `<div class="alert alert-${type}" role="alert">
                              ${text}
                            </div>`
  setTimeout(()=>{
      alertBox.innerHTML = ''
  }, 9000)
};
