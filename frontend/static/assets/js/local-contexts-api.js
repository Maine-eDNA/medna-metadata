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
            var i = data.clo.length; while(i--) {
                $lcProjectIdSpan.append('<p>'+data.clo[i].fin+'</>');
            }
        }
    });

});