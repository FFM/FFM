import _FFM

from _FFM.Graph                 import graph
from _FFM                       import *
from _TFL                       import TFL

from _MOM._Graph.Ascii          import Renderer as Ascii_Renderer
from _MOM._Graph.SVG            import Renderer as SVG_Renderer

import model

def _main (cmd) :
    scope = model.scope (cmd)
    g = graph (scope.app_type)
    if cmd.svg :
        r = SVG_Renderer (g)
        r.render ()
        with open ("doc/nodedb.svg", "wb") as f :
            r.canvas.write_to_xml_stream (f)
    else :
        r = Ascii_Renderer (g)
        print r.render ()
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler         = _main
    , defaults        = model.command.defaults
    , opts            =
        ( "verbose:B"
        , "create:B"
        , "-svg:B"
        ) + model.opts
    )

if __name__ == "__main__" :
    _Command ()
### __END__ graph
