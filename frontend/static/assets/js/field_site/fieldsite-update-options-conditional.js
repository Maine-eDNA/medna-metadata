$(function () {
    // load initial data onload
    var selected_val = $('#id_grant').val();
    if (selected_val) {
        var dependent_options = $('#id_project');
        var data_url = $("#url_project").data("url");
        getDependentOptions(dependent_options, data_url, select_val);
    }
    var selected_val = $('#id_envo_biome_first').val();
    if (selected_val) {
        var dependent_options = $('#id_envo_biome_second');
        var data_url = $("#url_envo_biome_second").data("url");
        getDependentOptions(dependent_options, data_url, select_val);
    }
    var selected_val = $('#id_envo_biome_second').val();
    if (selected_val) {
        var dependent_options = $('#id_envo_biome_third');
        var data_url = $("#url_envo_biome_third").data("url");
        getDependentOptions(dependent_options, data_url, select_val);
    }
    var selected_val = $('#id_envo_biome_third').val();
    if (selected_val) {
        var dependent_options = $('#id_envo_biome_fourth');
        var data_url = $("#url_envo_biome_fourth").data("url");
        getDependentOptions(dependent_options, data_url, select_val);
    }
    var selected_val = $('#id_envo_biome_fourth').val();
    if (selected_val) {
        var dependent_options = $('#id_envo_biome_fifth');
        var data_url = $("#url_envo_biome_fifth").data("url");
        getDependentOptions(dependent_options, data_url, select_val);
    }
    var selected_val = $('#id_envo_feature_first').val();
    if (selected_val) {
        var dependent_options = $('#id_envo_feature_second');
        var data_url = $("#url_envo_feature_second").data("url");
        getDependentOptions(dependent_options, data_url, select_val);
    }
    var selected_val = $('#id_envo_feature_second').val();
    if (selected_val) {
        var dependent_options = $('#id_envo_feature_third');
        var data_url = $("#url_envo_feature_third").data("url");
        getDependentOptions(dependent_options, data_url, select_val);
    }
    var selected_val = $('#id_envo_feature_third').val();
    if (selected_val) {
        var dependent_options = $('#id_envo_feature_fourth');
        var data_url = $("#url_envo_feature_fourth").data("url");
        getDependentOptions(dependent_options, data_url, select_val);
    }
    var selected_val = $('#id_envo_feature_fourth').val();
    if (selected_val) {
        var dependent_options = $('#id_envo_feature_fifth');
        var data_url = $("#url_envo_feature_fifth").data("url");
        getDependentOptions(dependent_options, data_url, select_val);
    }
    var selected_val = $('#id_envo_feature_sixth').val();
    if (selected_val) {
        var dependent_options = $('#id_envo_feature_seventh');
        var data_url = $("#url_envo_feature_seventh").data("url");
        getDependentOptions(dependent_options, data_url, select_val);
});


$("#id_envo_biome_first").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var data_url = $("#url_envo_biome_second").data("url");
    var dependent_options = $('#id_envo_biome_second');
    // console.log(select_val);
    getDependentOptions(dependent_options, data_url, select_val);
});

$("#id_envo_biome_second").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_envo_biome_third');
    var data_url = $("#url_envo_biome_third").data("url");
    // console.log(select_val);
    getDependentOptions(dependent_options, data_url, select_val);
});

$("#id_envo_biome_third").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_envo_biome_fourth');
    var data_url = $("#url_envo_biome_fourth").data("url");
    getDependentOptions(dependent_options, data_url, select_val);
});

$("#id_envo_biome_fourth").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_envo_biome_fifth');
    var data_url = $("#url_envo_biome_fifth").data("url");
    // console.log(select_val);
    getDependentOptions(dependent_options, data_url, select_val);
});

$("#id_envo_feature_first").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_feature_feature_second');
    var data_url = $("#url_envo_feature_second").data("url");
    getDependentOptions(dependent_options, data_url, select_val);
});

$("#id_envo_feature_second").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_feature_feature_third');
    var data_url = $("#url_envo_feature_third").data("url");
    // console.log(select_val);
    getDependentOptions(dependent_options, data_url, select_val);
});

$("#id_envo_feature_third").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_feature_feature_fourth');
    var data_url = $("#url_envo_feature_fourth").data("url");
    // console.log(select_val);
    getDependentOptions(dependent_options, data_url, select_val);
});

$("#id_envo_feature_fourth").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_feature_feature_fifth');
    var data_url = $("#url_envo_feature_fifth").data("url");
    // console.log(select_val);
    getDependentOptions(dependent_options, data_url, select_val);
});

$("#id_envo_feature_fifth").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_feature_feature_sixth');
    var data_url = $("#url_envo_feature_sixth").data("url");
    // console.log(select_val);
    getDependentOptions(dependent_options, data_url, select_val);
});

$("#id_envo_feature_sixth").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_feature_feature_seventh');
    var data_url = $("#url_envo_feature_seventh").data("url");
    // console.log(select_val);
    getDependentOptions(dependent_options, data_url, select_val);
});