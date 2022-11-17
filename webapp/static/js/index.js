const formBx = document.getElementById('formBx');
const body = document.getElementsByTagName('body')[0];

const OTPModal = new bootstrap.Modal(document.getElementById('OTP_modal'));
const successModal = new bootstrap.Modal(document.getElementById('success-modal'));
const firstName = document.getElementById('firstName');
const lastName = document.getElementById('lastName');
const email = document.getElementById('email');
const certificateName = document.getElementById('certificate_name');
const OTP = document.getElementById('OTP');
const OTPErrorMsg = document.getElementById('OTP-error-msg');
const OTPSuccessMsg = document.getElementById('OTP-success-msg');

const diplomaFile = document.getElementById('certificate');
const DiplomaErrorMsg = document.getElementById('diploma-error-msg');

function toggleForm() {
  formBx.classList.toggle('active');
  body.classList.toggle('active');
}

function askOTP() {
  let valid = true;
  /* Check if all fields are filled correctly */
  if (firstName.value.trim() === '') {
    firstName.classList.add('error');
    valid = false;
  } else {
    firstName.classList.remove('error');
  }
  if (lastName.value.trim() === '') {
    lastName.classList.add('error');
    valid = false;
  } else {
    lastName.classList.remove('error');
  }
  if (certificateName.value.trim() === '') {
    certificateName.classList.add('error');
    valid = false;
  } else {
    certificateName.classList.remove('error');
  }
  if (! (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email.value.trim()))) {
    email.classList.add('error');
    valid = false;
  } else {
    email.classList.remove('error');
  }
  if (valid) {
    OTPModal.show();
  }
}

function hideModal() {
  OTPModal.hide();
  OTP.value = '';
}

function hideSuccessModal() {
  successModal.hide();
  firstName.value = '';
  lastName.value = '';
  email.value = '';
  certificateName.value = '';
}

function createDiploma() {
  if (OTP.value.trim() === ''  || isNaN(OTP.value.trim())) {
    OTPErrorMsg.classList.add('active');
    OTPErrorMsg.innerText = "The OTP is incorrect (must be a 6 digit code).";
    return;
  }

  /* Send data to backend */
  fetch('/api/create', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      firstName: firstName.value.trim(),
      lastName: lastName.value.trim(),
      email: email.value.trim(),
      certificateName: certificateName.value.trim(),
      OTP: OTP.value.trim()
    })
  }).then(function(response) {
    switch (response.status) {
      case 200:
        response.json().then(function(data) {
          console.log(data);
          OTPSuccessMsg.innerHTML = `Diploma created for ${firstName.value.trim()} ${lastName.value.trim()}.<br/>He/She will receive an email containing the diploma.`;
          OTPModal.hide();
          successModal.show();
          OTPErrorMsg.classList.remove('active');
        });
        break;
      case 403:
        OTPErrorMsg.classList.add('active');
        OTPErrorMsg.innerText = "The password is incorrect.";
        break;
      default:
        OTPErrorMsg.classList.add('active');
        OTPErrorMsg.innerText = "An error occured. Please try again later.";
    }
  }).catch(function(error) {
    OTPErrorMsg.classList.add('active');
    OTPErrorMsg.innerText = "An error occured. Please try again later.";
  });
}

function verify(){
  /* Verify file length and type */
  if (diplomaFile.files.length === 0) {
    DiplomaErrorMsg.classList.add('active');
    DiplomaErrorMsg.innerText = "Please select a file.";
    return;
  } else if (diplomaFile.files[0].type !== 'image/png') {
    DiplomaErrorMsg.classList.add('active');
    DiplomaErrorMsg.innerText = "The file must be a PNG.";
    return;
  }
  DiplomaErrorMsg.classList.add('remove');

  const formData = new FormData();
  formData.append("file", diplomaFile.files[0]);
  const requestOptions = {
    headers: {
        "Content-Type": diplomaFile.files[0].contentType, // This way, the Content-Type value in the header will always match the content type of the file
    },
    mode: "no-cors",
    method: "POST",
    files: diplomaFile.files[0],
    body: formData,
  };

  fetch("/api/verify", requestOptions).then(
    (response) => {
      console.log(response.data);
    }
  );
}