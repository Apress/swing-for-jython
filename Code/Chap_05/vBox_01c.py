#-------------------------------------------------------------------------------
#    Name: vBox.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython script demonstrating the use of a vertical Box & Glue
#          components
#   Usage: wsadmin -f vBox.py
#            or
#          jython vBox.py
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
from   javax.swing import JLabel
from   javax.swing import JSeparator

#-------------------------------------------------------------------------------
# Name: vBox()
# Role: Used to demonstrate how to create a Jython Swing application
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class vBox( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'verticalBox',
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        box = Box.createVerticalBox()
        box.add( Box.createGlue() )
        box.add( JLabel( '<---- Top ---->' ) )
        box.add( Box.createGlue() )
        box.add( JSeparator() )
        box.add( Box.createGlue() )
        box.add( JLabel( '<---- Mid ---->' ) )
        box.add( Box.createGlue() )
        box.add( JSeparator() )
        box.add( Box.createGlue() )
        box.add( JLabel( '<---- Bot ---->' ) )
        box.add( Box.createGlue() )

        frame.add( box )
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( vBox() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
