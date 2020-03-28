$(async function () {
    //Select useful elements of index.html
    class BoggleGame {
        constructor(secs) {
            //timer data
            this.secs = secs;
            this.timer = setInterval(this.countdown.bind(this), 1000);
    
            //game data
            this.score = 0;
            this.words = new Set();
        }
    
        addWordList(word) {
            this.words.add(word);
            
        }
    
        addScore(score) {
            this.score += score;
        }
    
        showTimer(seconds) {
            $(".timer")
            .text(seconds)
        }
    
        async countdown() {
            this.secs -= 1;
            this.showTimer(this.secs);
    
            if(this.secs == 0) {
                clearInterval(this.timer);
                await this.scoreGame(this);
            }
        }
    
        async scoreGame(game) {
            $('#submit-word').hide();
            const res = await axios.post("/post-score", { score : game.score});
            if(res.data.record) {
                showMessage(`New Record: ${game.score}`, "ok");
            } else {
                showMessage(`Final Score: ${game.score}`, "ok");
            }
        }
    }

    $submitword = $("#submit-word");

    const game = new BoggleGame(60);
    game.showTimer(game.secs);
    game.countdown(game);

    $submitword.on("submit", async evt => {
        evt.preventDefault();
        const $newWord = $("#newWord");

        let word = $newWord.val();

        if(game.words.has(word)) {
            showMessage(`${word} has already been guessed`, "err");
            return;
        }

        const res = await axios.get("/check-word", {params: {word: word}});
        if(res.data.res === "not-word") {
            showMessage(`${word} is not a word in our dictionary`, "err");
        } else if(res.data.res === "not-on-board") {
            showMessage(`${word} is not a word on the board`, "err");
        } else {
            showMessage(`${word} is a valid word! Good job!`, "ok");
            game.addWordList(word);
            showAddWordList(word);
            game.addScore(word.length);
            showScore(game.score);
        }

        $newWord.val('').focus();
    
    });

    function showMessage(msg, err) {
        $(".msg")
        .text(msg)
        .removeClass()
        .addClass(`msg ${err}`);

    }

    function showScore(score) {
        $(".score")
        .text(score)
    }

    function showAddWordList(word) {
        $(".validWords")
        .append($("<li>")
            .append($('<p>')
                .append(`${word}`)
                    )
                );
    }


});