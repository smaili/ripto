/*--------------------------------------------------

memorial.js
Used when viewing a memorial

-------------------------------------------------- */



(function() {

    /*
        --- Imports ---
    */

    var
        ajax = rt.ajax,



    /*
        --- Locals ---
    */

        remembered = rt.getByClass('remembered')[0],
        remember_link = rt.getByClass('icon-remember', remembered)[0],
        remember_count = rt.getByClass('remember-count', remembered)[0],

        share_link_container = rt.getByClass('share-link')[0],
        share_link_input = share_link_container.firstChild, // share-link -> input

        flag_form = rt.getById('flag-form'),

        comments = rt.getByClass('comments')[0],
        reply_form = rt.getById('reply-comment-form');
        edit_form = rt.getById('edit-comment-form');



    /*
        --- Private Helpers ---
    */

    function trim(str) {
        return str.replace(/^\s+|\s+$/g,'');
    }

    function showReplyForm(reply_container, comment_id) {
        if (reply_form.parentNode != reply_container) {
            reply_container.appendChild(reply_form);
            rt.show(reply_form);
            rt.getByClass('text-input', reply_form)[0].focus();
            rt.getByTag('input', reply_form)[0].value = comment_id;
        } else {
            comments.parentNode.appendChild(reply_form);
            rt.hide(reply_form);
            rt.getByClass('text-input', reply_form)[0].blur();
        }
    }

    function showEditForm(comment_container, comment_id) {
        if (edit_form.parentNode != comment_container) {
            comment_container.insertBefore(edit_form, rt.getByClass('cbar', comment_container)[0]);
            rt.hide(rt.getByClass('ctext', comment_container)[0]); rt.hide(rt.getByClass('cmeta', comment_container)[0]);
            rt.show(edit_form);
            rt.getByClass('text-input', edit_form)[0].focus();
            rt.getByClass('text-input', edit_form)[0].value = trim(rt.getByClass('ctext', comment_container)[0].innerHTML);
            rt.getByTag('input', edit_form)[0].value = comment_id;
        } else {
            comments.parentNode.appendChild(edit_form);
            rt.show(rt.getByClass('ctext', comment_container)[0]); rt.show(rt.getByClass('cmeta', comment_container)[0]);
            rt.hide(edit_form);
            rt.getByClass('text-input', edit_form)[0].blur();
        }
    }

    function did(action, like_button, dislike_button) {
        if (action == 1) {
            if (rt.hasClass(like_button, 'did')) {
                rt.removeClass(like_button, 'did');
            } else {
                rt.addClass(like_button, 'did');
                rt.removeClass(dislike_button, 'did');
            }
        } else {
            if (rt.hasClass(dislike_button, 'did')) {
                rt.removeClass(dislike_button, 'did');
            } else {
                rt.addClass(dislike_button, 'did');
                rt.removeClass(like_button, 'did');
            }
        }
    }

    function like(url, comment_id, action, like_button, dislike_button) {
        ajax.post( url, { 'c': comment_id, 'a': action },
            function(data) {
                if (data['s'] == 'ok') {
                    rt.getByTag('span', like_button)[0].innerHTML = data['m'][0];
                    rt.getByTag('span', dislike_button)[0].innerHTML = data['m'][1];
                    did(action, like_button, dislike_button);
                }
        });
    }



    /*
            --- Listeners ---
    */

    remember_link.onclick = function(e) {
        rt.prevente(e);

        ajax.post( remember_link.href, {},
            function(data) {
                var s = data['s'];
                if (s == 'ok') {
                    remember_count.innerHTML = data['m'];
                    rt.hasClass(remembered, 'has')? rt.removeClass(remembered, 'has') : rt.addClass(remembered, 'has');
                }
        });
    };

    if (rt.is_mobile) {
        share_link_input.onfocus = function(e) {
            share_link_input.setSelectionRange(0, 9999);
        };
        share_link_container.onmouseup = function(e) {
            rt.prevente(e);
        };
    } else {
        share_link_container.onclick = share_link_container.onfocus = share_link_container.oncontextmenu = function(e) {
            rt.prevente(e);
            share_link_input.select();
            setTimeout(function() {
                share_link_input.select();
            }, 100);
        };
    }

    flag_form.onsubmit = function(e) {
        rt.prevente(e);

        var form = flag_form,
            input = form.firstChild,
            paragraph = rt.getByTag('p', form)[0],
            submit_wrap = form.lastChild;

        ajax.post( rt.getAttr(form, 'action'), { 'flag' : input.value },
            function(data) {
                paragraph.innerHTML = data['m'];
                form.removeChild(submit_wrap);
        });
    };

    comments.onclick = function(e) {
        var t = rt.getTarget(e),
            submit = rt.hasClass(t, 'submit')? t : rt.getParent(t, 'submit', comments);

        if (submit && rt.hasClass(submit.parentNode, 'cbar')) {
            var comment = rt.getParent(submit, 'comment'),
                comment_id = rt.getAttr(comment, 'data-id')
                cbar = rt.getByClass('cbar', comment)[0],
                reply = rt.getByClass('reply-container', comment)[0];

            if (rt.hasClass(submit, 'green-submit')) {
                rt.prevente(e);
                if (submit.href.indexOf('edit') > -1) {
                    showEditForm(comment, comment_id);
                } else {
                    like(submit.href, comment_id, 1, submit, rt.getByClass('submit', cbar)[1]);
                }
            } else if (rt.hasClass(submit, 'red-submit')) {
                rt.prevente(e);
                like(submit.href, comment_id, -1, rt.getByClass('submit', cbar)[0], submit);
            } else {
                showReplyForm(reply, comment_id);
            }
        }
    };

})();
