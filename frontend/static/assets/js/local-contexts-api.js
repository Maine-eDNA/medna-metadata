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
            $.each(data.notice, function(key, value){ // First Level
                console.log(value)
            });
            $.each(data.notice, function(key, value){  // The contents inside stars
                console.log(value)
            });
            $.each(data.institution_notice, function(key, value){  // The contents inside stars
                console.log(value)
            });
            $.each(data.project_boundary_geojson, function(key, value){  // The contents inside stars
                console.log(value)
            });
        }
    });

});