#-------------------------------------------------------------------------------
#    Name: Highlight.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple wsadmin Jython Swing script demonstrating text highlighting
#    Note: This requires a WebSphere Application Server environment.
#   Usage: wsadmin -f Highlight.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/11/03  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import Color
from   java.awt    import BorderLayout
from   java.awt    import EventQueue
from   java.awt    import Font
from   java.awt    import Toolkit

from   javax.swing import JLabel
from   javax.swing import JFrame
from   javax.swing import JPanel
from   javax.swing import JTextField
from   javax.swing import JTextPane
from   javax.swing import JScrollPane

from   javax.swing.text import DefaultHighlighter

#-------------------------------------------------------------------------------
# Name: Highlight()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Highlight( java.lang.Runnable ) :

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
#           print '\nBefore:', frame.getSize()
#           print ' After:', frameSize
            frame.setSize( frameSize )
        frame.setLocation(
            ( screenSize.width  - frameSize.width  ) >> 1,
            ( screenSize.height - frameSize.height ) >> 1
        )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Highlight',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        #-----------------------------------------------------------------------
        # Highlighter, and painter instances
        #-----------------------------------------------------------------------
        self.painter = DefaultHighlighter.DefaultHighlightPainter(
           Color.YELLOW
        )

        #-----------------------------------------------------------------------
        # JTextPane to hold text
        #-----------------------------------------------------------------------
        pane = self.tPane = JTextPane(
            editable = 0,
            preferredSize = ( 585, 300 ),
            text = Help.wsadmin().expandtabs(),
            font = Font( 'Courier', Font.PLAIN, 12 )
        )
        pane.moveCaretPosition( 0 )
        frame.add( JScrollPane( pane ), 'Center' )

        #-----------------------------------------------------------------------
        # Label & input field for user input
        #-----------------------------------------------------------------------
        info = JPanel( BorderLayout() )
        info.add( JLabel( 'Find text:' ), 'West' )
        tf = JTextField(
            actionPerformed = self.search
        )
        info.add( tf, 'Center' )
        frame.add( info, 'South' )

        frame.pack()
        self.center( frame )
        frame.setVisible( 1 )
        tf.requestFocusInWindow()

    #---------------------------------------------------------------------------
    # Name: search()
    # Role: ActionListener event handler called when user press <Enter>
    #---------------------------------------------------------------------------
    def search( self, event ) :
        data    = event.getSource().getText()
        hiliter = self.tPane.getHighlighter()
        hiliter.removeAllHighlights()
        if data :
            doc   = self.tPane.getDocument()
            text  = doc.getText( 0, doc.getLength() )
            start = 0
            here  = text.find( data, start )
            while here > -1 :
                hiliter.addHighlight(
                    here,
                    here + len( data ),
                    self.painter
                )
                start = here + len( data )
                here  = text.find( data, start )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( Highlight() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f Highlight.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
