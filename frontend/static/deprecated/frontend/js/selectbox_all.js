function toggle(source) {
    checkboxes = document.getElementsByName('selection');
    for(var i in checkboxes)
        checkboxes[i].checked = source.checked;
}