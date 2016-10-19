#-------------------------------------------------------------------------------
#    Name: hvBox.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple script to demonstrate how horizontal & vertical Struct
#          components can be used.
#    Note: Resize the application window to see some differences.
#   Usage: wsadmin -f hvBox.py
#            or
#          jython hvBox.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/22  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue

from   javax.swing import Box
from   javax.swing import JButton
from   javax.swing import JFrame

#-------------------------------------------------------------------------------
# Name: hvBox()
# Role: Used to demonstrate how to create a Jython Swing application
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class hvBox( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'horizontalBox',
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        vert = Box.createVerticalBox()
        vert.add( Box.createGlue() )
        vert.add( JButton( '<>' ) )
        vert.add( Box.createVerticalStrut( 5 ) )
        vert.add( JButton( '<>' ) )
        vert.add( Box.createVerticalStrut( 5 ) )
        vert.add( JButton( '<>' ) )
        vert.add( Box.createGlue() )

        hor = Box.createHorizontalBox()
        hor.add( Box.createGlue() )
        hor.add( JButton( '<>' ) )
        hor.add( Box.createHorizontalStrut( 5 ) )

        hor.add( vert )

        hor.add( Box.createHorizontalStrut( 5 ) )
        hor.add( JButton( '<>' ) )
        hor.add( Box.createGlue() )

        frame.add( hor )
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( hvBox() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
