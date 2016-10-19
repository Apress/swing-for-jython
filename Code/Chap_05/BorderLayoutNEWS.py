#-------------------------------------------------------------------------------
#    Name: BorderLayoutNEWS.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample / example wsadmin Jython script that positions application
#          components using a BorderLayout layout manager to position the
#          components using the North, East, West, and South directional
#          constants.
#    Note: None of the buttons have an ActionListener event handler assigned
#   Usage: wsadmin -f BorderLayoutNEWS.py
#            or
#          jython BorderLayoutNEWS.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import BorderLayout
from   java.awt    import Dimension
from   java.awt    import EventQueue
from   javax.swing import JButton
from   javax.swing import JFrame

#-------------------------------------------------------------------------------
# Name: BorderLayoutNEWS()
# Role: Used to demonstrate how to create, and display a JFrame instance
#-------------------------------------------------------------------------------
class BorderLayoutNEWS( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'BorderLayoutNEWS',
            layout = BorderLayout(),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        data = [
                 BorderLayout.NORTH,
                 BorderLayout.SOUTH,
                 BorderLayout.EAST,
                 BorderLayout.WEST
               ]

        for pos in data :
            frame.add( JButton( pos ), pos )

        big = JButton(
                       'Center',
                        preferredSize = Dimension( 256, 128 )
                     )
        frame.add( big, BorderLayout.CENTER )

        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( BorderLayoutNEWS() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
