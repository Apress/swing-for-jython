#-------------------------------------------------------------------------------
#    Name: WSAShelp_05.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: wsadmin Jython script to display wsadmin scripting object help text
#          with splitpanes to separate the general object description from the
#          method details.  This iteration adds code to highlight the user
#          specified text.
#    Note: This requires a WebSphere Application Server environment.
#   Usage: wsadmin -f WSAShelp_05.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 12/12/13  rag  0.05  Add - user specified text highlighting
# 12/12/12  rag  0.04  Add - tabbed pane event listener method tabPicked()
# 12/12/11  rag  0.03  Add - Separate the scripting object help from method help
# 12/12/10  rag  0.02  New - Add a tabbed pane
# 12/12/10  rag  0.01  New - Initial application
#-------------------------------------------------------------------------------

import java
import re
import sys

from   java.awt    import BorderLayout
from   java.awt    import Color
from   java.awt    import Dimension
from   java.awt    import EventQueue
from   java.awt    import Font
from   java.awt    import Toolkit

from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JPanel
from   javax.swing import JScrollPane
from   javax.swing import JSplitPane
from   javax.swing import JTabbedPane
from   javax.swing import JTextField
from   javax.swing import JTextPane

from   javax.swing.text import DefaultHighlighter

#-------------------------------------------------------------------------------
# Name: WSAShelp_05()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class WSAShelp_05( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Class constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        #-----------------------------------------------------------------------
        # Painter instance used to highlight text
        #-----------------------------------------------------------------------
        self.painter = DefaultHighlighter.DefaultHighlightPainter(
           Color.YELLOW
        )

    #---------------------------------------------------------------------------
    # Name: center()
    # Role: Position the frame in the center of the screen
    # Note: The frame isn't allowed to be wider than 1/2 the screen width, or
    #       more than 1/2 the screen height.  It is resized, if necessary.
    #---------------------------------------------------------------------------
    def center( self, frame ) :
        screenSize = Toolkit.getDefaultToolkit().getScreenSize()
        frameSize  = frame.getSize()
        frameSize.width  = min( frameSize.width , screenSize.width  >> 1 )
        frameSize.height = min( frameSize.height, screenSize.height >> 1 )
        if frameSize != frame.getSize() :
            frame.setSize( frameSize )
        frame.setLocation(
            ( screenSize.width  - frameSize.width  ) >> 1,
            ( screenSize.height - frameSize.height ) >> 1
        )

    #---------------------------------------------------------------------------
    # Name: hilight()
    # Role: Find, and highlight every occurrance of text on specified JTextPane
    #---------------------------------------------------------------------------
    def hilight( self, tPane, text ) :
        hiliter = tPane.getHighlighter()
        hiliter.removeAllHighlights()
        if text :
            doc   = tPane.getDocument()
            info  = doc.getText( 0, doc.getLength() )
            start = 0
            here  = info.find( text, start )
            while here > -1 :
                hiliter.addHighlight(
                    here,
                    here + len( text ),
                    self.painter
                )
                start = here + len( text )
                here  = info.find( text, start )

    #---------------------------------------------------------------------------
    # Name: lookFor()
    # Role: ActionListener event handler called when user press <Enter>
    #---------------------------------------------------------------------------
    def lookFor( self, event ) :
        text  = event.getSource().getText()
        index = self.tabs.getSelectedIndex()
        name  = self.tabs.getTitleAt( index )
        for tPane in self.tPanes[ name ] :
            self.hilight( tPane, text )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'WSAShelp_05',
            layout = BorderLayout(),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        #-----------------------------------------------------------------------
        # RegExp used to locate the method name portion of the help text
        #-----------------------------------------------------------------------
        methRE = re.compile( r'^(\w+)(?:\s+.*)$', re.MULTILINE )
        monoFont = Font( 'Courier' , Font.PLAIN, 12 )

        #-----------------------------------------------------------------------
        # Create & Populate the JTabbedPane
        #-----------------------------------------------------------------------
        objs = [
            ( 'wsadmin'     , None         ),    # Special case
            ( 'Help'        , Help         ),
            ( 'AdminApp'    , AdminApp     ),
            ( 'AdminConfig' , AdminConfig  ),
            ( 'AdminControl', AdminControl ),
            ( 'AdminTask'   , AdminTask    )
        ]
        self.tPanes = {}
        highlighters = {}
        self.tabs = tabs = JTabbedPane(
            stateChanged = self.tabPicked
        )
        for name, obj in objs :
            #-------------------------------------------------------------------
            # Use a single ScrollPane for the AdminTask help
            #-------------------------------------------------------------------
            if name in [ 'wsadmin', 'AdminTask' ] :
                if obj :
                    data = obj.help().expandtabs()
                else :
                    data = Help.wsadmin().expandtabs()
                pane = JTextPane(
                    text = data,
                    editable = 0,
                    font = monoFont
                )
                pane.moveCaretPosition( 0 )
                tabs.addTab( name, JScrollPane( pane ) )
                self.tPanes[ name ] = [ pane ]
