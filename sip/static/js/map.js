/*--- Get data from server to show markers (sale points) ---*/
$(document).ready(function(){
$.ajax({
      url: map_data,
      method: 'GET',
      success: function (data) {
          initMap(data);
      }
  });
});


/*--- Initiates Google Map in the contacts page, and enables to specify parameters ---*/
function initMap(data) {

       const map = new google.maps.Map(document.getElementById('googleMap'), {
          zoom: 10,
          center: {lat: 49.56455965000153, lng: 32.04540037731745},
       });

       var info = new google.maps.InfoWindow({
        content: 'Точка'
       });

       var markers = data?.map((i) => {
            var marker = new google.maps.Marker({
                position: { lat: parseFloat(i.latitude), lng: parseFloat(i.longitude)},
                map: map,
            });

            var info = new google.maps.InfoWindow({
                content:
                `<h4>${i.name}</h4>
                 <p>${i.city}, ${i.street}, ${i.house} ${i.corpus}</p>
                 <p>${i.schedule}</p>
                `
            });
            marker.addListener('click', function() {
                info.open(map, marker);
            })

        });
     }
window.initMap = initMap;