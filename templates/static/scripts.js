
/*function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}*/

function clearCanvas(){
    var c = document.getElementById("results");
	var ctx = c.getContext('2d');
	ctx.clearRect(0, 0, 500, 500);
}

var len_text = [143, 136, 132, 130, 111, 111, 106, 106, 103, 103, 102, 101, 98, 97, 96, 94, 93, 86, 75, 58, 49, 49, 49, 47, 45, 45, 44, 42, 40, 40, 39, 39, 39, 38, 38, 36, 36, 34, 34, 33, 32, 32, 31, 27, 27, 24, 24, 23, 22, 21, 21, 20, 20, 20, 20, 20, 18, 18, 18, 18, 18, 18, 17, 17, 17, 17, 17, 17, 17, 17, 17, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 15, 15, 15, 15, 15, 15, 15, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12, 12, 12, 12, 12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11]; 
var sentiments = [-0.6486, -0.8074, 0.4939, -0.807, 0.2732, -0.6486, 0.0258, -0.765, 0.7778, 0.7778, 0.5719, 0.0, -0.0258, 0.734, 0.0, 0.0, -0.2732, 0.2732, 0.0, 0.0772, 0.0, -0.7906, 0.3818, 0.4588, 0.0, 0.0, 0.2263, 0.1027, 0.0, 0.0, -0.5423, -0.0516, 0.3818, 0.4215, 0.0, 0.0, -0.296, 0.0, 0.0, 0.0, -0.6808, 0.0, 0.0, 0.4019, 0.0, 0.0, 0.0, 0.4404, 0.0, 0.0516, 0.0, 0.0, 0.4215, 0.0, 0.0, 0.0, 0.4215, 0.0, 0.0, 0.0, 0.0, 0.4215, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2716, 0.4019, 0.0, 0.0, 0.0, 0.0, 0.5859, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4019, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4215, 0.4215, 0.4404, 0.0, 0.0, 0.4215, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2732, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4215, 0.0, 0.0, 0.0, 0.0, 0.0];
function drawSAEye(){
    clearCanvas();
    var c = document.getElementById("results");
    var ctx = c.getContext("2d");
    for(let i = 0; i < sentiments.length; i++){
        if (sentiments[i] != 0){
            ctx.beginPath();
            ctx.arc(250, 250, getEyeRad(len_text[i]), 0, 2 * Math.PI);
            ctx.closePath();
            ctx.fillStyle = getSAHex(sentiments[i]);
            ctx.lineWidth = 0;
            //ctx.stroke();
            ctx.fill();
        }
    }   
}

function drawSABeads(){
    clearCanvas();
}

function getEyeRad(length){
    radius = Math.round(50 + length);
    if(radius > 250){
        radius = 250;
    }
    return radius;
}

function getSAHex(num){
    if (num <= 0){
        return '#FF' + Math.round(256 + num*256).toString(16) + Math.round(256 + num*256).toString(16);
    } else{
        return "#" + Math.round(256 - num*256).toString(16) + 'FF' +  Math.round(256 - num*256).toString(16);
    }
}

parameters = {}
function getPythonParameters(pmeters) {
    parameters = pmeters;
}

window.onLoad = drawSAEye();