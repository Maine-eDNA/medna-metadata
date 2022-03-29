$(function () {
    // hide dependent options onload
    $('#id_envo_biome_second').closest('.row').hide();
    $('#id_envo_biome_third').closest('.row').hide();
    $('#id_envo_biome_fourth').closest('.row').hide();
    $('#id_envo_biome_fifth').closest('.row').hide();
    $('#id_envo_feature_second').closest('.row').hide();
    $('#id_envo_feature_third').closest('.row').hide();
    $('#id_envo_feature_fourth').closest('.row').hide();
    $('#id_envo_feature_fifth').closest('.row').hide();
    $('#id_envo_feature_sixth').closest('.row').hide();
    $('#id_envo_feature_seventh').closest('.row').hide();
});

$("#id_envo_biome_first").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_envo_biome_second');
    var row = dependent_options.closest('.row');
    var data_url = $("#url_envo_biome_second").data("url");
    // console.log(select_val);
    if (select_val) {
        // show row - https://api.jquery.com/hide/
        row.show();
        $.ajax({
            url: data_url,
            data: {
                    'id': select_val
                  },
            success: function (data) {
                // remove any previous options - https://stackoverflow.com/questions/16310588/how-to-clean-completely-select2-control
                dependent_options.empty();
                // append blank option to beginning of results array
                data.results.unshift({id: "", text: "---------"});
                // console.log(data);
                // populate options with ajax data - https://select2.org/data-sources/arrays
                dependent_options.select2({
                    data: data.results
                })
            }
        })
        } else {
            // remove selection since there is no selected value in parent
            dependent_options.val(null);
            // hide row - https://api.jquery.com/hide/
            row.hide();
        }
});

$("#id_envo_biome_second").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_envo_biome_third');
    var row = dependent_options.closest('.row');
    var data_url = $("#url_envo_biome_third").data("url");
    // console.log(select_val);
    if (select_val) {
        // show row - https://api.jquery.com/hide/
        row.show();
        $.ajax({
            url: data_url,
            data: {
                    'id': select_val
                  },
            success: function (data) {
                // remove any previous options - https://stackoverflow.com/questions/16310588/how-to-clean-completely-select2-control
                dependent_options.empty();
                // append blank option to beginning of results array
                data.results.unshift({id: "", text: "---------"});
                // console.log(data);
                // populate options with ajax data - https://select2.org/data-sources/arrays
                dependent_options.select2({
                    data: data.results
                })
            }
        })
        } else {
            // remove selection since there is no selected value in parent
            dependent_options.val(null);
            // hide row - https://api.jquery.com/hide/
            row.hide();
        }
});

$("#id_envo_biome_third").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_envo_biome_fourth');
    var row = dependent_options.closest('.row');
    var data_url = $("#url_envo_biome_fourth").data("url");
    // console.log(select_val);
    if (select_val) {
        // show row - https://api.jquery.com/hide/
        row.show();
        $.ajax({
            url: data_url,
            data: {
                    'id': select_val
                  },
            success: function (data) {
                // remove any previous options - https://stackoverflow.com/questions/16310588/how-to-clean-completely-select2-control
                dependent_options.empty();
                // append blank option to beginning of results array
                data.results.unshift({id: "", text: "---------"});
                // console.log(data);
                // populate options with ajax data - https://select2.org/data-sources/arrays
                dependent_options.select2({
                    data: data.results
                })
            }
        })
        } else {
            // remove selection since there is no selected value in parent
            dependent_options.val(null);
            // hide row - https://api.jquery.com/hide/
            row.hide();
        }
});

$("#id_envo_biome_fourth").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_envo_biome_fifth');
    var row = dependent_options.closest('.row');
    var data_url = $("#url_envo_biome_fifth").data("url");
    // console.log(select_val);
    if (select_val) {
        // show row - https://api.jquery.com/hide/
        row.show();
        $.ajax({
            url: data_url,
            data: {
                    'id': select_val
                  },
            success: function (data) {
                // remove any previous options - https://stackoverflow.com/questions/16310588/how-to-clean-completely-select2-control
                dependent_options.empty();
                // append blank option to beginning of results array
                data.results.unshift({id: "", text: "---------"});
                // console.log(data);
                // populate options with ajax data - https://select2.org/data-sources/arrays
                dependent_options.select2({
                    data: data.results
                })
            }
        })
        } else {
            // remove selection since there is no selected value in parent
            dependent_options.val(null);
            // hide row - https://api.jquery.com/hide/
            row.hide();
        }
});

$("#id_envo_feature_first").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_feature_feature_second');
    var row = dependent_options.closest('.row');
    var data_url = $("#url_envo_feature_second").data("url");
    // console.log(select_val);
    if (select_val) {
        // show row - https://api.jquery.com/hide/
        row.show();
        $.ajax({
            url: data_url,
            data: {
                    'id': select_val
                  },
            success: function (data) {
                // remove any previous options - https://stackoverflow.com/questions/16310588/how-to-clean-completely-select2-control
                dependent_options.empty();
                // append blank option to beginning of results array
                data.results.unshift({id: "", text: "---------"});
                // console.log(data);
                // populate options with ajax data - https://select2.org/data-sources/arrays
                dependent_options.select2({
                    data: data.results
                })
            }
        })
        } else {
            // remove selection since there is no selected value in parent
            dependent_options.val(null);
            // hide row - https://api.jquery.com/hide/
            row.hide();
        }
});

