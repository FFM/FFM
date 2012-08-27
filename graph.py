import _FFM

from _FFM.Graph                 import graph
from _FFM                       import *
from _TFL                       import TFL

from _MOM._Graph.Ascii          import Renderer

import model

def _main (cmd) :
    scope = model.scope (cmd)
    g = graph (scope.app_type)
    r = Renderer (g)
    print r.render ()
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler         = _main
    , defaults        = model.command.defaults
    , opts            =
        ( "verbose:B"
        , "create:B"
        ) + model.opts
    )

if __name__ == "__main__" :
    _Command ()
