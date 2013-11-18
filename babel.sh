#! /bin/bash
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This script is part of the FFM program.
#
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this script. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    babel
#
# Purpose
#    Extract and compile translations from Python modules and Jinja templates
#
# Revision Dates
#    27-Mar-2012 (CT) Creation
#    11-May-2012 (CT) Factor `compile` to python library's babel.sh
#    ««revision-date»»···
#--

cmd=${1:?"Specify a command: extract | language | compile"}; shift

default_langs="en,de"
default_dirs="_FFM ."
lib=$(dirname $(python -c 'from _TFL import sos; print sos.path.dirname (sos.__file__)'))

export PYTHONPATH=./:$PYTHONPATH

case "$cmd" in
    "extract" )
        dirs=${1:-${default_dirs}}; shift
        ( cd ${lib}; ./babel_extract.sh extract )
        python ${lib}/_TFL/Babel.py extract                                          \
            -bugs_address        "tanzer@swing.co.at,ralf@runtux.com"         \
            -charset             utf-8                                        \
            -copyright_holder    "Mag. Christian Tanzer, Ralf Schlatterbeck"  \
            -global_config       ${lib}/_MOM/base_babel.cfg                   \
            -project             "FFM"                                        \
            -sort                                                             \
                $dirs
        ;;
    "language" )
        langs=${1:-${default_langs}}; shift
        dirs=${1:-${default_dirs}}; shift
        ( cd ${lib}; ./babel_extract.sh language "${langs}" )
        python ${lib}/_TFL/Babel.py language -languages "${langs}" -sort $dirs
        ;;
    "compile" )
        langs=${1:-${default_langs}}; shift
        ${lib}/babel.sh compile ./model.py "${langs}"
        ;;
    * )
        echo "Unknown command $cmd; use one of"
        echo "    extract"
        echo "    language"
        echo "    compile"
        ;;
esac

### __END__ babel
