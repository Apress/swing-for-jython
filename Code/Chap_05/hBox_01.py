#-------------------------------------------------------------------------------
#    Name: hBox.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple application using Box class to position some objects
#    Note: Uncomment the "box.add( Box.createGlue() )" to statements to
#          experiment and see how Glue components function.
#   Usage: wsadmin -f hBox.py
#            or
#          jython hBox.py
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

#-------------------------------------------------------------------------------
# Name: hBox()
# Role: Used to demonstrate how to create a Jython Swing application
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class hBox( java.lang.Runnable ) :

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
        box = Box.createHorizontalBox()
#       box.add( Box.createGlue() )
        box.add( JLabel( '<---- Left ---->' ) )
#       box.add( Box.createGlue() )
        box.add( JLabel( '<---- Middle ---->' ) )
#       box.add( Box.createGlue() )
        box.add( JLabel( '<---- Right ---->' ) )
#       box.add( Box.createGlue() )

        frame.add( box )
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( hBox() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
