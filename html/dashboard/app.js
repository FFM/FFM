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
              , instance_row     : "tr"
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
              , instance_id_pattern   : /^([^-]+-)(\d+)$/
              }
            , opts || {}
            , { selectors : selectors
              , urls      : urls
              }
            );
        var create_cb = function create_cb (ev) {
            var tab$  = $(this).closest ("section");
            var id    = tab$.prop ("id");
            var typ   = id.match  (/-(\w+)$/) [1];
            $.gtw_ajax_2json
                ( { url         : options.urls.page + typ + "?create"
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
        } ;
        var delete_cb = function delete_cb (ev) {
            var tr$   = $(this).closest (selectors.instance_row);
            var id    = tr$.prop  ("id");
            var pid   = pid_of_id (id);
            $.gtw_ajax_2json
                ( { url         : options.urls.pid + pid
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
            var tr$   = $(this).closest (selectors.instance_row);
            var id    = tr$.prop  ("id");
            var pid   = pid_of_id (id);
            $.gtw_ajax_2json
                ( { url         : options.urls.pid + pid
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
            var id    = instance_row_id (this);
            var all   = instance_rows_selector_all (id);
            var sel   = instance_rows_selector_sel (id);
            $(all).hide ();
            $(sel).show ();
        };
        var filter_cb = function filter_cb (ev) {
            var a$    = $(this);
            var id    = instance_row_id (this);
            var all   = instance_rows_selector_all (id);
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
        var instance_row_id = function instance_row_id (self) {
            return $(self).closest (selectors.instance_row).prop ("id");
        };
        var instance_rows_selector_all = function instance_rows_selector_all
                (id) {
            var typ = type_of_id (id);
            return selectors.instance_row + "[class*=\"" + typ + "\"]";
        };
        var instance_rows_selector_sel = function instance_rows_selector_sel
                (id) {
            return selectors.instance_row + "[class~=\"" + id + "-\"]";
        };
        var pid_of_id = function pid_of_id (id) {
            var groups = id.match (options.instance_id_pattern);
            return groups [2];
        };
        var type_of_id = function type_of_id (id) {
            var groups = id.match (options.instance_id_pattern);
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
