/*--------------------------------------------------

ajax.js
Used for sending in-browser requests

-------------------------------------------------- */



rt.ajax = new function() {

    /*
        --- Imports ---
    */

    var



    /*
        --- Locals ---
    */
        me = this,
        upload_div = rt.createEl('div'),
        upload_form = rt.createEl('form'),
        upload_iframe = rt.createEl('iframe'),
        posting = false;



    /*
        --- Private Helpers ---
    */

    function parseJSON(data) {
        // Attempt to parse using the native JSON parser first
        if ( rt.win.JSON && rt.win.JSON.parse ) {
            return rt.win.JSON.parse(data);
        }
        else if ( typeof data === 'string' ) {
            // Make sure leading/trailing whitespace is removed (IE can't handle it)
            data = data.replace( rtrim = new RegExp( '^' + '[\\x20\\t\\r\\n\\f]' + '+|((?:^|[^\\\\])(?:\\\\.)*)' + '[\\x20\\t\\r\\n\\f]' + '+$', 'g' ), '' );
            if (data) {
                return ( new Function( 'return ' + data ) )();
            }
        }

        return false;
    }

    function ajax(method, url, data, callback, type) {
        var xhr = rt.win.ActiveXObject ? new rt.win.ActiveXObject('Microsoft.XMLHTTP') : new rt.win.XMLHttpRequest();
        if (xhr) {
            var headers = [];

            headers['X-Requested-With'] = 'XMLHttpRequest';
            headers['Accept'] = '*/*; q=0.01';

            if (data) {
                var a = [];
                for (key in data) {
                    var value = data[key] == null ? '' : data[key];
                    a[ a.length ] = encodeURIComponent( key ) + '=' + encodeURIComponent( value );
                }
                 data = a.join('&').replace( /%20/g, '+' );

                if (method == 'GET') {
                    url = url + '?' + data;
                    data = undefined;
                } else {
                    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
                }
            }

            // TODO - see if we need to add the base path or not
            xhr.open(method, url, true);
            for (i in headers) {
                xhr.setRequestHeader(i, headers[i]);
            }

            xhr.onreadystatechange = function () {
                if ( xhr.readyState == 4 ) {
                    var data = xhr.responseText;

                    if (posting) {
                        posting = false;
                    }
                    if (type != 'html') {
                        data =  parseJSON(data);
                        if ( data['s'] == 'login' ) {
                            rt.loc.href = data['m'];
                            return; // prevent callback from being run
                        }
                    }

                    callback(data , xhr.status);
                }
            };

            if (xhr.readyState != 4) {
                xhr.send(data);
            }
        }

    }


    /*
        --- Public Helpers ---
    */

    me.get = function(url, data, callback, type) {
        ajax('GET', url, data, callback, type);
    };

    me.post = function(url, data, callback, type) {
        !posting && ajax('POST', url, data, callback, type);
    };

    // TODO - add a background timeout timer that aborts and retries if takes too long? abort iframe -> stackoverflow.com/questions/5280855/
    me.upload = function(input, callback) {
        if ( !upload_div.firstChild ) {
            upload_iframe.id = upload_iframe.name = upload_form.target = 'iframe-upload';
            upload_form.id = upload_form.name = 'form-upload';
            upload_form.action = rt.loc.href + '/save_photo';
            upload_form.method = 'POST';
            upload_form.enctype = 'multipart/form-data';
            upload_div.style.cssText = 'position:absolute;top:-1200px;left:-1200px';
            upload_div.appendChild(upload_iframe); upload_div.appendChild(upload_form);
            rt.body.appendChild(upload_div);
        }

        if ( !upload_form.firstChild ) {
            var _parent = input.parentNode;
            upload_form.appendChild(input);
            upload_iframe.onload = function() {
                var data;
                try { data = parseJSON( ( upload_iframe.contentWindow || upload_iframe.contentDocument ).document.body.innerHTML ); }
                catch(err) { data = []; }
                _parent.appendChild(input);
                callback(data);
            };
            upload_form.submit();
        }
    };

};
