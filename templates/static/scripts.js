//level 1 functions
async function animation(queries){
    document.getElementById("play").hidden = true;
    document.getElementById("next").hidden = true;
    document.getElementById("pb1").hidden = true;
    document.getElementById("pb2").hidden = true;
    document.getElementById("pb3").hidden = true;
    document.getElementById("step_num").value = "0";
    document.getElementById("query_details").hidden = false;
    document.getElementById("canvas").hidden = false;
    document.getElementById("phrases").hidden = false;

    if(Object.keys(queries).includes('Error')){
        error(queries['Error']); 
        document.getElementById("query_details").hidden = true;
    }
    else{
        for(let i = 1; i <= Object.keys(queries).length; i++)
        {
            document.getElementById("step").innerHTML = i;
            document.getElementById("newssite").innerHTML = queries[i.toString()].newssite;
            document.getElementById("date_queried").innerHTML = queries[i.toString()].date_queried;
            document.getElementById("date_returned").innerHTML = queries[i.toString()].date_returned;
            if (Object.keys(queries[i.toString()]).includes('Error')){
                error(queries[i.toString()]['Error']);
                await sleep(4000);
            }
            else{
                document.getElementById("phrases").hidden = false;
                document.getElementById("canvas").hidden = false;
                bullseye(queries[i.toString()].len_text_formatted, queries[i.toString()].sentiments_formatted);
                longest_phrases(queries, i.toString());
                await sleep(4000);
            }
        }
        document.getElementById("play").hidden = false;
        document.getElementById("next").hidden = false;
    }

}

async function step(queries){
    var step = parseInt(document.getElementById("step_num").value);
    var next = 0;
    if (step == 0 || step == Object.keys(queries).length){
        next = 1;
    } else {
        next = step + 1;
    }


    document.getElementById("step_num").value = next.toString();
    document.getElementById("step").innerHTML = next.toString();
    document.getElementById("newssite").innerHTML = queries[next.toString()].newssite;
    document.getElementById("date_queried").innerHTML = queries[next.toString()].date_queried;
    document.getElementById("date_returned").innerHTML = queries[next.toString()].date_returned;
    if (Object.keys(queries[next.toString()]).includes('Error')){
        clearPhrases();
        error(queries[next.toString()]['Error']);
        document.getElementById("query_details").hidden = false; 
    }
    else{
        document.getElementById("query_details").hidden = false;
        document.getElementById("canvas").hidden = false;
        document.getElementById("phrases").hidden = false;

        bullseye(queries[next.toString()].len_text_formatted, queries[next.toString()].sentiments_formatted);
        longest_phrases(queries, next.toString());
        document.getElementById("pb1").hidden = false;
        document.getElementById("pb2").hidden = false;
        document.getElementById("pb3").hidden = false;
    }
}

//level 2 functions
async function bullseye(len_text, sentiments){
    clearCanvas();
    var c = document.getElementById("visualizations");
    var ctx = c.getContext("2d");
    for(let i = 0; i < sentiments.length; i++){
        await sleep(75);
        if (sentiments[i] != 0){
            ctx.beginPath();
            ctx.arc(250, 250, getEyeRad(len_text[i]), 0, 2 * Math.PI);
            ctx.closePath();
            ctx.fillStyle = getEyeHex(sentiments[i]);
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


async function longest_phrases(queries, step){
    clearPhrases();
    document.getElementById("response").innerHTML = "Longest Phrases:";    
    phrase_dict = queries[step].phrases;
    for(let i = 1; i <= 5; i++){
        document.getElementById("p" + i.toString()).innerHTML = phrase_dict['text'][i-1];
        await sleep(200); 
    }
}


async function most_positive_phrases(queries, step){
    clearPhrases();
    document.getElementById("response").innerHTML = "Most Positive Phrases:";
    phrase_dict = queries[step].phrases;
    //https://stackoverflow.com/questions/1063007/how-to-sort-an-array-of-integers-correctly
    //https://www.javascripttutorial.net/object/3-ways-to-copy-objects-in-javascript/
    sorted_sentiments = JSON.parse(JSON.stringify(phrase_dict['sentiments'])).sort(function (a, b) {  return a - b;  }).reverse();
    for(let i = 1; i <= 5; i++){
        document.getElementById("p" + i.toString()).innerHTML = phrase_dict['text'][phrase_dict['sentiments'].indexOf(sorted_sentiments[i-1])];
        await sleep(200); 
    }
}

async function most_negative_phrases(queries, step){
    clearPhrases();
    document.getElementById("response").innerHTML = "Most Negative Phrases:";
    phrase_dict = queries[step].phrases;
    sorted_sentiments = JSON.parse(JSON.stringify(phrase_dict['sentiments'])).sort(function (a, b) {  return a - b;  });
    for(let i = 1; i <= 5; i++){
        document.getElementById("p" + i.toString()).innerHTML = phrase_dict['text'][phrase_dict['sentiments'].indexOf(sorted_sentiments[i-1])];
        await sleep(200); 
    }
}

function error(error_message){
    document.getElementById("response").innerHTML = error_message;
    document.getElementById("canvas").hidden = true;
    document.getElementById("phrases").hidden = true;

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

function getEyeHex(num){
    if (num <= 0){
        return '#FF' + Math.round(256 + num*256).toString(16) + Math.round(256 + num*256).toString(16);
    } else{
        return "#" + Math.round(256 - num*256).toString(16) + 'FF' +  Math.round(256 - num*256).toString(16);
    }
}
