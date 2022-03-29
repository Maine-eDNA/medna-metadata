var getDependentOptionsHide = function(dependent_options, data_url, select_val) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    var row = dependent_options.closest('.row');
    var empty_results = [{id: "", text: "---------"}]
    if (select_val) {
        // clear previously selected values on change
        dependent_options.val(null);
        // show row - https://api.jquery.com/hide/
        row.show();
        $.ajax({
            url: data_url,
            data: {
                    'id': select_val
                  },
            success: function (data) {
                // remove any previous options - https://stackoverflow.com/questions/16310588/how-to-clean-completely-select2-control
                if (data) {
                    dependent_options.empty();
                    // append blank option to beginning of results array
                    data.results.unshift({id: "", text: "---------"});
                    // console.log(data);
                    // populate options with ajax data - https://select2.org/data-sources/arrays
                    dependent_options.select2({
                        data: data.results
                    })
                } else {
                    console.log(empty_results);
                    dependent_options.empty();
                    dependent_options.select2({
                        data: empty_results
                    })
                }
            }
        })
        } else {
            // remove selection since there is no selected value in parent
            dependent_options.val(null);
            dependent_options.empty();
            // hide row - https://api.jquery.com/hide/
            row.hide();
        }
};

var getDependentOptions = function(dependent_options, data_url, select_val) {
    var row = dependent_options.closest('.row');
    var empty_results = [{id: "", text: "---------"}]
    if (select_val) {
        // clear previously selected values on change
        dependent_options.val(null);
        $.ajax({
            url: data_url,
            data: {
                    'id': select_val
                  },
            success: function (data) {
            if (data) {
                // remove any previous options - https://stackoverflow.com/questions/16310588/how-to-clean-completely-select2-control
                dependent_options.empty();
                // append blank option to beginning of results array
                data.results.unshift({id: "", text: "---------"});
                // console.log(data);
                // populate options with ajax data - https://select2.org/data-sources/arrays
                dependent_options.select2({
                    data: data.results
                })
            } else {
                console.log(empty_results);
                dependent_options.empty();
                dependent_options.select2({
                    data: empty_results
                })
            }
            }
        })
        } else {
            // remove selection since there is no selected value in parent
            dependent_options.val(null);
            dependent_options.empty();
        }
};