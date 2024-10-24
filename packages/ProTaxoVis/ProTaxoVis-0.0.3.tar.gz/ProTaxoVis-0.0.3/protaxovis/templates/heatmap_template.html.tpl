<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Heatmap</title>
<style type="text/css">
fieldset div {
	float: left;
	width: 50%;
}

legend {
	font-family: sans-serif;
	font-variant: small-caps;
}

span.left {
	float: left;
	color: black;
}

span.right {
	float: right;
	color: white;
}

#evalueNumber {
	border: solid 0px black;
	border-bottom: solid 1px black;
	width: 3em;
	font-size: 12pt;
}

#indicatordiv {
	border: 1px solid red;
	background-color: white;
	padding: 3px;
	position: absolute;
	left: -1000px;
	top: 0px;
}

#scalebar {
	display: inline-block;
	float: none;
	width: 150px;
	background-image: linear-gradient(to right, white, black);
}
</style>
</head>
<body>
<canvas id="c" width="<<<CWIDTH>>>" height="<<<CHEIGHT>>>"></canvas>

<form>
<div id="indicatordiv"><output id="indicator" size="30"></output></div>

<fieldset><legend>Absolute Values</legend>
<div>
Show only combinations with evalues better than:<br>
<input type="range" id="evalueSlider" value="30" min="0" max="150" step="1">
1e- <input type="number" id="evalueNumber" value="30" min="0" max="150">
</div>

<div>
In every enzyme/species combination that has a black dot, the particular enzyme was found in that species in Blast with an e-value better than the e-value chosen with the slider (or entered into the field).
</div>
</fieldset>

<p><button type="button" id="toggleAbsRel">Toggle absolute/relative</button> <button type="button" id="toggleAlphClus">Toggle alphabetical/clustered order</button></p>

<fieldset><legend>Relative Values</legend>
<div>
Color for relative values:
<select size="1" id="color">
<option value="grey">greyscale</option>
<option value="greenred">green → red</option>
<option value="redscale">redscale</option>
</select><br>
<div id="scalebar"><span class="left">1</span><span class="right">1e-150</span></div>
</div>

<div>
The color of every enzyme/species combination indicates the best e-value of the enzyme found in the species by Blast.
</div>
</fieldset>

</form>

<output id="debug"></output>

<script type="text/javascript">
'use strict';
const taxa = <<<TAXA>>>;

// alphabetically
const adata = <<<ADATA>>>;
const aproteins = <<<APROTEINS>>>;
const acluster = [];

// clustered
const cdata = <<<CDATA>>>;
const cproteins = <<<CPROTEINS>>>;
const ccluster = <<<CLUSTER>>>;

let data = cdata;
let proteins = cproteins;
let cluster = ccluster;

let isAbsolute = false;
let isClustered = true;
let oldPosX = -1000;
let oldPosY = -1000;

const rows = data.length;
const cols = data[0].length;

const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
ctx.font = '11px sans-serif';

const dendrogramoffset = 75;
const width = 12;
const height = 12;
const blockwidth = width - 1;
const blockheight = height - 1;
const halfwidth = width / 2;

const proteinBoxTop = height * rows + 10 + dendrogramoffset;
const taxaBoxLeft = width * cols + 10;

const COLORS = {
	BLACK: '#000000',
	WHITE: '#ffffff',
	GREEN: '#00aa00',
};

function drawProteins() {
	ctx.fillStyle = COLORS.WHITE;
	ctx.fillRect(0, proteinBoxTop, taxaBoxLeft, canvas.height);
	ctx.fillStyle = COLORS.BLACK;
	ctx.save();
	ctx.translate(0, 0);
	ctx.rotate(1.5 * Math.PI);
	ctx.textAlign = 'right';
	for(let i = 0; i < proteins.length; i++) {
		ctx.fillText(proteins[i], -1 * proteinBoxTop, (i + 1) * width + 2);
	}
	ctx.textAlign = 'left';
	ctx.restore();
}

function drawSpecies() {
	ctx.fillStyle = COLORS.WHITE;
	ctx.fillRect(taxaBoxLeft, dendrogramoffset, canvas.width, canvas.height);
	ctx.fillStyle = COLORS.BLACK;
	for(let i = 0; i < taxa.length; i++) {
		ctx.fillText(taxa[i], taxaBoxLeft, (i + 1) * height + 2 + dendrogramoffset);
	}
}

