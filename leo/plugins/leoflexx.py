# -*- coding: utf-8 -*-
#@+leo-ver=5-thin
#@+node:ekr.20181103094900.1: * @file leoflexx.py
#@@first
#@@language python
#@@tabwidth -4
'''
A Stand-alone prototype for Leo using flexx.
'''
import os
from flexx import flx
import leo.core.leoBridge as leoBridge
# import leo.core.leoGlobals as g
# assert g
lean_python = False
base_class = flx.PyComponent if lean_python else flx.Widget
# Globals...
c, g, node_list, main_window = None, None, None, None
#@+others
#@+node:ekr.20181105091529.1: **  top-level functions
#@+node:ekr.20181103151350.1: *3* init
def init():
    # At present, leoflexx is not a true plugin.
    # I am executing leoflexx.py from an external script.
    return False
#@+node:ekr.20181105091545.1: *3* open_bridge
def open_bridge():
    
    global c, g, node_list
    bridge = leoBridge.controller(gui = None,
        loadPlugins = False,
        readSettings = False,
        silent = False,
        tracePlugins = False,
        verbose = True, # True: prints log messages.
    )
    if not bridge.isOpen():
        print('Error opening leoBridge')
        return
    g = bridge.globals()
    path = r'c:\Users\edreamleo\ekr.leo'
    if not os.path.exists(path):
        print('open_bridge: does not exist:', path)
        return
    c = bridge.openLeoFile(path)
    node_list = make_outline_list()
    ### runUnitTests(c, g)
#@+node:ekr.20181105095150.1: *3* make_outline_list
def make_outline_list():
    
    global c
    return [(p2.gnx, p2.h) for p2 in c.p.self_and_siblings()]

    # print(p.h)
    # if result is None:
        # result = []
    # if not p:
        # return result
    # result.append((p.gnx, p.h),)
    # if p.hasChildren():
        # aList = [make_outline_list(child, result) for child in p.children()]
        # result.append(aList)
    # return result
#@+node:ekr.20181104082144.1: ** class LeoBody
base_url = 'https://cdnjs.cloudflare.com/ajax/libs/ace/1.2.6/'
flx.assets.associate_asset(__name__, base_url + 'ace.js')
flx.assets.associate_asset(__name__, base_url + 'mode-python.js')
flx.assets.associate_asset(__name__, base_url + 'theme-solarized_dark.js')

class LeoBody(base_class):
    
    """ A CodeEditor widget based on Ace.
    """

    CSS = """
    .flx-CodeEditor > .ace {
        width: 100%;
        height: 100%;
    }
    """
    if 0:
        def init(self):
            flx.Widget(flex=1).apply_style('background: blue')
    else:
        def init(self):

            global window
            # https://ace.c9.io/#nav=api
            self.ace = window.ace.edit(self.node, "editor")
            self.ace.setValue("import os\n\ndirs = os.walk")
            self.ace.navigateFileEnd()  # otherwise all lines highlighted
            self.ace.setTheme("ace/theme/solarized_dark")
            self.ace.getSession().setMode("ace/mode/python")

        @flx.reaction('size')
        def __on_size(self, *events):
            self.ace.resize()
#@+node:ekr.20181104174357.1: ** class LeoGui
class LeoGui (object):
    
    def runMainLoop(self):
        '''The main loop for the flexx gui.'''

        # print('LeoFlex running...')
        # c = g.app.log.c
        # assert g.app.gui.guiName() == 'browser'
        # if 0: # Run all unit tests.
            # g.app.failFast = True
            # path = g.os_path_finalize_join(
                # g.app.loadDir, '..', 'test', 'unittest.leo')
            # c = g.openWithFileName(path, gui=self)
            # c.findCommands.ftm = g.NullObject()
                # # A hack. Some other class should do this.
                # # This looks like a bug.
            # c.debugCommands.runAllUnitTestsLocally()
                # # This calls sys.exit(0)
        # print('calling sys.exit(0)')
        # sys.exit(0)
        
