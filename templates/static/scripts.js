
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
 }

function clearCanvas(){
    var c = document.getElementById("visualizations");
	var ctx = c.getContext('2d');
	ctx.clearRect(0, 0, 500, 500);
}

function clearPhrases(){
    for(let i = 1; i <= 5; i++){
        document.getElementById("t" + i.toString()).innerHTML = "";
    }
}

async function SAEyeAnimation(len_text, sentiments){
    clearCanvas();
    var c = document.getElementById("visualizations");
    var ctx = c.getContext("2d");
    for(let i = 0; i < sentiments.length; i++){
        await sleep(20);
        if (sentiments[i] != 0){
            ctx.beginPath();
            ctx.arc(250, 250, getEyeRad(len_text[i]), 0, 2 * Math.PI);
            ctx.closePath();
            ctx.fillStyle = getSAEyeHex(sentiments[i]);
            ctx.lineWidth = 0;
            ctx.fill();
        }
    }
    ctx.font = "12px Libre Franklin";
    ctx.fillStyle = "black";
    ctx.textAlign = "center";
    ctx.fillText("200", 485, 250); 
    ctx.fillText("100", 400, 250);
    ctx.fillText("10", 310, 250);
    await sleep(3000);   
}

async function longest_phrases(phrases){
    clearPhrases();
    for(let i = 1; i <= 5; i++){
        document.getElementById("t" + i.toString()).innerHTML = phrases['text'][i-1];
        //document.getElementById("t" + i.toString()).style.color = getSAPhraseHex(phrases['sentiments'][i]);
        await sleep(500); 
    }
    
}

async function most_positive_phrases(phrases){
    clearPhrases();
    sorted_sentiments = phrases['sentiments'].sort().reverse();
    for(let i = 1; i <= 5; i++){
        document.getElementById("t" + i.toString()).innerHTML = phrases['text'][phrases['sentiments'].indexOf(sorted_sentiments[i-1])];
        await sleep(500); 
    }
}

async function most_negative_phrases(phrases){
    clearPhrases();
    sorted_sentiments = phrases['sentiments'].sort();
    for(let i = 1; i <= 5; i++){
        document.getElementById("t" + i.toString()).innerHTML = phrases['text'][phrases['sentiments'].indexOf(sorted_sentiments[i-1])];
        await sleep(500); 
    }
}


function getEyeRad(length){
    radius = Math.round(50 + length);
    if(radius > 250){
        radius = 250;
    }
    return radius;
}

function getSAEyeHex(num){
    if (num <= 0){
        return '#FF' + Math.round(256 + num*256).toString(16) + Math.round(256 + num*256).toString(16);
    } else{
        return "#" + Math.round(256 - num*256).toString(16) + 'FF' +  Math.round(256 - num*256).toString(16);
    }
}


function getSAPhraseHex(num){
    if (num <= 0){
        return '#C8' + Math.round(256 + num*256).toString(16) + Math.round(256 + num*256).toString(16);
    } else{
        return "#" + Math.round(256 - num*256).toString(16) + 'C8' +  Math.round(256 - num*256).toString(16);
    }
}
