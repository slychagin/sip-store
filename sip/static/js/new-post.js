//var settings = {
//    apiKey: "54e3bb8b4eb27d205ce6d489712a5524",
//    modelName: "Address",
//    calledMethod: "getCities",
//    methodProperties: { FindByString: "Львів" }
//};
//
//$.ajax({
//    url: "https://api.novaposhta.ua/v2.0/json/",
//    method: "POST",
//    processData: false,
//    crossDomain: true,
//    async: true,
//    contentType: "application/json",
//    data: JSON.stringify(settings)
//}).done(function (response) {
//    console.log(response);
//});

var settings = {
    apiKey: "54e3bb8b4eb27d205ce6d489712a5524",
    modelName: "Address",
    calledMethod: "getCities",
    methodProperties: { FindByString: "Львів" }
};

$.ajax({
    url: "https://api.novaposhta.ua/v2.0/json/",
    method: "POST",
    processData: false,
    crossDomain: true,
    async: true,
    contentType: "application/json",
    data: JSON.stringify(settings)
}).done(function (response) {
    console.log(response);
});