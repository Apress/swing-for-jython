#-------------------------------------------------------------------------------
#    Name: iFrameEvents1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample Jython Swing script demonstrating some simple internal frames
#          event information details.
#    Note: This is the initial iteration where no event listeners exist
#   Usage: wsadmin -f iFrameEvents1.py
#            or
#          jython iFrameEvents1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/30  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue
from   java.awt    import Toolkit

from   javax.swing import JDesktopPane
from   javax.swing import JFrame
from   javax.swing import JInternalFrame
from   javax.swing import JScrollPane
from   javax.swing import JTextArea

#-------------------------------------------------------------------------------
# Name: eventLogger()
# Role: Used to implement a special internal frame to show InternalFrameEvent
#       details
#-------------------------------------------------------------------------------
class eventLogger( JInternalFrame ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: eventLogger class constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        JInternalFrame.__init__(
            self,
            'eventLogger',
            1,               # Resizeable  - yes
            0,               # Closeable   - no
            0,               # Maximizable - no
            1,               # Iconifiable - yes
            visible = 1,
            bounds = ( 0, 0, 250, 250 )
        )
        self.textArea = JTextArea(
             20,             # rows
             40,             # columns
             editable = 0    # read-only
        )
        self.add( JScrollPane( self.textArea ) )

#-------------------------------------------------------------------------------
# Name: iFrameEvents1()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class iFrameEvents1( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        screenSize = Toolkit.getDefaultToolkit().getScreenSize()
        w = screenSize.width  >> 1          # 1/2 screen width
        h = screenSize.height >> 1          # 1/2 screen height
        x = ( screenSize.width  - w ) >> 1
        y = ( screenSize.height - h ) >> 1
        frame = JFrame(
            'iFrameEvents1',
            bounds = ( x, y, w, h ),        # location & size
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        desktop = JDesktopPane()
        desktop.add( eventLogger(), 0, 0 )
        frame.setContentPane( desktop )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( iFrameEvents1() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
