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
            $.each(data.data, function(key, value){ // First Level
                console.log(value)
                $.each(value.notice, function(k, v){  // The contents inside stars
                 console.log(v)
                });
                $.each(value.institution_notice, function(k, v){  // The contents inside stars
                 console.log(v)
                });
                $.each(value.project_boundary_geojson, function(k, v){  // The contents inside stars
                 console.log(v)
                });
            });
        }
    });

});