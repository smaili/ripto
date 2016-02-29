/*--------------------------------------------------

form.js
Used for handling forms

-------------------------------------------------- */



rt.modal = new function() {

    /*
        --- Imports ---
    */

    var
        ajax = rt.ajax,
        notice = rt.notice,



    /*
        --- Locals ---
    */
        me = this,
        modal_overlay = rt.getByClass('modal-overlay')[0],
        modal_clicks = rt.getByClass('js-modal-click'),
        modal_forms = rt.getByClass('js-modal-form'),
        modals = rt.getByClass('modal'),
        upload_iframe = rt.createEl('iframe');


    /*
        --- Public Helpers ---
    */

    me.show = function(id) {
        rt.show(modal_overlay);
        rt.show(rt.getById(id));
    };

    me.hide = function(el) {
        rt.hide(modal_overlay);
        rt.hide(el);
    };

    me.getMenuLinks = function(menu) {
        return rt.getByTag( 'a', menu );
    };

    me.selectMenuLink = function(link) {
        rt.addClass( link, 'selected' );
    };

    me.hideMenuLinks = function(menu) {
        var links = me.getMenuLinks(menu),
            i = 0;
        for (; i < links.length; i++) {
            rt.removeClass( links[i], 'selected' );
        }
    };

    me.selectContainer = function(container) {
        rt.show(container);
    };

    me.hideContainers = function(content) {
        var containers = content.children,
            i = 0;
        for (; i < containers.length; i++) {
            rt.hide(containers[i]);
        }
    };

    me.changeMenuLink = function(id, text) {
        var menu = rt.getByClass( 'canvas-menu', rt.getById(id) )[0],
            items = me.getMenuLinks(menu),
            i = 0;
        for (; i < items.length; i++) {
            if ( rt.hasClass(items[i], 'selected' ) ) items[i].innerHTML = text;
        }
    };



    /*
            --- Listeners ---
    */

    for (var i = 0; i < modal_clicks.length; i++) {
        // closure
        (function (modal_click) {
            modal_click.onclick = function(e) {
                rt.prevente(e);

                var id = rt.getAttr(modal_click, 'data-modal-for'),
                    flag = rt.getAttr(modal_click, 'data-flag-for');

                if (flag) {
                    var flag_form = rt.getById('flag-form');
                    rt.getByTag('input', flag_form)[0].value = flag;
                }

                me.show(id);
            };
        })(modal_clicks[i]);
    }

    // i.e., jQuery('.modal-container .body-header a')
    var menu_links = [];
    for (var i = 0; i < modals.length; i++) {
        var canvas_menu = rt.getByClass('canvas-menu', modals[i])[0],
            links = me.getMenuLinks(canvas_menu);
        for (var j = 0; j < links.length; j++)
            menu_links[menu_links.length] = links[j];
    }

    for (var i = 0; i < menu_links.length; i++) {
        // closure
        (function (link) {
            link.onclick = function(e) {
                rt.prevente(e);

                if (!rt.hasClass(link, 'selected')) {
                    var next = rt.getAttr(link, 'data-menu-for')
                        body = rt.getParent(link, 'modal-content'),
                        menu = rt.getByClass('canvas-menu', body)[0],
                        content = rt.getByClass('canvas-content', body)[0];

                    // header stuff
                    me.hideMenuLinks(menu);
                    me.selectMenuLink(link);
                    // content stuff
                    me.hideContainers(content);
                    me.selectContainer( rt.getByClass(next, content)[0] );
                }
            };
        })(menu_links[i]);
    }


    for (var i = 0; i < modals.length; i++) {
        var modal = modals[i],
            close = rt.getByClass('close-modal', modal)[0];

        // closure
        (function (c, m) {
            c.onclick = function(e) {
                rt.prevente(e);
                me.hide(m);
            };
        })(close, modal);
    }

    modal_overlay.onclick = function(e) {
        rt.prevente(e);

        for (var i = 0; i < modals.length; i++) {
            me.hide( modals[i] );
        }
    };



    /* TODO - move to form.js and change class to js-form-submit */
    for (var i = 0; i < modal_forms.length; i++) {
         // closure
        (function (form) {
            form.onsubmit = function(e) {
                rt.prevente(e);

                var inputs = rt.concatNodeLists( rt.getByTag('input', form), rt.getByTag('textarea', form) ),
                    notices = rt.getByClass('notice-box', form),
                    submit = rt.getByClass('submit', form)[0],
                    data = {};

                for (var i = 0; i < notices.length; i++) {
                    notice.hide( notices[i] );
                }

                // generate data params
                for (var i = 0; i < inputs.length; i++) {
                    var name = rt.getAttr(inputs[i], 'name');
                    data[name] = inputs[i].value;
                }
                // show 'loading'
                rt.addClass(submit, 'wait');

                ajax.post( rt.getAttr(form, 'action'), data,
                    function(data) {
                        for (var i = 0; i < notices.length; i++) {
                            if (rt.hasClass( notices[i], data['s'] )) {
                                notice.change( notices[i], data['m'] );
                                notice.show( notices[i] );
                            }
                            else notice.hide( notices[i] );
                        }
                        rt.removeClass(submit, 'wait');
                });

            };
        })(modal_forms[i]);
    }

};
