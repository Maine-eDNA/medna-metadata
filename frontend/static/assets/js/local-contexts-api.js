$(function () {
    var $localContextsUrl = "https://localcontextshub.org/api/v1/projects/"
    // grab each project_code from response to render each project's local context project ID
    $('[id^=lcLoading_]').each(function() {
        // dynamically set ID based on returned project_code in template
        var project_code = this.id.split('_').splice(1).join('_');
        var lc_loading_id = 'lcLoading_'+project_code
        var $lcProjectIdSpan = $("#lcProjectId_"+project_code)
        var $projectUniqueId = $lcProjectIdSpan.text();
        var $lcResponse = $("#lcResponse_"+project_code)

        function returnDateFmt (date) {
            var newDate = new Date(date)
            var dateFmt = newDate.toLocaleString()
            return dateFmt
        }
        $.ajax({
            //type
            url: $localContextsUrl + $projectUniqueId,
            //data
            dataType:'json',
            success: function (data) {
            //console.log(data[0].detail);
                document.getElementById(lc_loading_id).remove() // remove loading spinner from page
                $lcProjectIdSpan.remove() // remove id from page
                if (data.created_by) {
                    $.each(data.created_by, function(key, value){ // The contents inside notice
                        $lcResponse.append("<div class='row justify-content-center'><div class='col-auto'><h6 class='font-weight-bolder mt-3' style='text-transform:capitalize;'>Affiliated Institution: "+value.institution.institution_name+" <a href="+data.project_page+">(Project Page)</a></h6></div></div><div class='w-100'></div><hr/>")
                    });
                }
                if (data.notice) {

                    $.each(data.notice, function(key, value){ // The contents inside notice
                        //console.log(value)
                        var $createdDateFmt = returnDateFmt(value.created);
                        var $updatedDateFmt = returnDateFmt(value.updated);
                            $lcResponse.append("<div class='row'><div class='col-md-3 col-12 my-auto'><a target='_blank' href="+value.svg_url+"><img class='w-100 border-radius-lg' src="+value.svg_url+" alt="+value.notice_type+"></a></div><div class='col-md-9 col-12 my-auto'><p class='pe-md-5'>"+value.default_text+"</p><table class='table align-items-center mb-0' style='text-transform:capitalize;'><tbody><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Notice Type"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+value.name+"</span></div></td></tr><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Created"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+$createdDateFmt+"</span></div></td></tr><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Updated"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+$updatedDateFmt+"</span></div></td></tr></tbody></table></div></div><div class='w-100'></div><hr/>")
                    });
                }
                if (data.institution_notice) {
                    $.each(data.institution_notice, function(key, value){  // The contents inside institution_notice
                        var $createdDateFmt = returnDateFmt(value.created);
                        var $updatedDateFmt = returnDateFmt(value.updated);
                        $lcResponse.append("<div class='row'><div class='col-md-3 col-12 my-auto'><a target='_blank' href="+value.svg_url+"><img class='w-100 border-radius-lg' src="+value.svg_url+" alt="+value.notice_type+"></a></div><div class='col-md-9 col-12 my-auto'><p class='pe-md-5'>"+value.default_text+"</p><table class='table align-items-center mb-0' style='text-transform:capitalize;'><tbody><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Notice Type"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+value.notice_type+"</span></div></td></tr><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Created"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+$createdDateFmt+"</span></div></td></tr><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Updated"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+$updatedDateFmt+"</span></div></td></tr></tbody></table></div></div><div class='w-100'></div><hr/>")
                    });
                }
                /*
                if (data.project_boundary_geojson) {
                $.each(data.project_boundary_geojson, function(key, value){  // The contents inside project_boundary_geojson
                    console.log(value)
                });
                }
                */
                if (data.bc_labels) {
                    $.each(data.bc_labels, function(key, value){  // The contents inside bc_labels
                        var $createdDateFmt = returnDateFmt(value.created);
                        var $updatedDateFmt = returnDateFmt(value.updated);
                        $lcResponse.append("<div class='row'><div class='col-md-3 col-12 my-auto'><a target='_blank' href="+value.svg_url+"><img class='w-100 border-radius-lg' src="+value.svg_url+" alt="+value.label_type+"></a></div><div class='col-md-9 col-12 my-auto'><p class='pe-md-5'>"+value.label_text+"</p><table class='table align-items-center mb-0' style='text-transform:capitalize;'><tbody><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Label Type"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+value.label_type+"</span></div></td></tr><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Label Name"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+value.name+"</span></div></td></tr><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Community"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+value.community+"</span></div></td></tr><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Created"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+$createdDateFmt+"</span></div></td></tr><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Updated"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+$updatedDateFmt+"</span></div></td></tr></tbody></table></div></div><div class='w-100'></div><hr/>")
                    });
                }
                if (data.tk_labels) {
                    $.each(data.tk_labels, function(key, value){  // The contents inside tk_labels
                        var $createdDateFmt = returnDateFmt(value.created);
                        var $updatedDateFmt = returnDateFmt(value.updated);
                        $lcResponse.append("<div class='row'><div class='col-md-3 col-12 my-auto'><a target='_blank' href="+value.svg_url+"><img class='w-100 border-radius-lg' src="+value.svg_url+" alt="+value.label_type+"></a></div><div class='col-md-9 col-12 my-auto'><p class='pe-md-5'>"+value.label_text+"</p><table class='table align-items-center mb-0' style='text-transform:capitalize;'><tbody><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Label Type"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+value.label_type+"</span></div></td></tr><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Label Name"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+value.name+"</span></div></td></tr><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Community"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+value.community+"</span></div></td></tr><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Created"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+$createdDateFmt+"</span></div></td></tr><tr><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+"Updated"+"</span></div></td><td class='align-middle text-center'><div class='d-flex align-items-center'><span class='me-2 text-xs'>"+$updatedDateFmt+"</span></div></td></tr></tbody></table></div></div><div class='w-100'></div><hr/>")
                    });
                }
                if ($lcResponse.html() == "") {
                    $lcResponse.html("No notices or labels found for this project.")
                }
            }
        });
   });
});