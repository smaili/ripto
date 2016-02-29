/*--------------------------------------------------

results.js
Used on search results page

-------------------------------------------------- */



(function() {

    /*
        --- Imports ---
    */

    var
        memorials = rt.memorials,



    /*
        --- Locals ---
    */

        query = rt.getByClass('search-input')[0].value;



    /*
        --- Init ---
    */

    memorials.page = '/results';
    memorials.data['q'] = query;
    memorials.init();

})();
