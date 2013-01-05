import os
from   rsclib.HTML_Parse  import tag, Page_Tree
from   rsclib.stateparser import Parser

class Guess (Page_Tree) :
    site  = 'http://%(ip)s/'
    url   = ''
    delay = 0

    status_url = 'cgi-bin-status.html'

    def parse (self) :
        #print self.tree_as_string ()
        root = self.tree.getroot ()
        for sm in root.findall (".//%s" % tag ("small")) :
            if sm.text.startswith ('v1') :
                self.version = sm.text
                break
        else :
            self.version = "Unknown"
        print "Version: %s" % self.version
        for a in root.findall (".//%s" % tag ("a")) :
            if a.get ('class') == 'plugin' and a.text == 'Status' :
                self.status_url = a.get ('href')
        url = self.url [len (self.site) + 1:]
        url = os.path.join (os.path.dirname (url), self.status_url)
        self.status = Freifunk (site = self.site, url = url)
    # end def parse

# end class Guess

class Freifunk (Page_Tree) :
    url = 'cgi-bin-status.html'

    def parse (self) :
        #print self.tree_as_string ()
        root = self.tree.getroot ()
        for pre in root.findall (".//%s" % tag ("pre")) :
            if pre.get ('id') == 'ifconfig' :
                self.ifconfig = pre.text
                break
        else :
            raise ValueError, "No interface config found"
        print self.ifconfig
    # end def parse

# end class Freifunk

if __name__ == '__main__' :
    import sys
    # For testing we download the index page and cgi-bin-status.html
    # page into a directory named with the ip address
    ip   = '193.238.158.241'
    if len (sys.argv) > 1 :
        ip = sys.argv [1]
    site = Guess.site % locals ()
    site = 'file://'
    url  = os.path.join (os.path.abspath (ip), 'index.html')
    ff   = Guess (site = site, url = url)
