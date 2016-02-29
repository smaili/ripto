/*--------------------------------------------------

edit_new_memorial.js
Common js for editing and creating memorials

-------------------------------------------------- */



(function() {

    /*
        --- Imports ---
    */

    var
        form = rt.form,
        ajax = rt.ajax,
        notice = rt.notice,
        modal = rt.modal,
        calendar = rt.calendar,



    /*
        --- Locals ---
    */

        ftype_select = rt.getByClass('ftype-select')[0],
        dof = rt.getByClass('dof')[0],
        floc = rt.getByClass('floc')[0];


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
    ftype_select.onchange = function() {
        if ( ftype_select.selectedIndex == ftype_select.length - 1 ) {
            disable_funeral();
        } else {
            enable_funeral();
        }
    }


    /*
        --- Register Validators ---
    */




    /*
            --- Additional Listeners ---
    */

    var
        //container
        select_container = rt.getById('select-container'),
        selected_container = rt.getById('selected-container'),

        // inputs
        file_input = rt.getById('photo-upload'),
        check_input = rt.getById('nophoto'),
        save_button = rt.getByClass('submit', selected_container)[0], // i.e., jQuery('#selected-container .submit').eq(0)

        // images
        saved_image = rt.getByClass('img-selectedphoto', select_container)[0], // i.e., jQuery('#select-container .img-selectedphoto')
        select_image = rt.getByClass('img-selectphoto', select_container)[0], // i.e., jQuery('#select-container .img-selectphoto')
        no_image = rt.getByClass('img-nophoto', select_container)[0], // i.e., jQuery('#select-container .img-nophoto')

        // directions
        h4_change = rt.getByTag('h4', selected_container)[0], // i.e., jQuery('#selected-container h4').eq(0)
        h4_select = rt.getByTag('h4', selected_container)[1], // i.e., jQuery('#selected-container h4').eq(1)

        // status
        new_filename = rt.getByClass('selected-filename', selected_container)[0], // i.e., jQuery('#selected-container .selected-filename')
        side = rt.getByClass('sidetip', rt.getParent(file_input, 'photo'))[0], // i.e., file_input.parents('.photo').find('.sidetip')

        // trackers
        saving = false, // TODO - replace saving var by just checking if save_button has 'wait' class
        saved = rt.isVisible(saved_image);

    function show_notice(notice_type) {
        hide_notices();
        for (var i = 0; i < side.children.length; i++) {
            if ( rt.hasClass( side.children[i], notice_type ) ) {
                notice.show( side.children[i] );
            }
        }
    }

    function check_file(input) {
        var file = input.value.split('\\').pop(),
            exts = {'png':0, 'jpg':0, 'jpeg':0, 'gif':0},
            ext = file.split('.').pop().toLowerCase();

        var result = 'blank';
        if (file.length) {
            if (ext in exts) {
                result = 'ok';
            } else {
                result = 'invalid';
            }
        }

        return result;
    }

    function hide_notices() {
        for (var i = 0; i < side.children.length; i++) {
            notice.hide( side.children[i] );
        }
    }

    function clear_file_input() {
        // i.e., file_input.replaceWith( file_input = file_input.clone( true ) );
        var new_file_input = file_input.cloneNode(false);
        new_file_input.onchange = file_input.onchange;
        file_input.parentNode.replaceChild(new_file_input, file_input);
        file_input = new_file_input;

        new_filename.innerHTML = '';
        rt.hide(save_button);
    }

    function show_image(which) {
        rt.hide(saved_image); rt.hide(select_image); rt.hide(no_image);
        rt.hide(h4_change); rt.hide(h4_select);
        if (which == 'saved') {
            rt.show(saved_image);
            rt.show(h4_change);
        }
        else if (which == 'select') {
            rt.show(select_image);
            rt.show(h4_select);
        }
        else {
            rt.show(no_image);
        }
    }

    function selected_ok_file(filename) {
        rt.hide(h4_select); rt.hide(h4_change);
        rt.show(save_button);
        hide_notices();
        new_filename.innerHTML = filename;
    }

    function selected_bad_file(filename) {
        if (saved) {
            show_image('saved');
        } else {
            show_image('select');
        }

        if (filename) show_notice('invalid');
        else hide_notices();

        clear_file_input();
    }

    file_input.onchange = function(e) {
        if (!saving) {
            var filename = file_input.value.split('\\').pop(),
                valid = check_file(file_input);

            if (valid == 'ok') selected_ok_file(filename);
            else selected_bad_file(filename);
        }
    };

    save_button.onclick = function(e) {
        rt.prevente(e);

        if (!saving) {
            saving = true; rt.addClass(save_button, 'wait');
            rt.hide(file_input);

            ajax.upload(file_input, function(data) {
                var valid = data['s'];

                if (valid == 'ok') {
                    saved_image.src = data['m'];
                    saved = true;
                    show_image('saved');
                    new_filename.innerHTML = '';
                } else {
                    valid = 'unknown';
                }
                saving = false;
                rt.hide(save_button); rt.removeClass(save_button, 'wait');
                clear_file_input();
                rt.show(file_input);
                show_notice(valid);
            });
        }
    };

    check_input.onchange = function() {
        if (check_input.checked) {
            show_image('no');
            hide_notices();
            clear_file_input();
            rt.hide(file_input);
        } else {
            if (saved) show_image('saved');
            else show_image('select');
            rt.show(file_input);
        }
    };

    if (rt.is_mobile) {
        check_input.parentNode.ontouchstart = function(e) {
            rt.prevente(e);
            check_input.click();
        }
    }


    var dates = [ rt.getById('details-dob'), rt.getById('details-dod'), rt.getById('details-dof') ],
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
                    if (date) {
                        date = date.split('/');
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
