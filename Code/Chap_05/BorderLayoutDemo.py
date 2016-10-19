#-------------------------------------------------------------------------------
#    Name: BorderLayoutDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample / example wsadmin Jython script that positions application
#          components using a BorderLayout layout manager
#    Note: None of the buttons have an ActionListener event handler assigned
#   Usage: wsadmin -f BorderLayoutDemo.py
#            or
#          jython BorderLayoutDemo.py
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
# Name: BorderLayoutDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
#-------------------------------------------------------------------------------
class BorderLayoutDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'BorderLayout',
            layout = BorderLayout(),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        data = [
                   [ 'PAGE_START', BorderLayout.PAGE_START ],
                   [ 'PAGE_END'  , BorderLayout.PAGE_END   ],
                   [ 'LINE_START', BorderLayout.LINE_START ],
                   [ 'LINE_END'  , BorderLayout.LINE_END   ],
               ]

        for name, pos in data :
            frame.add( JButton( name ), pos )

        big = JButton(
                       'CENTER',
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
    EventQueue.invokeLater( BorderLayoutDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
