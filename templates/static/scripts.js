//level 1 functions
async function animation(queries){
    for(let i = 1; i <= 4; i++)
    {
        document.getElementById("step").innerHTML = i;
        document.getElementById("newssite").innerHTML = queries[i.toString()].newssite;
        document.getElementById("date_queried").innerHTML = queries[i.toString()].date_queried;
        document.getElementById("date_returned").innerHTML = queries[i.toString()].date_returned;
        bullseye(queries[i.toString()].len_text_formatted, queries[i.toString()].sentiments_formatted);
        phrases(queries[i.toString()].phrases);
        await sleep(5000);
    }
}

async function step(queries){
    step = parseInt(document.getElementById("step_num").value);
    if (step == 0 || step == 4){
        next = 1;
    } else {
        next = step + 1;
    }
    document.getElementById("step_num").value = next.toString();
    document.getElementById("step").innerHTML = next;
    document.getElementById("newssite").innerHTML = queries[next.toString()].newssite;
    document.getElementById("date_queried").innerHTML = queries[next.toString()].date_queried;
    document.getElementById("date_returned").innerHTML = queries[next.toString()].date_returned;
    bullseye(queries[next.toString()].len_text_formatted, queries[next.toString()].sentiments_formatted);
    phrases(queries[next.toString()].phrases);

}

//level 2 functions
async function bullseye(len_text, sentiments){
    clearCanvas();
    var c = document.getElementById("visualizations");
    var ctx = c.getContext("2d");
    for(let i = 0; i < sentiments.length; i++){
        await sleep(100);
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
}

async function phrases(phrases){
    clearPhrases();
    for(let i = 1; i <= 5; i++){
        document.getElementById("p" + i.toString()).innerHTML = phrases['text'][i-1];
        await sleep(500); 
    }
    
}

async function most_positive_phrases(phrases){
    clearPhrases();

    //https://stackoverflow.com/questions/1063007/how-to-sort-an-array-of-integers-correctly
    //https://www.javascripttutorial.net/object/3-ways-to-copy-objects-in-javascript/
    sorted_sentiments = JSON.parse(JSON.stringify(phrases['sentiments'])).sort(function (a, b) {  return a - b;  }).reverse();
    for(let i = 1; i <= 5; i++){
        document.getElementById("p" + i.toString()).innerHTML = phrases['text'][phrases['sentiments'].indexOf(sorted_sentiments[i-1])];
        await sleep(100); 
    }
}

async function most_negative_phrases(phrases){
    clearPhrases();
    sorted_sentiments = JSON.parse(JSON.stringify(phrases['sentiments'])).sort(function (a, b) {  return a - b;  });
    for(let i = 1; i <= 5; i++){
        document.getElementById("p" + i.toString()).innerHTML = phrases['text'][phrases['sentiments'].indexOf(sorted_sentiments[i-1])];
        await sleep(100); 
    }
}

//level 3 functions
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
        document.getElementById("p" + i.toString()).innerHTML = "";
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

/*function create_legend(){
    var c = document.getElementById("legend");
    var ctx = c.getContext("2d");

    var grd = ctx.createLinearGradient(0, 0, 300, 0);
    grd.addColorStop(1, "#FF0000");
    grd.addColorStop(0.5 ,"#FFFFFF");
    grd.addColorStop(0, "#00FF00");
    ctx.fillStyle = grd;
    ctx.fillRect(0, 0, 300, 75);

    ctx.font = "12px Libre Franklin";
    ctx.fillStyle = "black";
    ctx.textAlign = "center";
    ctx.fillText("-1", 10, 37); 
    ctx.fillText("-0.5", 80, 37); 
    ctx.fillText("0", 150, 37);
    ctx.fillText("+0.5", 220, 37);
    ctx.fillText("+1", 290, 37);
}*/