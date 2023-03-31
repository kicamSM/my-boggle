// this file will handle clicks from the dom and then make axios calls to the flask routes 
"use strict"

let score = 0; 
let wordCount = 0;
let seconds = 60; 
let validWords = [];

$("#board-form").on("submit", handleSubmit);

async function handleSubmit(e) {
    e.preventDefault();
    let word = $("input").val();
    console.log(word)
    if(!word) return;
    const res = await axios.get("/check-word", { params: {word: word} });
    // how do we know this is the format needed { params: {word: word} })
    console.log(res)
    let response = res.data.result;
    $("#response").html(response); 
    // this is returning a phrase that is determined by the route that is calling the function check_for_valid_word in boggle.py 
    $("#board-form").trigger("reset");
    // reseting the input field
    console.log(response)
    adjustScore();
    adjustWordCount(); 
    startTimer();

    async function adjustScore() {
        console.log(word)
        if(response === "ok" && validWords.includes(word) === false) {
            score += word.length; 
            console.log(word.length)
            console.log(score)
            $("#score").html(`Score: ${score}`);
        } else if (response == "not-word") {
            return;
        } else { (response === "not-on-board")
            return;
        }
    }
     
    async function adjustWordCount() {
        if(response === "ok"&& validWords.includes(word) === false) {
            validWords.push(word)
            wordCount += 1; 
            console.log(wordCount)
            $("#word-count").html(`You have found ${wordCount} valid words`);
        } else if (response == "not-word") {
            return;
        } else { (response === "not-on-board")
            return;
        }
    }

    const timer = setInterval(startTimer, 1000)

    async function startTimer() {
        $("#timer").html(seconds);
        seconds --;
        if(seconds < 1) {
            $("#timer").html("0")
            $("#word-input").attr('disabled', 'disabled');
            endGame(); 
            clearInterval(timer);
        }
    }


    async function endGame() {
        await axios.post("/end-game", {score: score});
    }
}






