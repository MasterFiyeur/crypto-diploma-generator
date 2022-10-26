const formBx = document.getElementById('formBx');
const body = document.getElementsByTagName('body')[0];

function toggleForm() {
  formBx.classList.toggle('active');
  body.classList.toggle('active');
}

function askOTP() {
	console.log("Check your email for OTP");
}

function verify(){
	console.log("diplomat verified");
}