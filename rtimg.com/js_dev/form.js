/*--------------------------------------------------

form.js
Used for handling forms

-------------------------------------------------- */



rt.form = new function() {

    /*
        --- Imports ---
    */

    var



    /*
        --- Locals ---
    */
        me = this,
        labels = rt.getByTag('label'),
        can_check = true,
        timer;



    /*
        --- Private Helpers ---
    */

    function startChecking(fieldName, input, side, keep_checking) {
        clearTimeout(timer);

        var current_value = input.value;

        if (input.prev_value != current_value) {
            me.checkField(fieldName, input, side);
        }

        if (input.has_focus) {
            timer = setTimeout(function() {
                startChecking(fieldName, input, side);
            }, 1000);
        }

        input.prev_value = current_value;
    }

    function show_placeholder(label) {
        rt.removeClass(label, 'hasome');
    }

    function hide_placeholder(label) {
        rt.addClass(label, 'hasome');
    }

    function check_placeholder(label, input) {
        if (input.value.length) {
            hide_placeholder(label);
        } else {
            show_placeholder(label);
        }
    }

    function check_placeholders() {
        for (var i = 0; i < labels.length; i++) {
            if (labels[i].className == 'placeholder') {
                var label = labels[i],
                    input = rt.getById(label.htmlFor);

                check_placeholder(label, input);
            }
        }
    }



    /*
        --- Public Helpers ---
    */

    me.lookups = {}; // used for looking up function names since closure obfuscates

    me.check_global = function() {};

    me.checkField = function(fieldName, input, side) {
        var check_function = me.lookups['check_' + fieldName];
        if (check_function && typeof check_function == 'function') {
            var result = check_function(input);
            if (result) {
                me.showSideTip(side, result);
                check_placeholders();
            }
        }
        me.check_global();
    };

    me.hideSideTip = function(side) {
        var children = side.children,
            i = 0;
        for (; i < children.length; i++) {
            rt.hide(children[i]);
        }
    };

    me.showSideTip = function(side, name) {
        me.hideSideTip(side);
        rt.show( ( rt.getByClass(name, side)[0] || rt.getByClass('tip', side)[0] ) ); // default to tip if the specific side isn't in the dom
    };

    me.listen = function() {
        // TODO - maybe we should have a js class instead of assuming all holding should have listeners?

        var fields = rt.concatNodeLists( rt.getByClass('placeholding-input'), rt.getByClass('holding') ),
            i = 0;

        for (; i < fields.length; i++) {
            var field = fields[i],
                fieldName = rt.getAttr(field, 'data-field'),
                input = rt.concatNodeLists( rt.getByTag('input', field), rt.getByTag('textarea', field) )[0],
                side = rt.getByClass('sidetip', field)[0];

            // closure
            (function (n, i, s) {
                i.prev_value = i.value;

                i.onfocus = function(e) {
                    i.has_focus = true;
                    startChecking(n, i, s);
                };

                i.onblur = function(e) {
                    i.has_focus = false;
                    startChecking(n, i, s);
                };
            })(fieldName, input, side);
        }

    };



    /*
        --- Listeners ---
    */

    // TODO - make the checking smarter (right clicking, ctrl+v, etc...) --> http://stackoverflow.com/questions/6458840/on-input-change-event
    // handlers for giving input focus on label click/touch and showing/hiding label
    for (var i = 0; i < labels.length; i++) {
        if ( rt.hasClass(labels[i], 'placeholder') ) {
            var label = labels[i],
                input = rt.getById(label.htmlFor);

            // closure
            (function (myLabel, myInput) {
                if (rt.is_mobile) {
                    myLabel.onclick = function() {}; // fixes iOS bug with tapping labels
                }
                myInput.onkeydown = function(e) {
                    hide_placeholder(myLabel);
                }
                myInput.onblur = function(e) {
                    check_placeholder(myLabel, myInput);
                }
            })(label, input);
        }
    }



    /*
        --- Initialization ---
    */

};
