function resetAllDropdowns() {
    var dropdowns = document.querySelectorAll('#actionDropdown');

    dropdowns.forEach(function (dropdown) {
      dropdown.value = '';
    });
}

document.addEventListener("DOMContentLoaded", function () {
  var dropdowns = document.querySelectorAll('#actionDropdown');

  dropdowns.forEach(function (dropdown) {
    dropdown.value = ' ';
  });
})