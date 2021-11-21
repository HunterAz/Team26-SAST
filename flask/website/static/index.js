var slideIndex = 1;
showDivs(slideIndex);

function plusDivs(n) {
  showDivs(slideIndex += n);
}

function currentDiv(n) {
  showDivs(slideIndex = n);
}

function showDivs(n) {
  var i;
  var x = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("demo");
  if (n > x.length) {slideIndex = 1}
  if (n < 1) {slideIndex = x.length}
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" w3-white", "");
  }
  x[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " w3-white";
}


//for captcha
function recaptchaCallback() {
  var submit_btn = document.querySelector('#submitBtn');
  submit_btn.removeAttribute('disabled');
  submit_btn.style.cursor = 'pointer';
}

//check password fields match
function validatePassword(pfield1, pfield2) {
	var x = document.getElementById(pfield1);
	var y = document.getElementById(pfield2);
	if (x.value == y.value) {
		y.setCustomValidity("");
	}
	else {
		y.setCustomValidity("Passwords do not match");
	}
}

