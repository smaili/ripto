/*--------------------------------------------------

admin.js
Used for admin page

-------------------------------------------------- */



(function() {

    /*
        --- Imports ---
    */

    var
        modal = rt.modal,
        calendar = rt.calendar,



    /*
        --- Locals ---
    */

        admin_bar = rt.getByClass('abar')[0],
        section_containers = rt.getByClass('section-container');


    /*
        --- Private Helpers ---
    */

    function enable_funeral() {
        rt.show(dof);
        rt.show(floc);
    }

    function disable_funeral() {
        rt.hide(dof);
        rt.hide(floc);
    }


    /*
        --- Register Helpers ---
    */
    admin_bar.onclick = function(e) {
        var t = rt.getTarget(e),
            submit = rt.hasClass(t, 'submit')? t : rt.getParent(t, 'submit', admin_bar);

        if ( submit && rt.hasClass( submit.parentNode, 'abar' ) ) {
            var section = rt.getAttr( submit, 'data-section' );
            for ( var i = 0; i < section_containers.length; i++ ) {
                if ( rt.hasClass(section_containers[i], section) && rt.hasClass(section_containers[i], 'hidden') ) {
                    rt.show( section_containers[i] );
                } else {
                    rt.hide( section_containers[i] );
                }
            }
            submit.blur(); // forces outline and hover color to go away
        }
    }


    /*
        --- Register Validators ---
    */




    /*
            --- Additional Listeners ---
    */

    var dates = [ rt.getById('comments-date') ],
        calendar_modal = rt.getById('calendar-dialog'),
        shown = false,
        i = 0;

    for (; i < dates.length; i++) {
        // closure
        (function (input) {
            input.onfocus = function(e) {
                rt.prevente(e); input.blur();

                var date = input.value,
                    header = rt.getAttr(input, 'data-modal-header');


                if (date || shown) {
                    if ( date && (date = date.split('/')) && date.length == 3 ) {
                        date = new Date( +date[2], +date[0] - 1, +date[1] ); // MM/DD/YYYY
                    } else {
                        date = new Date();
                    }
                    calendar.change_date(date);

                } else {
                    shown = true;
                }

                calendar.on_select(function(new_date) {
                    var m = new_date.getMonth() + 1,
                        d = new_date.getDate(),
                        y = new_date.getFullYear();

                    input.value = ( m < 10? '0' : '' ) + m + '/' + ( d < 10? '0' : '' ) + d + '/' + y; // MM/DD/YYYY
                    input.onblur(); // trick that triggers form.check_placeholder
                    modal.hide(calendar_modal);
                });

                modal.changeMenuLink('calendar-dialog', header);
                modal.show('calendar-dialog');

            };
        })(dates[i]);
    }

})();