#@+node:ekr.20181104082149.1: ** class LeoLog
class LeoLog(base_class):

    CSS = """
    .flx-CodeEditor > .ace {
        width: 100%;
        height: 100%;
    }
    """
    if 0:
        def init(self):
            flx.Widget(flex=1).apply_style('background: red') # 'overflow-y: scroll;'
    else:
        def init(self):
            global window
            # https://ace.c9.io/#nav=api
            self.ace = window.ace.edit(self.node, "editor")
            ### self.ace.setValue("import os\n\ndirs = os.walk")
            self.ace.navigateFileEnd()  # otherwise all lines highlighted
            self.ace.setTheme("ace/theme/solarized_dark")
            ### self.ace.getSession().setMode("ace/mode/python")

        @flx.reaction('size')
        def __on_size(self, *events):
            self.ace.resize()
#@+node:ekr.20181104082130.1: ** class LeoMainWindow
class LeoMainWindow(base_class):
    
    def init(self):
        global main_window
        main_window = self
        # Create dummy g.
        # global g
        # g = G()
        with flx.VBox():
            with flx.HBox(flex=1):
                self.tree = LeoTree(flex=1)
                self.log = LeoLog(flex=1)
            self.body = LeoBody(flex=1)
            self.minibuffer = LeoMiniBuffer()
            self.status_line = LeoStatusLine()
#@+node:ekr.20181104082154.1: ** class LeoMiniBuffer
class LeoMiniBuffer(base_class):
    
    def init(self): 
        with flx.HBox():
            flx.Label(text='Minibuffer')
            self.widget = flx.LineEdit(
                flex=1, placeholder_text='Enter command')
        self.widget.apply_style('background: yellow')

#@+node:ekr.20181104082201.1: ** class LeoStatusLine
class LeoStatusLine(base_class):
    
    def init(self):
        with flx.HBox():
            flx.Label(text='Status Line')
            self.widget = flx.LineEdit(flex=1, placeholder_text='Status')
        self.widget.apply_style('background: green')

#@+node:ekr.20181104082138.1: ** class LeoTree
class LeoTree(base_class):

    CSS = '''
    .flx-TreeWidget {
        background: #000;
        color: white;
        /* background: #ffffec; */
        /* Leo Yellow */
        /* color: #afa; */
    }
    '''
    def init(self):

        with flx.TreeWidget(flex=1, max_selected=1) as self.tree:
            self.make()
        if 0: # Items don't become visible right away.
            for item in self.tree.get_all_items():
                item.set_collapsed()

    #@+others
    #@+node:ekr.20181105045657.1: *3* tree.make
    def make(self):
        
        ### global node_list
        for gnx, h in node_list:
            flx.TreeItem(text=h, checked=None, collapsed=True)
        ###
            # for t in ['foo', 'bar', 'spam', 'eggs']:
                # with flx.TreeItem(text=t, checked=None, collapsed=True):
                    # for i in range(4):
                        # item2 = flx.TreeItem(
                            # text=t + ' %i' % i,
                            # checked=False,
                            # collapsed=False,
                        # )
                        # if i == 2:
                            # with item2:
                                # flx.TreeItem(title='A',
                                    # # text='A text',
                                    # collapsed=False,
                                # )
                                # flx.TreeItem(title='B',
                                    # # text='more info on B',
                                    # collapsed=False,
                                # )
    #@+node:ekr.20181104080854.3: *3* tree.on_event
    @flx.reaction(
        'tree.children**.checked',
        'tree.children**.selected',
        'tree.children**.collapsed',
    )
    def on_event(self, *events):
        for ev in events:
            # print(ev.source, ev.type)
            id_ = ev.source.title or ev.source.text
            kind = '' if ev.new_value else 'un-'
            text = '%10s: %s' % (id_, kind + ev.type)
            assert text
            ### self.label.set_html(text + '<br />' + self.label.html)
    #@-others
#@-others
if __name__ == '__main__':
    open_bridge()
        # Sets globals c, node_list.
    flx.launch(LeoMainWindow, runtime='firefox-browser')
    flx.run()
        # # Runs in browser.
        # # `python -m flexx stop 49190` stops the server.
        # flx.App(LeoWapp).launch('firefox-browser')
        # flx.start()

    ### RuntimeError: Cannot instantiate a PyComponent from JS.
    ### g.app.gui = LeoGui()
#@-leo