function drawDendrogram() {
	ctx.fillStyle = COLORS.WHITE;
	ctx.fillRect(0, 0, canvas.width, dendrogramoffset + 1);
	if(cluster.length > 0) {
		for(let i = 0; i < cluster.length; i++) {
			ctx.strokeStyle = cluster[i][0];
			ctx.beginPath();
			ctx.moveTo(cluster[i][1][0] * (taxaBoxLeft - blockwidth - 5) + halfwidth, dendrogramoffset - cluster[i][1][1] * dendrogramoffset);
			for(let j = 2; j < cluster[i].length; j++) {
				ctx.lineTo(cluster[i][j][0] * (taxaBoxLeft - blockwidth - 5) + halfwidth, dendrogramoffset - cluster[i][j][1] * dendrogramoffset);
			}
			ctx.stroke();
		}
		ctx.strokeStyle = COLORS.BLACK;
	}
	ctx.fillStyle = COLORS.BLACK;
}


const evalueSlider = document.getElementById('evalueSlider');
const evalueNumber = document.getElementById('evalueNumber');
const indicator = document.getElementById('indicator');
const indicatordiv = document.getElementById('indicatordiv');
const colorSelect = document.getElementById('color');
// const debug = document.getElementById('debug');

const scalebar = document.getElementById('scalebar');

function getMousePos(c, evt) {
	const rect = c.getBoundingClientRect();
	return [evt.clientX - rect.left, evt.clientY - rect.top];
}

function highlightPos(x, y) {
	ctx.fillStyle = COLORS.WHITE;
	ctx.fillRect(0, proteinBoxTop - 5, taxaBoxLeft, 5);                 // lower
	ctx.fillRect(taxaBoxLeft - 5, dendrogramoffset, 5, proteinBoxTop);  // right
	ctx.fillRect(0, dendrogramoffset, taxaBoxLeft, 5);                  // upper
	ctx.fillRect(0, dendrogramoffset, 5, proteinBoxTop);                // left
	ctx.fillStyle = COLORS.GREEN;

	ctx.strokeStyle = COLORS.WHITE;
	ctx.beginPath();
	ctx.rect(oldPosX + 0.5, dendrogramoffset + 4.5, width, height*rows);
	ctx.rect(4.5, oldPosY + 0.5, width * cols, height);
	ctx.stroke();

	let row = -1;
	let col = -1;
	ctx.strokeStyle = COLORS.GREEN;

	if(x > 5 && x < width * cols + 5) {
		const posX = Math.floor((x - 5) / width) * width + 4;
		oldPosX = posX;
		ctx.beginPath();
		ctx.rect(posX + 0.5, dendrogramoffset + 4.5, width, height*rows);
		ctx.stroke();
		ctx.fillRect(posX, proteinBoxTop - 5, blockwidth + 2, 5);
		ctx.fillRect(posX, dendrogramoffset, blockwidth + 2, 5);
		col = Math.floor((x - 5) / width);
	}

	if(y > 5 + dendrogramoffset && y < height * rows + 5 + dendrogramoffset) {
		const posY = Math.floor((y - 5 - dendrogramoffset) / height) * height + 4 + dendrogramoffset;
		oldPosY = posY;
		ctx.beginPath();
		ctx.rect(4.5, posY + 0.5, width * cols, height);
		ctx.stroke();
		ctx.fillRect(taxaBoxLeft - 5, posY, 5, blockheight + 2);
		ctx.fillRect(0, posY, 5, blockheight + 2);
		row = Math.floor((y - 5 - dendrogramoffset) / height);
	}
	ctx.strokeStyle = COLORS.BLACK;

	if(row >= 0 && col >= 0) {
		let v = data[row][col];
		if(v === -100) {
			v = '> 0';
		}
		else if(v === 200) {
			v = '< -150';
		}
		else {
			v = `-${v}`;
		}
		indicator.value = v;
		indicatordiv.style.left = `${x + 20}px`;
		indicatordiv.style.top = `${y + 30}px`;
	}
	else {
		indicator.value = '';
		indicatordiv.style.left = '-1000px';
		indicatordiv.style.top = '0px';
	}
}

function drawRectAbs(ctx, x, y, fill) {
	if(fill) {
		fill = COLORS.BLACK;
	}
	else {
		fill = COLORS.WHITE;
	}
	drawRect(ctx, x, y, fill);
}

