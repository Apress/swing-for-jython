#-------------------------------------------------------------------------------
#    Name: ToggleButton.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script that demonstrates a ToggleButton
#    Note: 
#   Usage: wsadmin -f ToggleButton.py
#            or
#          jython ToggleButton.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.awt    import FlowLayout
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JToggleButton

#-------------------------------------------------------------------------------
# Name: ToggleButton()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class ToggleButton( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Toggle Button',
            layout = FlowLayout(),
            size   = ( 275, 85 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        button  = JToggleButton(            # Make a toggle button
            'Off' ,                         # Initial button text
            itemStateChanged = self.toggle  # Event handler
        )

        frame.add( button  )
        frame.setVisible( 1 )

    #-----------------------------------------------------------------------------
    # Name: toggle()
    # Role: Used to handle itemStateChanged events when the button is pressed
    #-----------------------------------------------------------------------------
    def toggle( self, event ) :
        button = event.getItem()
        button.setText( [ 'Off', 'On' ][ button.isSelected() ] )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( ToggleButton() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
