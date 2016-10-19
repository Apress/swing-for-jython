#-------------------------------------------------------------------------------
#    Name: ScreenLoc.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script that demonstrates the creation of a
#          JFrame() instance on each physical display.
#    Note: This script expects multiple displays to be connected to the system.
#   Usage: wsadmin -f ScreenLoc.py
#            or
#          jython ScreenLoc.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue
from   java.awt    import GraphicsEnvironment
from   java.awt    import Rectangle

from   javax.swing import JLabel
from   javax.swing import JFrame

#-------------------------------------------------------------------------------
# Name: ScreenLoc()
# Role: Show how to create, and display a JFrame instance on each display
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class ScreenLoc( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        d   = 0
        LGE = GraphicsEnvironment.getLocalGraphicsEnvironment()
        for GD in LGE.getScreenDevices() :       # foreach ScreenDevice...
            CO = GD.getDefaultConfiguration()    # Configuration object
            for GC in GD.getConfigurations() :   # GraphicConfiguration
                b = GC.getBounds()               # virtual bounds
                frame = JFrame(
                    'Screen: %d' % d,            # d == Device # 0..N
                    CO,
                    size = (
                        int( b.getWidth()  ) >> 1,
                        int( b.getHeight() ) >> 3
                    ),
                    defaultCloseOperation = JFrame.EXIT_ON_CLOSE
                )
                d += 1
                frame.add( JLabel( `CO` ) )
                frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( ScreenLoc() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
