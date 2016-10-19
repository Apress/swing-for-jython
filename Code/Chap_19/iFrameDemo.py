#-------------------------------------------------------------------------------
#    Name: iFrameDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script demonstrating some simple internal frames
#    Note: The internal frames require manual manipulation in order to match the
#          arrangement seen in Figure 19-1 in the text.
#   Usage: wsadmin -f iFrameDemo.py
#            or
#          jython iFrameDemo.py
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

#-------------------------------------------------------------------------------
# Name: iFrameDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class iFrameDemo( java.lang.Runnable ) :

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
            'iFrameDemo',
            bounds = ( x, y, w, h ),        # location & size
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        desktop = JDesktopPane()
        for i in range( 3 ) :
            inner = JInternalFrame(
                'Inner Frame #%d' % ( i + 1 ),
                1,                          # Resizeable
                1,                          # Closeable
                1,                          # Maximizable
                1,                          # Iconifiable
                visible = 1,                # setVisible( 1 )
                bounds = ( i * 25 + 25, i * 25 + 25, 250, 250 )
            )
            desktop.add( inner )
#           desktop.add( inner, i, 0 )      # preferred add() method
        frame.setContentPane( desktop )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( iFrameDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
