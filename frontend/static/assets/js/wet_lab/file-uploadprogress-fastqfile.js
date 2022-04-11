$(function () {
  // https://anshu-dev.medium.com/file-upload-progress-bar-using-django-and-ajax-ba4eb7482d9c
    const uploadForm = document.getElementById('upload_form');
    const input_file = document.getElementById('id_fastq_datafile');
    const progress_bar = document.getElementById('progress');
    const add_url = $("#url_add_fastqfile").data("url");

    $("#upload_form").submit(function(e){
        e.preventDefault();
        $form = $(this)
        var formData = new FormData(this);
        const media_data = input_file.files[0];
        if(media_data != null){
            console.log(media_data);
            progress_bar.classList.remove("not-visible");
        }

        $.ajax({
            type: 'POST',
            url: add_url,
            data: formData,
            dataType: 'json',
            beforeSend: function(){

            },
            xhr:function(){
                const xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', e=>{
                    if(e.lengthComputable){
                        const percentProgress = (e.loaded/e.total)*100;
                        const roundPercentProgress = Math.round(percentProgress)
                        // console.log(percentProgress);
                        progress_bar.innerHTML = `<div class="col-12 d-flex align-items-center">
                        <i class="fa fa-file-o text-3xl mx-2 mb-2" aria-hidden="true"></i>
                        <span class="text-sm font-weight-normal">${roundPercentProgress}%</span></div>
                        <div class="col-12 progress-bar progress-bar-striped bg-success"
                        role="progressbar" style="width: ${percentProgress}%" aria-valuenow="${percentProgress}" aria-valuemin="0"
                        aria-valuemax="100"></div>`
                    }
                });
                return xhr
            },
            success: function(response){
                console.log(response);
                uploadForm.reset();
                progress_bar.classList.add('not-visible');
            },
            error: function(err){
                console.log(err);
            },
            cache: false,
            contentType: false,
            processData: false,
        });
    });

});