#               print 'tPanes[ "%s" ]' % name
            else :
                #---------------------------------------------------------------
                # Use a RegExp to identify where the 1st method starts.
                #---------------------------------------------------------------
                text = obj.help().expandtabs()
                mo   = re.search( methRE, text ) # Match Object
                desc = text[ :mo.start( 1 ) ].strip()
                meth = text[ mo.start( 1 ): ].strip()
                #---------------------------------------------------------------
                # The description section is before the 1st method
                #---------------------------------------------------------------
                topPane = JTextPane(
                    text = desc,
                    editable = 0,
                    font = monoFont
                )
                topPane.moveCaretPosition( 0 )
                top = JScrollPane( topPane )
                #---------------------------------------------------------------
                # The method section starts at the 1st method
                #---------------------------------------------------------------
                botPane = JTextPane(
                    text = meth,
                    editable = 0,
                    font = monoFont
                )
                botPane.moveCaretPosition( 0 )
                bot = JScrollPane( botPane )
                #---------------------------------------------------------------
                # For the other scripting objects, use a vertically split pane
                # with the top containing the description section, and the
                # bottom containing the method details.
                #---------------------------------------------------------------
                tabs.addTab(
                    name,
                    JSplitPane(
                        JSplitPane.VERTICAL_SPLIT,
                        top,
                        bot,
                        resizeWeight = 0.5, # divider position = 50%
                        oneTouchExpandable = 1
                    )
                )
                self.tPanes[ name ] = [ topPane, botPane ]
#               print 'tPanes[ "%s" ]' % name

        #-----------------------------------------------------------------------
        # Add the tabbed pane to the frame & show the result
        #-----------------------------------------------------------------------
        frame.add( tabs, 'Center' )

        #-----------------------------------------------------------------------
        # Label & input field for user input
        #-----------------------------------------------------------------------
        info = JPanel( BorderLayout() )
        info.add( JLabel( 'Highlight text:' ), 'West' )
        self.textField = JTextField(
            actionPerformed = self.lookFor
        )
        info.add( self.textField, 'Center' )
        frame.add( info, 'South' )

        frame.pack()
        self.center( frame )
        frame.setVisible( 1 )
        self.textField.requestFocusInWindow()

    #---------------------------------------------------------------------------
    # Name: tabPicked()
    # Role: ChangeListener event handler - called when a tab is selected
    #---------------------------------------------------------------------------
    def tabPicked( self, event ) :
        pane  = event.getSource()
        index = pane.getSelectedIndex()
        name  = pane.getTitleAt( index )
        try :
            for tPane in self.tPanes[ name ] :
                self.hilight( tPane, self.textField.getText() )
        except :
            pass

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( WSAShelp_05() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f WSAShelp_05.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
