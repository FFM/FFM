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
            ( { app_div          : "[id^=\"app-D:\"]"
              , app_div_edit     : "[id=\"app-D:edit\"]"
              , create_button    : "[href=#create]"
              , delete_button    : "[href=#delete]"
              , edit_button      : "[href=#edit]"
              , filter_button    : "[href=#filter]"
              , firmware_button  : "[href=#firmware]"
              , graph_button     : "[href=#graphs]"
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
        var pat_pid       = new RegExp ("^([^-]+)-(\\d+)$");
        var pat_typ_name  = new RegExp (options.app_typ_prefix + "(\\w+)$");
        var closest_el    = function closest_el_id (self, selector) {
            return $(self).closest (selector);
        };
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
                ( { type        : "GET"
                  , url         : url
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
            var success_cb = function success_cb (response, status) {
                var cs  = $("td", obj.row$).length;
                if (! response ["error"]) {
                    obj.row$.html
                        ( "<td class=\"feedback\" colspan=\"" + cs + "\">"
                        + (  response.html
                          || response.replacement
                          || "Deleted"
                          )
                        + "</td>"
                        );
                } else {
                    $GTW.show_message ("Ajax Error: " + response ["error"]);
                };
            };
            $.gtw_ajax_2json
                ( { type        : "DELETE"
                  , url         : obj.url
                  , success     : success_cb
                  }
                , "Delete"
                );
            return false;
        };
        var edit_cb   = function edit_cb (ev) {
            var obj         = obj_of_row (this);
            var referrer_id = closest_el_id (this, selectors.app_div);
            var url         = obj.url;
            setTimeout
                ( function () {
                    window.location.href = url;
                  }
                , 0
                );
            return false;
            var success_cb  = function success_cb (response, status) {
                if (! response ["error"]) {
                    var target_id =
                        response ["target_id"] || selectors.app_div_edit;
                    var target$   = $(target_id);
                    var form$     = $(response ["form"]);
                    form$.data ("ffd_referrer", referrer_id);
                    target$.prepend (form$);
                    $(selectors.app_div).hide ();
                    target$.show ();
                } else {
                    $GTW.show_message
                        ("Ajax Error: " + response ["error"]);
                };
            };
            $.gtw_ajax_2json
                ( { type        : "GET"
                  , url         : url
                  , success     : success_cb
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
        var firmware_cb = function firmware_cb (ev) {
            var a$    = $(this);
            var row$  = closest_el (this, selectors.obj_row);
            var name  = $(".name", row$).text ();
            var msgs$ = $("#messages");
            var mid   = new Date().valueOf().toString();
            var msg$  =
                $( "<a class=\"feedback\" id=\""
                + mid + "\" href=\"#" + mid+ "\">"
                + "The firmware for " + name
                + " will be built and an email with the download URL "
                + "sent to you."
                + "<i>✕</i></a>"
                );
            msgs$.append (msg$);
            msg$.focus ();
            msg$.on    ("click", hide_feedback);
        };
        var graph_cb = function graph_cb (ev) {
            var a$    = $(this);
            var row$  = closest_el     (this, selectors.obj_row);
            var rid   = row$.prop      ("id");
            var typ   = type_of_obj_id (rid);
            var pref  =
                "https://marvin.funkfeuer.at/cgi-bin/smokeping/freenet.cgi?target=";
            var name  = $(".name", row$).text ();
            var node, url;
            if (typ == "node") {
                url   = pref + name;
            } else if (typ == "interface") {
                node  = $(".Node", row$).text ();
                url   = pref + node + "." + name;
            } else {
                alert ("Graph type " + typ + " is not implemented");
            };
            if (url) {
                window.open (url).focus ();
            };
        };
        var hide_feedback = function hide_feedback (ev) {
            var target$ = $(ev.target);
            target$.remove ();
            return false;
        };
        var obj_of_row  = function obj_of_row (self) {
            var result  = {};
            var row$    = closest_el       (self, selectors.obj_row)
            result.row$ = row$;
            result.rid  = row$.prop        ("id");
            result.pid  = pid_of_obj_id    (result.rid);
            result.sid  = closest_el_id    (self, "section");
            result.typ  = result.sid.match (pat_typ_name) [1];
            result.url  = options.urls.page + result.typ + "/" + result.pid;
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
        $(selectors.create_button  ).on ("click", create_cb);
        $(selectors.delete_button  ).on ("click", delete_cb);
        $(selectors.edit_button    ).on ("click", edit_cb);
        $(selectors.filter_button  ).on ("click", filter_cb);
        $(selectors.firmware_button).on ("click", firmware_cb);
        $(selectors.graph_button   ).on ("click", graph_cb);
        return this;
    };
  } (jQuery)
);

// __END__ html/dashboard/app.js
