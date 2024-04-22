function getFilterString() {
    var filters = document.getElementById("filter-fieldset").getElementsByClassName("custom-select");
    filter_url = "";
    for(let i = 0; i < filters.length; ++i) {
      let element = filters[i];
      filter_url += "&";
      filter_url += element.name;
      filter_url += "=";
      filter_url += element.value;
    }
  
    search_name = document.getElementById("search-form").elements[0].name
    search_value = document.getElementById("search-form").elements[0].value;
    filter_url += `&${search_name}=${search_value}`
  
    return filter_url
  }

function handleFilterChange() {
    var filter_form = document.getElementById("filter-form");
    var search_form = document.getElementById("search-form");
    if(filter_form.checkValidity() && search_form.checkValidity()) {
        const baseURL = window.location.origin+window.location.pathname;
        url = "?page=1";
        filters = getFilterString();
        url += filters;
        window.location.href = baseURL+url;
    }

    return false;
}

function getPageUrl(page) {
    const baseURL = window.location.origin+window.location.pathname;
    url = `?page=${page}`;
    filters = getFilterString();
    url += filters;

    window.location.href = baseURL+url;
    return false;
}

document.addEventListener("DOMContentLoaded", function() {

    document.getElementById("exercise_name").value = filter_dict.name;

    var selectElement = document.getElementById("exercise_muscle");
    var options = selectElement.options;
    for (var i = 0; i < options.length; i++) {
        if (options[i].value === filter_dict.muscle) {
            options[i].selected = true;
            break;
        }
    }

    var selectElement = document.getElementById("exercise_level");
    var options = selectElement.options;
    for (var i = 0; i < options.length; i++) {
        if (options[i].value === filter_dict.level) {
            options[i].selected = true;
            break;
        }
    }

    var selectElement = document.getElementById("exercise_equipment");
    var options = selectElement.options;
    for (var i = 0; i < options.length; i++) {
        if (options[i].value === filter_dict.equipment) {
            options[i].selected = true;
            break;
        }
    }

    var selectElement = document.getElementById("exercise_category");
    var options = selectElement.options;
    for (var i = 0; i < options.length; i++) {
        if (options[i].value === filter_dict.category) {
            options[i].selected = true;
            break;
        }
    }

    document.getElementById('filter-form').addEventListener('change', function(event) {
        handleFilterChange()
    }, false);

    document.getElementById("selected_ex_container").style.height = document.getElementById("display_ex_container").offsetHeight + 170;

});