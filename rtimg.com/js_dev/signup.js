/*--------------------------------------------------

signup.js
Used when signing up

-------------------------------------------------- */



(function() {

    /*
        --- Imports ---
    */

    var
        form = rt.form,
        ajax = rt.ajax;



    /*
        --- Locals ---
    */



    /*
        --- Private Helpers ---
    */

    function _scorePassword(word) {
        var score = 0;
        if ( !word )
            return score;

        // award every unique letter until 5 repetitions
        var letters = {};
        for ( var i = 0; i < word.length; i++ ) {
            letters[ word[i] ] = ( letters[ word[i] ] || 0 ) + 1;
            score+= 5.0 / letters[ word[i] ];
        }

        // bonus points for mixing it up
        var variations = {
            digits: /\d/.test(word),
            lower: /[a-z]/.test(word),
            upper: /[A-Z]/.test(word),
            nonWords: /\W/.test(word)
        }

        variationCount = 0;
        for ( var check in variations ) {
            variationCount += ( variations[check] == true ) ? 1 : 0;
        }
        score += ( variationCount - 1 ) * 10;

        return parseInt(score);
    }



    /*
        --- Register Validators ---
    */

    form.lookups['check_username'] = function(input) {
        if (input.value.length) {
            var side = rt.getByClass( 'sidetip', rt.getParent(input, 'holding') )[0];
            form.showSideTip(side, 'checking');
            ajax.get('/field_ok', { 'u' : input.value },
                function(data) {
                    form.showSideTip(side, data['valid']);
            });
        } else {
            return 'blank';
        }

        return false;
    };

    form.lookups['check_password'] = function(input) {
        var word = input.value,
            finalScore = 0,
            result = 'blank';

        if (!word.length) {}
        else if (word.length < 6) {
            result = 'invalid';
            finalScore = word.length * 2;
        } else {
            var score = _scorePassword(input.value),
                whichSide;
            switch (true) {
                case ( score > 80 ): whichSide = 'perfect'; break;
                case ( score > 50 ): whichSide = 'ok'; break;
                case ( score >=30 ): whichSide = 'weak'; break;
                default: whichSide = 'tooweak'; break;
            }
            result = whichSide;
            finalScore = score/2;
        }
        
        var scorebar = rt.getByClass( 'fill', rt.getParent(input, 'prompt') )[0],
            i = 0,
            rounded = finalScore|0,
            current = +scorebar.style.width.slice(0,-2);
        if (rounded == 0 && current == 0 ) {}
        else {
            var can_grow = current <= finalScore;
            (function bar() {
                ( scorebar.style.width = ( +scorebar.style.width.slice(0,-2) + (can_grow? 1 : -1)  )+'px' ) == (rounded + 'px') ? scorebar.style.width = finalScore : setTimeout(bar, 40);
            })();
        }

        return result;
    };



    /*
            --- Initialization ---
    */

    form.listen();

})();
