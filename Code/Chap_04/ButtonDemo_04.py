#-------------------------------------------------------------------------------
#    Name: ButtonDemo_04.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: A more verbose, and somewhat Java like, version of the button
#          example, this time displaying the result in a Label on the
#          application frame.
#    Note: There is no real need for the ActionListener class to be imported
#   Usage: wsadmin -f ButtonDemo_04.py
#            or
#          jython ButtonDemo_04.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt       import BorderLayout
from   java.awt       import EventQueue
from   java.awt.event import ActionListener
from   java.lang      import Runnable
from   javax.swing    import JButton
from   javax.swing    import JFrame
from   javax.swing    import JLabel

#-------------------------------------------------------------------------------
# Name: ButtonDemo_04
# Role: Adding a button to our application that reacts to a button pressed event
#-------------------------------------------------------------------------------
class ButtonDemo_04( Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame( 'ButtonDemo_04' )
        frame.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE )
        button = frame.add( JButton( 'Press me' ) )
        button.actionPerformed = self.buttonPressed
        self.label = JLabel( 'button press pending' )
        frame.add( self.label, BorderLayout.SOUTH )
        frame.pack()
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: buttonPressed()
    # Role: Invoked when the associated button is pressed
    #---------------------------------------------------------------------------
    def buttonPressed( self, e ) :
        self.label.setText( 'button pressed' )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( ButtonDemo_04() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
