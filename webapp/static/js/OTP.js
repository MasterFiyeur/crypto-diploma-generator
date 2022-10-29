const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const timer = document.getElementById('timer');

let code = "000000";
let key = "12345678901234567890123456789012";

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

function updateCode() {
	document.getElementById('code').innerHTML = code;
	/* Calculate code for next update */
	code = "123456";
	console.log("Code updated " + new Date().toLocaleTimeString());
}

function init() {
	/* Get key */
	fetch('/api/key').then(function(response) {
		return response.json();
	}).then(function(data) {
		key = data.key;
	});

	/* Set code */
	updateCode();

	/* Setup canva */
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
		setInterval(updateCode, 30000)
		updateCode();
	}, timeout * 1000);
}

init();