#-------------------------------------------------------------------------------
#    Name: ButtonDemo_03.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Another technique for associating an event handler method with a
#          button
#   Usage: wsadmin -f ButtonDemo_03.py
#            or
#          jython ButtonDemo_03.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt       import EventQueue
from   java.lang      import Runnable
from   javax.swing    import JButton
from   javax.swing    import JFrame

#-------------------------------------------------------------------------------
# Name: ButtonDemo_03
# Role: Adding a button to our application that reacts to a button pressed event
#-------------------------------------------------------------------------------
class ButtonDemo_03( Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame( 'ButtonDemo_03' )
        frame.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE )
        button = frame.add( JButton( 'Press me' ) )
        button.actionPerformed = self.buttonPressed
        frame.pack()
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: buttonPressed()
    # Role: Invoked when the associated button is pressed
    #---------------------------------------------------------------------------
    def buttonPressed( self, e ) :
        print 'button pressed'

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( ButtonDemo_03() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
