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
#    ««revision-date»»···
#--

cmd=${1:?"Specify a command: extract | language"}; shift
lang=${1:-"de"}; shift
dirs=${1:-"_FFM ."}; shift
lib=$(dirname $(python -c 'from _TFL import sos; print sos.path.dirname (sos.__file__)'))

export PYTHONPATH=./:$PYTHONPATH

case "$cmd" in
    "extract" )
        ( cd ${lib}; ./babel_extract.sh extract "${lang}" )
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
        ( cd ${lib}; ./babel_extract.sh language "${lang}" )
        python ${lib}/_TFL/Babel.py language -languages "$lang" -sort $dirs
        ;;
    "compile" )
        for lang in en de
        do
            mkdir -p ./locale/${lang}/LC_MESSAGES
            /usr/bin/python ${lib}/_TFL/Babel.py compile \
               -use_fuzzy \
               -languages ${lang} -combine -import_file ./model.py \
               -output_file ./locale/${lang}/LC_MESSAGES/messages.mo
        done
        ;;
    * )
        echo "Unknown command $cmd; use one of"
        echo "    extract"
        echo "    language"
        echo "    compile"
        ;;
esac

### __END__ babel
