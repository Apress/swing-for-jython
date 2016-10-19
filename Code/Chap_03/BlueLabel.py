#-------------------------------------------------------------------------------
#    Name: BlueLabel.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Demonstrate how to display a colored label on the content pane
#    Note: This script is not referenced in the book
#   Usage: wsadmin -f BlueLabel.py
#            or
#          jython BlueLabel.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import Color
from   java.awt    import Dimension
from   java.awt    import EventQueue
from   javax.swing import JFrame
from   javax.swing import JLabel

#-------------------------------------------------------------------------------
# Name: BlueLabel()
# Role: Trivial Jython Swing application
#-------------------------------------------------------------------------------
class BlueLabel( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Create & display the application JFrame on the Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame( 'BlueLabel' )       # Create a JFrame with a title
        frame.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE )

        Label = JLabel()                    # Create an empty label
        Label.setOpaque( 1 )                # Must be opaque for color to be seen
        Label.setBackground( Color.BLUE )   # Make the label blue
        Label.setPreferredSize( Dimension( 200, 200 ) )

        frame.getContentPane().add( Label ) # Add the label to the content pane

        frame.pack()                        # Size frame to display the contents
        frame.setVisible( 1 )               # Finally, make the frame visible

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( BlueLabel() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application: ' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()