#-------------------------------------------------------------------------------
#    Name: AbsoluteLayout.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample / example wsadmin Jython script that positions application
#          components without the use of a Layout Manager
#   Usage: wsadmin -f AbsoluteLayout.py
#            or
#          jython AbsoluteLayout.py
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

#-------------------------------------------------------------------------------
# Name: AbsoluteLayout()
# Role: Used to demonstrate how to create, and display a JFrame instance
#-------------------------------------------------------------------------------
class AbsoluteLayout( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'AbsoluteLayout',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        # Replace the default Layout Manager
        frame.setLayout( None )

        # Information defining button title, location & size
        data = [
                    [ 'A', 20, 10,  0,  0 ],
                    [ 'B', 40, 40, 10, 10 ],
                    [ 'C', 80, 20, 20, 20 ]
               ]

        # For each data entry, create & position a button
        insets = frame.getInsets()
        for item in data :
            button = frame.add( JButton( item[ 0 ] ) )
            size   = button.getPreferredSize()
            button.setBounds(
                insets.left + item[ 1 ],
                insets.top  + item[ 2 ],
                size.width  + item[ 3 ],
                size.height + item[ 4 ]
            )

        # Define the application frame size
        frame.setSize(
            300 + insets.left + insets.right,   # frame width
            150 + insets.top + insets.bottom    # frame height
        )

        # Make the frame visible
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( AbsoluteLayout() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
