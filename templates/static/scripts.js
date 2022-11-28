function drawEye(){
    var c = document.getElementById("results");
    var ctx = c.getContext("2d");
    ctx.beginPath();
    ctx.arc(95, 50, 40, 0, 2 * Math.PI);
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(105, 60, 40, 0, 2 * Math.PI);
    ctx.stroke();
}

parameters = {}
function getPythonParameters(pmeters) {
    parameters = pmeters;
}

//window.onLoad = drawEye();