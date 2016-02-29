/*--------------------------------------------------

memorials.js
Used for handling memorial lists

-------------------------------------------------- */



rt.memorials = new function() {

    /*
        --- Imports ---
    */

    var
        ajax = rt.ajax,



    /*
        --- Locals ---
    */

        me = this,
        page_offset = 0, // we start off with 0 by default since initially we just see the first loaded results (which means first page)
        results = rt.getByClass('results')[0],
        memorials = rt.getByClass('memorial-list', results)[0];



    /*
        --- Private Helpers ---
    */

    function get_show_more() {
        var b = rt.getByTag('button', results);
        return b? b[0] : false;
    }



    /*
        --- Public Helpers ---
    */

    me.page = '';

    me.data = {};

    me.init = function() {
        var show_more = get_show_more();
        if (show_more) {
            show_more.onclick = function(e) {
                rt.prevente(e);
                rt.removeEl(show_more);
                me.data['p'] = ++page_offset;

                ajax.get( me.page, me.data,
                    function(data) {
                        memorials.innerHTML+= data;
                        me.init();
                }, 'html');
            };
        }
    };



    /*
            --- Listeners ---
    */


};

