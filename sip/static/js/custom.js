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