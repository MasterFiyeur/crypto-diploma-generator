const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const timer = document.getElementById('timer');

let code = "";
let secret_key = "";

/* Make the animation around the code */
function degToRad(degree) {
	let factor = Math.PI / 180;
	return degree * factor;
}

function renderTime() {
	let now = new Date();
	let seconds = now.getSeconds();
	let milliseconds = now.getMilliseconds();

	let newSeconds = seconds+(milliseconds/1000);
	timer.innerHTML = (30 - (seconds % 30)) + 's';

	ctx.fillStyle = '#F3DEA0';
	ctx.fillRect(0,0,300,300);

	//seconds
	ctx.beginPath();
	ctx.arc(150, 150, 130, degToRad(270), degToRad((newSeconds+2)*12)-90);
	ctx.stroke();
}

function updateCodeIfIsTime() {
	let seconds = new Date().getSeconds();
	if (seconds % 30 == 0) {
		updateCode();
	}
}

/* Update the OTP */
function updateCode() {
	code = getOTP(secret_key);
	document.getElementById('code').innerHTML = code;
	/* Calculate code for next update */
	console.log("Code updated " + new Date().toLocaleTimeString());
}

/* Get key, setup canvas and set interval functions*/
function init() {
	/* Get key */
	fetch('/api/key').then(function(response) {
		return response.json();
	}).then(function(data) {
		secret_key = data.key;
		/* Set code */
		updateCode();

		/* Setup canvas */
		ctx.strokeStyle = '#8D6D15';
		ctx.lineWidth = 17;
		ctx.lineCap = 'round';
		ctx.shadowBlur = 5;
		ctx.shadowColor = '#8D6D15';

		/* Update canva render */
		setInterval(renderTime, 40);

		/* Update code every 30s */
		let timeout = 30 - (new Date().getSeconds() % 30);
		setTimeout(() => {	
			setInterval(updateCodeIfIsTime, 1000)
			updateCode();
		}, timeout * 1000);
	});
}

/* Time based OTP generation from common API key */
function getOTP(myKey) {
	var myKey = base32tohex(myKey);
	var epoch = Math.round(new Date().getTime() / 1000.0);
	var time = leftpad(dec2hex(Math.floor(epoch / 30)), 16, '0');
	var shaObj = new jsSHA("SHA-1", "HEX");
	shaObj.setHMACKey(myKey, "HEX");
	shaObj.update(time);
	var hmac = shaObj.getHMAC("HEX");
	var offset = hex2dec(hmac.substring(hmac.length - 1));
	var otp = (hex2dec(hmac.substr(offset * 2, 8)) & hex2dec('7fffffff')) + '';
	otp = (otp).substr(otp.length - 6, 6);
	return otp;
}

/* Misc in purpose to create OTP */
function dec2hex(s) { return (s < 15.5 ? '0' : '') + Math.round(s).toString(16); }

function hex2dec(s) { return parseInt(s, 16); }

function base32tohex(base32) {
	var base32chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";
	var bits = "";
	var hex = "";

	for (var i = 0; i < base32.length; i++) {
		var val = base32chars.indexOf(base32.charAt(i).toUpperCase());
		bits += leftpad(val.toString(2), 5, '0');
	}

	for (var i = 0; i+4 <= bits.length; i+=4) {
		var chunk = bits.substr(i, 4);
		hex = hex + parseInt(chunk, 2).toString(16) ;
	}
	return hex;
}

function leftpad(str, len, pad) {
	if (len + 1 >= str.length) {
		str = Array(len + 1 - str.length).join(pad) + str;
	}
	return str;
}