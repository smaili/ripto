/*--------------------------------------------------

index.js
Used on first page

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

        results = rt.getByClass('results')[0],
        filter_form = rt.getByTag('form', results)[0],
        filter_select = rt.getByTag('select', filter_form)[0],
        time_select = rt.getByTag('select', filter_form)[1];



    /*
        --- Init ---
    */

    memorials.page = '/';
    memorials.data['f'] = filter_select.options[filter_select.selectedIndex].value;
    memorials.data['t'] = time_select.options[time_select.selectedIndex].value;
    memorials.init();



    /*
            --- Listeners ---
    */

    filter_select.onchange = time_select.onchange = function() {
        filter_form.submit();
    };

})();
