$("#id_envo_biome_first").on("select2:select", function (e) {
    var select_val = $(e.currentTarget).val();
    console.log(select_val);

    $('#id_envo_biome_second').select2({
      ajax: {
        url: window.location.origin+"/dashboard/biome/second/",
        data: {
          'envo_biome_first': select_val       // add the country id to the GET parameters
        },
        processResults: function (data) {  // `data` is the return of the `load_cities` view function
          return {
           results: data  // replace the contents of the city input with the data that came from the server
          }
        }
      }
    })
});


$("#id_envo_biome_second").change(function () {
  var url = window.location.origin+"/dashboard/biome/third/";
  var pk = $(this).val();  // get the selected country ID from the HTML input

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    data: {
      'envo_biome_second': pk       // add the country id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#id_envo_biome_third").html(data);  // replace the contents of the city input with the data that came from the server
    }
  })
});

$("#id_envo_biome_third").change(function () {
  var url = window.location.origin+"/dashboard/biome/fourth/";
  var pk = $(this).val();  // get the selected country ID from the HTML input

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    data: {
      'envo_biome_third': pk       // add the country id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#id_envo_biome_fourth").html(data);  // replace the contents of the city input with the data that came from the server
    }
  })
});

$("#id_envo_biome_fourth").change(function () {
  var url = window.location.origin+"/dashboard/biome/fifth/";
  var pk = $(this).val();  // get the selected country ID from the HTML input

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    data: {
      'envo_biome_fourth': pk       // add the country id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#id_envo_biome_fifth").html(data);  // replace the contents of the city input with the data that came from the server
    }
  })
});

$("#id_envo_feature_first").change(function () {
  var url = window.location.origin+"/dashboard/feature/second/";
  var pk = $(this).val();  // get the selected country ID from the HTML input

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    data: {
      'envo_feature_first': pk       // add the country id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#id_envo_feature_second").html(data);  // replace the contents of the city input with the data that came from the server
    }
  })
});

$("#id_envo_feature_second").change(function () {
  var url = window.location.origin+"/dashboard/feature/third/";
  var pk = $(this).val();  // get the selected country ID from the HTML input

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    data: {
      'envo_feature_second': pk       // add the country id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#id_envo_feature_third").html(data);  // replace the contents of the city input with the data that came from the server
    }
  })
});

$("#id_envo_feature_third").change(function () {
  var url = window.location.origin+"/dashboard/feature/fourth/";
  var pk = $(this).val();  // get the selected country ID from the HTML input

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    data: {
      'envo_feature_third': pk       // add the country id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#id_envo_feature_fourth").html(data);  // replace the contents of the city input with the data that came from the server
    }
  })
});

$("#id_envo_feature_fourth").change(function () {
  var url = window.location.origin+"/dashboard/feature/fifth/";
  var pk = $(this).val();  // get the selected country ID from the HTML input

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    data: {
      'envo_feature_fourth': pk       // add the country id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#id_envo_feature_fifth").html(data);  // replace the contents of the city input with the data that came from the server
    }
  })
});

$("#id_envo_feature_fifth").change(function () {
  var url = window.location.origin+"/dashboard/feature/sixth/";
  var pk = $(this).val();  // get the selected country ID from the HTML input

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    data: {
      'envo_feature_fifth': pk       // add the country id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#id_envo_feature_sixth").html(data);  // replace the contents of the city input with the data that came from the server
    }
  })
});

$("#id_envo_feature_sixth").change(function () {
  var url = window.location.origin+"/dashboard/feature/seventh/";
  var pk = $(this).val();  // get the selected country ID from the HTML input

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
    data: {
      'envo_feature_sixth': pk       // add the country id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#id_envo_feature_seventh").html(data);  // replace the contents of the city input with the data that came from the server
    }
  })
});