$(function () {
    var $localContextsUrl = "https://localcontextshub.org/api/v1/projects/"
    var $lcProjectIdSpan = $("#lcProjectId")
    var $projectUniqueId = $lcProjectIdSpan.text();
    $.ajax({
        //type
        url: $localContextsUrl + $projectUniqueId,
        //data
        dataType:'json',
        success: function (data) {
            $.each(data.data , function(key , value){ // First Level
                 $.each(value.stars , function(k , v ){  // The contents inside stars
                     console.log(v)
                 });
            });
        }
    });

});