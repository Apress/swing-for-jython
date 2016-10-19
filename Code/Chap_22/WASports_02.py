#-------------------------------------------------------------------------------
#    Name: WASports_02.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Display information about the ports configured within a cell
#    Note: This script requires a WebSphere Application Server environment
#   Usage: wsadmin -f WASports_02.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 14/04/19  rag  0.2   Add - Add a (vertically) split pane to the internal frame
# 14/04/19  rag  0.1   Add - Display the JFrame with an empty internal frame
# 14/04/19  rag  0.0   New - Initial iteration - simply display an empty Frame
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Import the necessary Java, AWT & Swing modules
#-------------------------------------------------------------------------------
import java

from   java.awt          import Dimension
from   java.awt          import EventQueue
from   java.awt          import Point
from   java.awt          import Toolkit

from   javax.swing       import JDesktopPane
from   javax.swing       import JFrame
from   javax.swing       import JLabel
from   javax.swing       import JInternalFrame
from   javax.swing       import JSplitPane

#-------------------------------------------------------------------------------
# Name: InternalFrame
# Role: Provide a class for our internal frames
#-------------------------------------------------------------------------------
class InternalFrame( JInternalFrame ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    #---------------------------------------------------------------------------
    def __init__( self, title, size, location, closable = 0 ) :
        JInternalFrame.__init__(
            self,
            title,
            resizable   = 1,
            closable    = closable,
            maximizable = 1,
            iconifiable = 1,
            size        = size
        )
        self.setLocation( location )

        pane = self.add(
            JSplitPane(
                JSplitPane.HORIZONTAL_SPLIT,
                JLabel( 'Left' ),
                JLabel( 'Right' )
            )
        )
        pane.setDividerLocation( size.width >> 1 )

        self.setVisible( 1 )

#-------------------------------------------------------------------------------
# Name: WASports_02
# Role: Display a table of the Ports and associated End Point Names
#-------------------------------------------------------------------------------
class WASports_02( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Called by Swing Event Dispatcher thread
    #---------------------------------------------------------------------------
    def run( self ) :

        #-----------------------------------------------------------------------
        # Starting width, height & location of the application frame
        #-----------------------------------------------------------------------
        screenSize = Toolkit.getDefaultToolkit().getScreenSize()
        w = screenSize.width  >> 1          # Use 1/2 screen width
        h = screenSize.height >> 1          # and 1/2 screen height
        x = ( screenSize.width  - w ) >> 1  # Top left corner of frame
        y = ( screenSize.height - h ) >> 1

        #-----------------------------------------------------------------------
        # Center the application frame in the window
        #-----------------------------------------------------------------------
        frame = self.frame = JFrame(
            'WASports_02',
            bounds = ( x, y, w, h ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        #-----------------------------------------------------------------------
        # Internal frames require us to use a JDesktopPane()
        #-----------------------------------------------------------------------
        desktop = JDesktopPane()

        #-----------------------------------------------------------------------
        # Create our initial internal frame, and add it to the desktop
        #-----------------------------------------------------------------------
        internal = InternalFrame(
            'InternalFrame',
            size = Dimension( w >> 1, h >> 1 ),
            location = Point( 5, 5 )
        )
        desktop.add( internal )

        frame.setContentPane( desktop )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
# Role: main entry point - verify that the script was executed, not imported.
#-------------------------------------------------------------------------------
if __name__ == '__main__' :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( WASports_02() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f WASports_02.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
