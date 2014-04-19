// Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
// Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
// #*** <License> ************************************************************#
// This module is licensed under the terms of either the
// MIT License or the GNU Affero General Public License (AGPL) Version 3.
// http://www.c-tanzer.at/license/mit_or_agpl.html
// #*** </License> ***********************************************************#
//
//++
// Name
//    html/dashboard/app.js
//
// Purpose
//    Javascript code for Funkfeuer dashboard
//
// Revision Dates
//    15-Apr-2014 (CT) Creation
//    ««revision-date»»···
//--

;( function ($) {
    "use strict";
    $.fn.ff_dashboard = function ff_dashboard (opts) {
        var selectors = $.extend
            ( { create_button    : "[href=#create]"
              , delete_button    : "[href=#delete]"
              , edit_button      : "[href=#edit]"
              , filter_button    : "[href=#filter]"
              , obj_row          : "tr"
              , root             : "#app"
              }
            , opts && opts ["selectors"] || {}
            );
        var page_url  =
            (opts ["urls"] && opts ["urls"] ["page"]) || "/dashboard/";
        var urls      = $.extend
            ( { page             : page_url
              , pid              : page_url + "pid/"
              }
            , opts && opts ["urls"] || {}
            );
        var options   = $.extend
            ( { active_button_class   : "pure-button-active"
              , app_div_prefix        : "app-D:"
              , app_typ_prefix        : "app-T:"
              }
            , opts || {}
            , { selectors : selectors
              , urls      : urls
              }
            );
        var pat_div_name  = new RegExp (options.app_div_prefix + "(\\w+)$");
        var pat_pid       = new RegExp ("^([^-]+-)(\\d+)$");
        var pat_typ_name  = new RegExp (options.app_typ_prefix + "(\\w+)$");
        var closest_el_id = function closest_el_id (self, selector) {
            return $(self).closest (selector).prop ("id");
        };
        var create_cb = function create_cb (ev) {
            var sid   = closest_el_id (this, "section");
            var typ   = sid.match     (pat_typ_name) [1];
            var url   = options.urls.page + typ + "?create";
            setTimeout
                ( function () {
                    window.location.href = url;
                  }
                , 0
                );
            return false;
            $.gtw_ajax_2json
                ( { url         : url
                  , type        : "GET"
                  , success     : function (response, status) {
                        if (! response ["error"]) {
                            // XXX TBD
                            // hide "#overview"
                            // fill and display "#edit" with response.html...
                            $GTW.show_message (response);
                        } else {
                            $GTW.show_message
                                ("Ajax Error: " + response ["error"]);
                        };
                    }
                  }
                , "Create"
                );
            return false;
        };
        var delete_cb = function delete_cb (ev) {
            var obj   = obj_of_row (this);
            $.gtw_ajax_2json
                ( { url         : obj.url
                  , type        : "DELETE"
                  , success     : function (response, status) {
                        if (! response ["error"]) {
                            tr$.html (response.html || "<td>Deleted</td>");
                        } else {
                            $GTW.show_message
                                ("Ajax Error: " + response ["error"]);
                        };
                    }
                  }
                , "Delete"
                );
            return false;
        };
        var edit_cb   = function edit_cb (ev) {
            var obj   = obj_of_row (this);
            $.gtw_ajax_2json
                ( { url         : obj.url
                  , type        : "GET"
                  , success     : function (response, status) {
                        if (! response ["error"]) {
                            // XXX TBD
                            // hide "#overview"
                            // fill and display "#edit" with response.html...
                            $GTW.show_message (response);
                        } else {
                            $GTW.show_message
                                ("Ajax Error: " + response ["error"]);
                        };
                    }
                  }
                , "Edit"
                );
            return false;
        };
        var do_filter = function do_filter (ev) {
            var id    = closest_el_id (this, selectors.obj_row);
            var all   = obj_rows_selector_all (id);
            var sel   = obj_rows_selector_sel (id);
            $(all).hide ();
            $(sel).show ();
        };
        var filter_cb = function filter_cb (ev) {
            var a$    = $(this);
            var id    = closest_el_id (this, selectors.obj_row);
            var all   = obj_rows_selector_all (id);
            var hide$;
            if (a$.hasClass (options.active_button_class)) {
                // currently filtered --> show all instances
                $(all).show ();
            };
            a$.toggleClass (options.active_button_class);
            // execute all filters that are active now
            hide$ = $(selectors.filter_active_button);
            hide$.each (do_filter);
            return false;
        };
        var obj_of_row = function obj_of_row (self) {
            var result = {};
            result.rid = closest_el_id    (self, selectors.obj_row);
            result.pid = pid_of_obj_id    (result.rid);
            result.sid = closest_el_id    (self, "section");
            result.typ = result.sid.match (pat_typ_name) [1];
            result.url = options.urls.page + result.typ + "/" + result.pid;
            return result;
        };
        var obj_rows_selector_all = function obj_rows_selector_all (id) {
            var typ = type_of_obj_id (id);
            return selectors.obj_row + "[class*=\"" + typ + "\"]";
        };
        var obj_rows_selector_sel = function obj_rows_selector_sel (id) {
            return selectors.obj_row + "[class~=\"" + id + "-\"]";
        };
        var pid_of_obj_id = function pid_of_obj_id (id) {
            var groups = id.match (pat_pid);
            return groups [2];
        };
        var type_of_obj_id = function type_of_obj_id (id) {
            var groups = id.match (pat_pid);
            return groups [1];
        };
        selectors.filter_active_button =
            "." + options.active_button_class + selectors.filter_button;
        $(selectors.create_button).on ("click", create_cb);
        $(selectors.delete_button).on ("click", delete_cb);
        $(selectors.edit_button  ).on ("click", edit_cb);
        $(selectors.filter_button).on ("click", filter_cb);
        return this;
    };
  } (jQuery)
);

// __END__ html/dashboard/app.js
