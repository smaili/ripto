/*--------------------------------------------------

notice.js
Used for showing/hiding notice boxes

-------------------------------------------------- */



rt.notice = new function() {

    /*
        --- Imports ---
    */

    var



    /*
        --- Locals ---
    */
        me = this,
        notices = rt.getByClass('notice-box');


    /*
        --- Public Helpers ---
    */

    me.show = function(notice) {
        rt.show(notice);
    };

    me.hide = function(notice) {
        rt.hide(notice);
    };

    me.change = function(notice, text) {
        var t = rt.getByTag('span', notice)[0];
        t.innerHTML = text;
    }



    /*
            --- Listeners ---
    */

    for (var i = 0; i < notices.length; i++) {
        var notice = notices[i],
            close = rt.getByClass('close', notice)[0];

        // closure
        (function (c, n) {
            c.onclick = function(e) {
                rt.prevente(e);
                me.hide(n);
            };
        })(close, notice);
    }

};
