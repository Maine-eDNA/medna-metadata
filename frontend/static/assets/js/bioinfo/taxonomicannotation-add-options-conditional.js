$(function () {
    // hide dependent options onload
    $('#id_manual_kingdom').closest('.row').hide();
    $('#id_manual_supergroup').closest('.row').hide();
    $('#id_manual_phylum_division').closest('.row').hide();
    $('#id_manual_class').closest('.row').hide();
    $('#id_manual_order').closest('.row').hide();
    $('#id_manual_family').closest('.row').hide();
    $('#id_manual_genus').closest('.row').hide();
    $('#id_manual_species').closest('.row').hide();
});

$("#id_manual_domain").on("select2:select", function (e) {
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_manual_kingdom');
    var data_url = $("#url_manual_kingdom").data("url");
    // console.log(select_val);
    getDependentOptionsHide(dependent_options, data_url, select_val);
});

$("#id_manual_kingdom").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_manual_supergroup');
    var data_url = $("#url_manual_supergroup").data("url");
    // console.log(select_val);
    getDependentOptionsHide(dependent_options, data_url, select_val);
});

$("#id_manual_supergroup").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_manual_phylum_division');
    var data_url = $("#url_manual_phylum_division").data("url");
    // console.log(select_val);
    getDependentOptionsHide(dependent_options, data_url, select_val);
});

$("#id_manual_phylum_division").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_manual_class');
    var data_url = $("#url_manual_class").data("url");
    getDependentOptionsHide(dependent_options, data_url, select_val);
});

$("#id_manual_class").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_manual_order');
    var data_url = $("#url_manual_order").data("url");
    // console.log(select_val);
    getDependentOptionsHide(dependent_options, data_url, select_val);
});

$("#id_manual_order").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_manual_family');
    var data_url = $("#url_manual_family").data("url");
    getDependentOptionsHide(dependent_options, data_url, select_val);
});

$("#id_manual_family").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_manual_genus');
    var data_url = $("#url_manual_genus").data("url");
    // console.log(select_val);
    getDependentOptionsHide(dependent_options, data_url, select_val);
});

$("#id_manual_genus").on("select2:select", function (e) {
    // https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    // https://stackoverflow.com/questions/19908273/jquery-select2-get-value-of-select-tag
    var select_val = $(e.currentTarget).val();
    var dependent_options = $('#id_manual_species');
    var data_url = $("#url_manual_species").data("url");
    // console.log(select_val);
    getDependentOptionsHide(dependent_options, data_url, select_val);
});