$("#id_envo_feature_second").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_feature_feature_third');
    var row = dependent_options.closest('.row');
    var data_url = $("#url_envo_feature_third").data("url");
    // console.log(select_val);
    if (select_val) {
        // show row - https://api.jquery.com/hide/
        row.show();
        $.ajax({
            url: data_url,
            data: {
                    'id': select_val
                  },
            success: function (data) {
                // remove any previous options - https://stackoverflow.com/questions/16310588/how-to-clean-completely-select2-control
                dependent_options.empty();
                // append blank option to beginning of results array
                data.results.unshift({id: "", text: "---------"});
                // console.log(data);
                // populate options with ajax data - https://select2.org/data-sources/arrays
                dependent_options.select2({
                    data: data.results
                })
            }
        })
        } else {
            // remove selection since there is no selected value in parent
            dependent_options.val(null);
            // hide row - https://api.jquery.com/hide/
            row.hide();
        }
});

$("#id_envo_feature_third").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_feature_feature_fourth');
    var row = dependent_options.closest('.row');
    var data_url = $("#url_envo_feature_fourth").data("url");
    // console.log(select_val);
    if (select_val) {
        // show row - https://api.jquery.com/hide/
        row.show();
        $.ajax({
            url: data_url,
            data: {
                    'id': select_val
                  },
            success: function (data) {
                // remove any previous options - https://stackoverflow.com/questions/16310588/how-to-clean-completely-select2-control
                dependent_options.empty();
                // append blank option to beginning of results array
                data.results.unshift({id: "", text: "---------"});
                // console.log(data);
                // populate options with ajax data - https://select2.org/data-sources/arrays
                dependent_options.select2({
                    data: data.results
                })
            }
        })
        } else {
            // remove selection since there is no selected value in parent
            dependent_options.val(null);
            // hide row - https://api.jquery.com/hide/
            row.hide();
        }
});

$("#id_envo_feature_fourth").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_feature_feature_fifth');
    var row = dependent_options.closest('.row');
    var data_url = $("#url_envo_feature_fifth").data("url");
    // console.log(select_val);
    if (select_val) {
        // show row - https://api.jquery.com/hide/
        row.show();
        $.ajax({
            url: data_url,
            data: {
                    'id': select_val
                  },
            success: function (data) {
                // remove any previous options - https://stackoverflow.com/questions/16310588/how-to-clean-completely-select2-control
                dependent_options.empty();
                // append blank option to beginning of results array
                data.results.unshift({id: "", text: "---------"});
                // console.log(data);
                // populate options with ajax data - https://select2.org/data-sources/arrays
                dependent_options.select2({
                    data: data.results
                })
            }
        })
        } else {
            // remove selection since there is no selected value in parent
            dependent_options.val(null);
            // hide row - https://api.jquery.com/hide/
            row.hide();
        }
});

$("#id_envo_feature_fifth").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_feature_feature_sixth');
    var row = dependent_options.closest('.row');
    var data_url = $("#url_envo_feature_sixth").data("url");
    // console.log(select_val);
    if (select_val) {
        // show row - https://api.jquery.com/hide/
        row.show();
        $.ajax({
            url: data_url,
            data: {
                    'id': select_val
                  },
            success: function (data) {
                // remove any previous options - https://stackoverflow.com/questions/16310588/how-to-clean-completely-select2-control
                dependent_options.empty();
                // append blank option to beginning of results array
                data.results.unshift({id: "", text: "---------"});
                // console.log(data);
                // populate options with ajax data - https://select2.org/data-sources/arrays
                dependent_options.select2({
                    data: data.results
                })
            }
        })
        } else {
            // remove selection since there is no selected value in parent
            dependent_options.val(null);
            // hide row - https://api.jquery.com/hide/
            row.hide();
        }
});

$("#id_envo_feature_sixth").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_feature_feature_seventh');
    var row = dependent_options.closest('.row');
    var data_url = $("#url_envo_feature_seventh").data("url");
    // console.log(select_val);
    if (select_val) {
        // show row - https://api.jquery.com/hide/
        row.show();
        $.ajax({
            url: data_url,
            data: {
                    'id': select_val
                  },
            success: function (data) {
                // remove any previous options - https://stackoverflow.com/questions/16310588/how-to-clean-completely-select2-control
                dependent_options.empty();
                // append blank option to beginning of results array
                data.results.unshift({id: "", text: "---------"});
                // console.log(data);
                // populate options with ajax data - https://select2.org/data-sources/arrays
                dependent_options.select2({
                    data: data.results
                })
            }
        })
        } else {
            // remove selection since there is no selected value in parent
            dependent_options.val(null);
            // hide row - https://api.jquery.com/hide/
            row.hide();
        }
});