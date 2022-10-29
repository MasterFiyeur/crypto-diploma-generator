var canvas = document.getElementById('canvas');
var ctx = canvas.getContext('2d');
var timer = document.getElementById('timer');

function degToRad(degree) {
	var factor = Math.PI / 180;
	return degree * factor;
}

function renderTime() {
	var now = new Date();
	var seconds = now.getSeconds();
	var milliseconds = now.getMilliseconds();
  
	var newSeconds = seconds+(milliseconds/1000);
	timer.innerHTML = (30 - (seconds % 30)) + 's';

	ctx.fillStyle = '#F3DEA0';
	ctx.fillRect(0,0,300,300);

	//seconds
	ctx.beginPath();
	ctx.arc(150, 150, 130, degToRad(270), degToRad((newSeconds+2)*12)-90);
	ctx.stroke();
}


function init() {
	ctx.strokeStyle = '#8D6D15';
	ctx.lineWidth = 17;
	ctx.lineCap = 'round';
	ctx.shadowBlur = 5;
	ctx.shadowColor = '#8D6D15';
	setInterval(renderTime, 40);
	// Set interval 30s to refresh code with setTimeout to fit exactly to 30s base on actual time
}

init();