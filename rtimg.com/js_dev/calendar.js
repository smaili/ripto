/*--------------------------------------------------

calendar.js
Used when showing/hiding calendar modal popup

-------------------------------------------------- */



rt.calendar = new function() {

    var


        /*
                --- Elements ---
        */

        calendar = rt.getByClass('calendar')[0],
        prev_month = rt.getByClass('prev-month', calendar)[0],
        next_month = rt.getByClass('next-month', calendar)[0],
        month_year = rt.getByClass('month-year', calendar)[0],
        year_select = rt.getByClass('year-select', calendar)[0],
        day_list = rt.getByClass('day-list', calendar)[0],
        day_name = rt.getByClass('day-name', calendar)[0],
        day_month = rt.getByClass('month', calendar)[0],
        day_num = rt.getByClass('day-num', calendar)[0],
        submit = rt.getByClass('submit', calendar)[0],



        /*
                --- Data ---
        */

        month_names = rt.getAttr(month_year, 'data-month-names').split(', '),
        month_names_short = rt.getAttr(day_month, 'data-month-names-short').split(', '),
        day_names = rt.getAttr(day_name, 'data-day-names').split(', '),
        year_range = rt.getAttr(year_select, 'data-year-range').split(', '),

        current_date = new Date(),

        me = this,

        callback = function() {},




        /*
                --- Helpers ---
        */

        get_days_in_month = function() {
            return new Date(current_date.getFullYear(), current_date.getMonth() + 1, 0).getDate();
        },

        get_current_day_num = function(date) {
            date = date || current_date;

            return date.getDate();
        },

        get_current_day_name = function(date) {
            date = date || current_date;

            return day_names[ date.getDay() ];
        },

        get_current_day_month_name = function() {
            return month_names[ current_date.getMonth() ];
        },

        get_current_day_month_name_short = function() {
            return month_names_short[ current_date.getMonth() ];
        },

        get_current_day_year = function() {
            return current_date.getFullYear();
        },

        update_day_list = function() {
            var days_in_month = get_days_in_month(),
                current_day_num = get_current_day_num();

            rt.removeChildren(day_list);
            for (var i = 1; i <= days_in_month; i++) {
                var li = document.createElement('li');
                li.className = (i == current_day_num? 'selected' : '');
                li.innerHTML = (i < 10? '0' : '') + i;
                if (!rt.is_mobile) {
                    // closure
                    (function (day) {
                        day.onmouseover = function(e) {
                            rt.prevente(e);

                            var new_selected_day = day;

                            var temp_date = new Date(current_date.getTime());
                            temp_date.setDate(+new_selected_day.innerHTML);

                            update_selected_day(temp_date);
                        };
                    })(li);
                }



                day_list.appendChild(li);
            }
        },

        update_month_year = function() {
            var children = rt.getByTag('span', month_year),
                i = 0;
            for (; i < children.length; i++) {
                children[i].innerHTML = get_current_day_month_name() + ' ' + get_current_day_year();
            }
        },

        update_day_name = function(date) {
            day_name.innerHTML = get_current_day_name(date);
        },

        update_day_month = function() {
            day_month.innerHTML = get_current_day_month_name_short();
        },

        update_day_num = function(date) {
            var new_day_num = get_current_day_num(date);
            day_num.innerHTML = (new_day_num < 10? '0' : '') + new_day_num;
        },

        update_year_select = function() {
            year_select.selectedIndex = get_current_day_year() - year_range[0]; //clever math :)
        },

        update_selected_day = function(date) {
            update_day_name(date);
            update_day_num(date);
        },

        update_selected_class = function(new_day_element) {
            new_day_element = new_day_element || rt.getByTag('li', day_list)[ get_current_day_num() - 1 ]

            var children = rt.getByClass('selected', day_list),
                i = 0;
            for (; i < children.length; i++) {
                rt.removeClass(children[i], 'selected');
            }
            rt.addClass(new_day_element, 'selected');
        },




        /*
                --- Main Functions ---
        */

        draw_calendar = function() {
            update_day_list();
            update_month_year();
            update_day_name();
            update_day_month();
            update_day_num();
            update_year_select();
        },

        date_selected = function() {
            callback(current_date);
        },

        init = function() {
            year_range[0] = +year_range[0]; year_range[1] = +year_range[1];
            for (var i = year_range[0]; i <= year_range[1]; i++) {
                var opt = rt.createEl('option');
                opt.text = opt.value = '' + i;
                year_select.options[ year_select.options.length ] = opt;
            }
            draw_calendar();
        }();



    /*
            --- Public Functions ---
    */

    me.change_date = function(new_date) {
        current_date = new_date;
        draw_calendar();
    };

    me.on_select = function(cb) {
        callback = cb;
    };



    /*
            --- Listeners ---
    */

    prev_month.onclick = function(e) {
        rt.prevente(e);

        current_date.setMonth(current_date.getMonth() - 1);
        draw_calendar();
    };

    next_month.onclick = function(e) {
        rt.prevente(e);

        current_date.setMonth(current_date.getMonth() + 1);
        draw_calendar();
    };


    year_select.onchange = function(e) {
        var new_year = year_select.options[year_select.selectedIndex].value;
        current_date.setFullYear(+new_year);

        draw_calendar();
    };


    day_list.onclick = function(e) {
        rt.prevente(e);

        var new_selected_day = rt.getTarget(e);
        current_date.setDate(+new_selected_day.innerHTML);

        update_selected_day();
        update_selected_class(new_selected_day);
    };

    submit.onclick = function(e) {
        rt.prevente(e);
        date_selected();
    };


    if (!rt.is_mobile) {
        day_list.onmouseout = function(e) {
            rt.prevente(e);
            update_selected_day();
        };
    }
};
