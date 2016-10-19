#-------------------------------------------------------------------------------
#    Name: SplitPane1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython script using a JSplitPane
#    Note: None of the button have an ActionListener event handler assigned
#   Usage: wsadmin -f SplitPane1.py
#            or
#          jython SplitPane1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JSplitPane

#-------------------------------------------------------------------------------
# Name: SplitPane1()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class SplitPane1( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'SplitPane1',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add( JSplitPane(
                JSplitPane.HORIZONTAL_SPLIT,
                JButton( 'Left' ),
                JButton( 'Right' )
            )
        )
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( SplitPane1() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
