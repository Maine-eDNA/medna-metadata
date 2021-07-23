window.onload=function(){
    // view geom field as readonly
    $(".readonly-geom").on('keydown paste', function(e){
        e.preventDefault();
    });
}