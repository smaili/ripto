/*--------------------------------------------------

home.js
Used on home

-------------------------------------------------- */



(function() {

    /*
        --- Imports ---
    */

    var
        form = rt.form,
        ajax = rt.ajax,



    /*
        --- Locals ---
    */

        results = rt.getByClass('results')[0];



    /*
            --- Listeners ---
    */



    /*filter_select.onchange = time_select.onchange = function() {
        rt.addClass(results, 'changing');

        var f_index = filter_select.selectedIndex,
            f_name = filter_select.options[f_index].text,
            f_val = filter_select.options[f_index].value,

            t_index = time_select.selectedIndex,
            t_name = time_select.options[t_index].text,
            t_val = time_select.options[t_index].value;

        filter_text.innerHTML = f_name;
        time_text.innerHTML = t_name;


        ajax.get( '/', { 'f':f_val, 't':t_val },
            function(data) {
                memorials.innerHTML = data;
                rt.removeClass(results, 'changing');
                setup_show_more();
                page_offset = 0;
        }, 'html');
    };*/

})();
