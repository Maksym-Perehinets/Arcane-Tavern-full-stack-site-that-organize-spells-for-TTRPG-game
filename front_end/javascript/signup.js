function showPassword() {
    let x = document.getElementById("pass");
    let svg = document.getElementById("showPasswordButton")
  if (x.type === "password") {
    x.type = "text";
    svg.style.transition = "all .7s"
    svg.src = "https://www.svgrepo.com/show/522528/eye.svg";
  } else {
    x.type = "password";
    svg.src = "https://www.svgrepo.com/show/522530/eye-off.svg";
  }
}


document.addEventListener("DOMContentLoaded", function() {
  var tooltip = document.getElementById("tooltip");

  document.addEventListener("mousemove", function(event) {
    tooltip.style.left = (event.pageX + 5) + "px";
    tooltip.style.top = (event.pageY + -200) + "px";
  });

  document.addEventListener("mouseover", function(event) {
    if (event.target.dataset.tooltip) {
      tooltip.style.display = "block";
    }
  });

  document.addEventListener("mouseout", function(event) {
    if (event.target.dataset.tooltip) {
      tooltip.style.display = "none";
    }
  });
});