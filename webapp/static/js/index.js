const formBx = document.getElementById('formBx');
const body = document.getElementsByTagName('body')[0];

const OTPModal = new bootstrap.Modal(document.getElementById('OTP_modal'));
const successModal = new bootstrap.Modal(document.getElementById('success-modal'));
const firstName = document.getElementById('firstName');
const lastName = document.getElementById('lastName');
const email = document.getElementById('email');
const certificateName = document.getElementById('certificate_name');
const OTP = document.getElementById('OTP');
const OTPCreateButton = document.getElementById('confirmOTP');
const OTPErrorMsg = document.getElementById('OTP-error-msg');
const OTPSuccessMsg = document.getElementById('OTP-success-msg');

const diplomaFile = document.getElementById('certificate');
const DiplomaErrorMsg = document.getElementById('diploma-error-msg');
const verifyModal = new bootstrap.Modal(document.getElementById('verify-modal'));
const verifyFirstName = document.getElementById('verify-first-name');
const verifyLastName = document.getElementById('verify-last-name');
const verifyCertifName = document.getElementById('verify-certificate-name');
const verifyTime = document.getElementById('verify-time');
const verifyTimestampIcon = document.getElementById('timestamp-icon');
const verifySignatureIcon = document.getElementById('signature-icon');
const verifyTimestamp = document.getElementById('verify-timestamp');
const verifySignature = document.getElementById('verify-signature');

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

function hideVerifyModal(){
  verifyModal.hide();
}

function createDiploma() {
  if (OTP.value.trim() === ''  || isNaN(OTP.value.trim())) {
    OTPErrorMsg.classList.add('active');
    OTPErrorMsg.innerText = "The OTP is incorrect (must be a 6 digit code).";
    return;
  }

  OTPCreateButton.setAttribute('disabled', 'true')
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
    OTPCreateButton.removeAttribute('disabled');
  }).catch(function(error) {
    OTPErrorMsg.classList.add('active');
    OTPErrorMsg.innerText = "An error occured. Please try again later.";
    OTPCreateButton.removeAttribute('disabled');
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
    function(response){
      switch (response.status) {
        case 200:
          response.json().then(function(data) {
            verifyFirstName.innerText = data.user.firstName;
            verifyLastName.innerText = data.user.lastName;
            verifyCertifName.innerText = data.user.certificateName;
            verifyTime.innerText = data.tsSignature ?
                new Date(data.user.timestamp).toLocaleString('en-US',{weekday: "long", year: "numeric", month: "long", day: "numeric", hour:'numeric', minute: 'numeric'})
                : "-";
            if (data.tsSignature) {
              verifyTimestampIcon.classList.add("bi-check-circle-fill", "checked");
              verifyTimestampIcon.classList.remove("bi-x-circle-fill", "wrong");
              verifyTimestamp.innerText = "verified";
            } else {
              verifyTimestampIcon.classList.add("bi-x-circle-fill", "wrong");
              verifyTimestampIcon.classList.remove("bi-check-circle-fill", "checked");
              verifyTimestamp.innerText = "not verified";
            }
            if (data.qrSignature) {
              verifySignatureIcon.classList.add("bi-check-circle-fill", "checked");
              verifySignatureIcon.classList.remove("bi-x-circle-fill", "wrong");
              verifySignature.innerText = "verified";
            } else {
              verifySignatureIcon.classList.add("bi-x-circle-fill", "wrong");
              verifySignatureIcon.classList.remove("bi-check-circle-fill", "checked");
              verifySignature.innerText = "not verified";
            }
            verifyModal.show();
          });
          break;
        default:
          DiplomaErrorMsg.classList.add('active');
          DiplomaErrorMsg.innerText = "An error occured.";

      }
    }
  );
}