function drawRect(ctx, x, y, fill) {
	ctx.fillStyle = fill;
	ctx.fillRect(x * width + 5, y * height + 5 + dendrogramoffset, blockwidth, blockheight);
}

function updateCanvas(source) {
	const evalue = parseInt(source.value);
	evalueNumber.value = evalue;
	evalueSlider.value = evalue;
	if(isAbsolute) {
		makeCanvasAbsolute(evalue);
	}
	else {
		makeCanvasRelative();
	}
}

function makeCanvasAbsolute(evalue) {
	isAbsolute = true;
	for(let row = 0; row < data.length; row++) {
		for(let col = 0; col < data[0].length; col++) {
			drawRectAbs(ctx, col, row, data[row][col] >= evalue);
		}
	}
}

const colorScales = {
	greyscale: {'min': 'hsl(0, 0%, 100%)', 'max': 'hsl(0, 0%, 0%)'},
	redscale: {'min': 'hsl(0, 100%, 100%)', 'max': 'hsl(0, 100%, 50%)'},
	greenred: {'min': 'hsl(0, 100%, 50%)', 'max': 'hsl(120, 100%, 50%)'},
};

function makeCanvasRelative() {
	isAbsolute = false;
	const emax = 150;
	const emin = 0;

	const key = colorSelect.value in colorScales ? colorSelect.value : 'greyscale';

	scalebar.style.backgroundImage = `linear-gradient(to right, ${colorScales[key].min}, ${colorScales[key].max})`;

	for(let row = 0; row < data.length; row++) {
		for(let col = 0; col < data[0].length; col++) {
			let fill = '#ffff00';
			if(data[row][col] > emax) {
				fill = colorScales[key].max;
			}
			else if(data[row][col] < emin) {
				fill = colorScales[key].min;
			}
			else {
				let clr;
				if(key == 'greenred') {
					clr = Math.round(((data[row][col] - emin)/emax) * 120);
					fill = `hsl(${clr}, 100%, 50%)`;
				}
				else if(key == 'redscale') {
					clr = 100 - Math.round(((data[row][col] - emin)/emax/2) * 100);
					fill = `hsl(0, 100%, ${clr}%)`;
				}
				else {
					clr = 100 - Math.round(((data[row][col] - emin)/emax) * 100);
					fill = `hsl(0, 0%, ${clr}%)`;
				}
			}
			drawRect(ctx, col, row, fill);
		}
	}
}

function toggleAbsRel() {
	if(isAbsolute) {
		makeCanvasRelative();
	}
	else {
		makeCanvasAbsolute(+evalueSlider.value);
	}
}

function toggleAlphClus() {
	if(isClustered) {
		isClustered = false;
		data = adata;
		proteins = aproteins;
		cluster = acluster;
	}
	else {
		isClustered = true;
		data = cdata;
		proteins = cproteins;
		cluster = ccluster;
	}
	drawAll();
}

function drawAll() {
	drawDendrogram();
	drawProteins();
	drawSpecies();
	updateCanvas(evalueSlider);
}

drawAll();

canvas.addEventListener('mousemove', function(evt) {
	const mousePos = getMousePos(canvas, evt);
	highlightPos(mousePos[0], mousePos[1]);
});

canvas.addEventListener('mouseout', function(_evt) {
	highlightPos(width * cols * 2, height * rows * 2);
});

const mouseWheelEvent = (/Firefox/i.test(navigator.userAgent)) ? 'DOMMouseScroll' : 'mousewheel';

canvas.addEventListener(mouseWheelEvent, function(evt) {
	const direction = evt.detail ? -1 * evt.detail : evt.wheelDelta;
	if(direction > 0) {
		evalueSlider.value++;
	}
	else {
		evalueSlider.value--;
	}
	updateCanvas(evalueSlider);
	return false;
});

document.getElementById('evalueSlider').addEventListener('input', updateCanvas);
document.getElementById('evalueNumber').addEventListener('input', updateCanvas);
document.getElementById('toggleAbsRel').addEventListener('click', toggleAbsRel);
document.getElementById('toggleAlphClus').addEventListener('click', toggleAlphClus);
document.getElementById('color').addEventListener('change', makeCanvasRelative);
</script>
</body>
</html>
