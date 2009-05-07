#@+leo-ver=4-thin
#@+node:ville.20090503124249.1:@thin tomboy_import.py
#@<< docstring >>
#@+node:ville.20090503124249.2:<< docstring >>
'''This plugin adds a possibility to import the notes created in Tomboy / gnote

Usage:

  * Create a node with the headline 'tomboy'
  * Select the node, and do alt+x act-on-node    
  * The notes will appear as children of 'tomboy' node
  * The next time you do act-on-node, existing notes will be updated (they don't need to 
    be under 'tomboy' node anymore) and new notes added.

'''
#@-node:ville.20090503124249.2:<< docstring >>
#@nl

__version__ = '0.1'
#@<< version history >>
#@+node:ville.20090503124249.3:<< version history >>
#@@killcolor
#@+at
# 
# 0.1 Ville M. Vainio:
# 
#     * Functional version, has unidirectional (import) support with
#       updates. Strips html.
# 
#@-at
#@-node:ville.20090503124249.3:<< version history >>
#@nl

#@<< imports >>
#@+node:ville.20090503124249.4:<< imports >>
import leo.core.leoGlobals as g

import xml.etree.ElementTree as ET
from leo.core import leoPlugins
import HTMLParser

# Whatever other imports your plugins uses.
#@nonl
#@-node:ville.20090503124249.4:<< imports >>
#@nl

#@+others
#@+node:ville.20090503124249.5:init
def init ():

    ok = True

    if ok:

        leoPlugins.registerHandler('after-create-leo-frame',onCreate)
        g.plugin_signon(__name__)

    return ok
#@-node:ville.20090503124249.5:init
#@+node:ville.20090503124249.6:onCreate
def onCreate (tag, keys):

    c = keys.get('c')
    if not c: return

    # c not needed

    tomboy_install()

#@-node:ville.20090503124249.6:onCreate
#@+node:ville.20090503124249.7:the code
class MLStripper(HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_fed_data(self):
        return ''.join(self.fed)

def strip_tags(cont):
    x = MLStripper()
    x.feed(cont)
    return x.get_fed_data()


def parsenote(cont):
    tree = ET.parse(cont)
    #ET.dump(tree)
    title = tree.findtext('{http://beatniksoftware.com/tomboy}title')
    body  = tree.getiterator('{http://beatniksoftware.com/tomboy}note-content')[0]
    #b = "".join(el.text for el in body.getiterator())
    b = ET.tostring(body)
    b = strip_tags(b)
    #print "body",b
    return title, b

def pos_for_gnx(c,gnx):
    #print "match",gnx
    for pos in c.allNodes_iter():
        pos = pos.copy()
        #print pos.gnx, pos.h
        if pos.gnx == gnx:
            return pos.copy()
    return None

def capturenotes(c,pos):
    import glob, os
    notes = glob.glob(os.path.expanduser('~/.tomboy/*.note'))

    # map tomboy file name => gnx
    old_nodes = c.db.get('tomboy_notes', {})

    for no in notes:
        fname = os.path.basename(no)
        title, body = parsenote(open(no))

        po = None
        if fname in old_nodes:

            po = pos_for_gnx(c,old_nodes[fname])
            if po is not None:
                g.es('tomboy: Updating note "%s"' % title)

        if po is None:
            g.es('tomboy: Creating note "%s"' % title)
            po = pos.insertAsLastChild()

        po.h = title
        po.b = body        
        old_nodes[fname] = po.gnx
    c.db['tomboy_notes'] = old_nodes

def tomboy_act_on_node(c,p,event):
    #print 'act', `p.h`
    if not p.h == 'tomboy':
        raise leoPlugins.TryNext

    capturenotes(c,p)
    c.redraw_now()

def tomboy_install():
    g.act_on_node.add(tomboy_act_on_node, 99)

#print "capturing"
#capturenotes(p)
#tomboy_install()
#@-node:ville.20090503124249.7:the code
#@-others
#@nonl
#@-node:ville.20090503124249.1:@thin tomboy_import.py
#@-leo
