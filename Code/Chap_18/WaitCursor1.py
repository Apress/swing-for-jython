#-------------------------------------------------------------------------------
#    Name: WaitCursor1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing how to use the WaitCursor.
#    Note: 
#   Usage: wsadmin -f WaitCursor1.py
#            or
#          jython WaitCursor1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/30  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   time        import sleep

from   java.awt    import Cursor
from   java.awt    import EventQueue

from   javax.swing import JButton
from   javax.swing import JFrame

#-------------------------------------------------------------------------------
# Name: WaitCursor1()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class WaitCursor1( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'WaitCursor1',
            size = ( 150, 100 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add(
            JButton(
                'Wait',
                actionPerformed = self.wait
            )
        )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: wait()
    # Role: Demonstrate changing the cursor...
    #---------------------------------------------------------------------------
    def wait( self, event ) :
        source = event.getSource()
        prev   = source.getCursor()
        source.setCursor(
            Cursor.getPredefinedCursor( Cursor.WAIT_CURSOR )
        )
        sleep( 5 )
        source.setCursor( prev )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( WaitCursor1() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
