/*--------------------------------------------------

rt.js
Used for storing global variables and functions
sitepoint.com/jquery-vs-raw-javascript-1-dom-forms/, sitepoint.com/jquery-vs-raw-javascript-3-events-ajax/

-------------------------------------------------- */



var rt = new function() {

    /*
        --- Imports ---
    */

    var



    /*
        --- Locals ---
    */
        me = this;



    /*
        --- Public Vars ---
    */
	me.doc = document,
    me.win = window,
    me.loc = location,
    me.body = me.doc.body,
    me.is_mobile = !!('ontouchstart' in me.win) || !!('msmaxtouchpoints' in navigator),
    me.protocol = ('https:' == me.loc.protocol ? 'https://' : 'http://');



    /*
        --- Public Helpers ---
    */
    me.gete = function(e) {
        return e || me.win.event;
    };

    me.prevente = function(e) {
        e = me.gete(e);
        if (e.preventDefault) e.preventDefault();
        else e.returnValue = false;
    };

    me.getTarget = function(e) {
        // http://stackoverflow.com/questions/485453/, http://stackoverflow.com/questions/4643249/
        e = me.gete(e);
        var target = e.target || e.srcElement || e.originalTarget;
		if ( target.nodeType === 3 ) {
			target = target.parentNode;
		}
        return target;
    };

    me.createEl = function(tag) {
        return me.doc.createElement(tag);
    };

    me.removeEl = function(element) {
        element.parentNode.removeChild(element);
    };

    me.removeChildren = function(element) {
        while (element.lastChild) {
            element.removeChild(element.lastChild);
        }
    };

    me.show = function(element) {
        me.removeClass(element, 'hidden');
    };

    me.hide = function(element) {
        me.addClass(element, 'hidden');
    };

    me.isVisible = function(element) {
        return !me.hasClass(element, 'hidden');
    };

    me.getById = function(id) {
        return me.doc.getElementById(id);
    };

	me.getByClass = function(classname, element) {
        element = element || me.doc;
        if (element.getElementsByClassName) return element.getElementsByClassName(classname);
        else if (element.querySelectorAll) return element.querySelectorAll('.' + classname);
        else {
			var a = [],
				re = new RegExp('(^| )' + classname + '( |$)'),
				els = element.getElementsByTagName('*');

			for (var i = 0; i < els.length; i++) {
				if (re.test(els[i].className)) {
					a.push(els[i]);
				}
			}

			return a;
		}
	};

    me.getByTag = function(tag, element) {
        element = element || me.doc;
        return element.getElementsByTagName(tag);
    };

    me.getParent = function(element, classname, peak) {
        var p = element;
        peak = peak || me.doc;
        while ( ( p = p.parentNode ) && p != peak) {
            if (me.hasClass(p, classname)) {
                return p;
            }
        }
        return false;
    };

    me.concatNodeLists = function(list1, list2) {
        try {
            return [].slice.call(list1).concat([].slice.call(list2));
        } catch(e) {
            var arr = [];
            for (var i = 0; i < list1.length; i++) {
                arr[arr.length] = list1[i];
            }
            for (var i = 0; i < list2.length; i++) {
                arr[arr.length] = list2[i];
            }
            return arr;
        }
    };

    me.hasClass = function(element, name) {
        return new RegExp('(\\s|^)' + name + '(\\s|$)').test(element.className);
    }

	me.addClass = function(element, name) {
        if (!me.hasClass(element, name)) {
            element.className += (element.className ? ' ' : '') + name;
        }
	};

	me.removeClass = function(element, name) {
        if (me.hasClass(element, name)) {
            element.className = element.className.replace( new RegExp('(\\s|^)' + name + '(\\s|$)'), ' ').replace(/^\s+|\s+$/g, '' );
        }
	};

    me.getAttr = function(element, attr) {
        var attrs = element.attributes,
            value = false;

        for (var i = 0; i < attrs.length; i++) {
            if (attrs[i].name == attr) {
                value = attrs[i].value;
                break;
            }
        }

        return value;
    };



    /*
        --- Mobile Only ---
    */

    if (me.is_mobile) {
        var
            _page = me.getById('page-outer'),
            _class = 'scroller';

        if ( me.hasClass(_page, _class) ) {
            /* Really strange iOS bug where having nested overflow-scrolling touches causes page-outer to stop scrolling after rotation, so we need to force page-outer to redraw */
            me.win.addEventListener('orientationchange', function() {
                me.removeClass(_page, _class);
                setTimeout(function () {
                    me.addClass(_page, _class);
                }, 50);
            }, false);
        }
    }

};
