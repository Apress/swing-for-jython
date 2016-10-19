#-------------------------------------------------------------------------------
#    Name: PasswordDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script that uses a JPassword field.
#    Note: This script uses the insecure technique of "hard coding" the text to
#          be matched.
#   Usage: wsadmin -f PasswordDemo.py
#            or
#          jython PasswordDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import jarray
import java
import sys
from   java.awt    import EventQueue
from   java.awt    import FlowLayout
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JPasswordField

#-------------------------------------------------------------------------------
# Name: PasswordDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class PasswordDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'PasswordDemo',
            size = ( 215, 100 ),
            layout = FlowLayout(),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add( JLabel( 'Password:' ) )
        self.pwd = frame.add(
            JPasswordField(
                10,
#               echoChar = '\x00',
#               actionCommand = '<Enter>',
                actionPerformed = self.enter
            )
        )
        self.msg = frame.add( JLabel() )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: enter()
    # Role: Event handler associated withe the <Enter> key
    #---------------------------------------------------------------------------
    def enter( self, event ) :
        print 'ActionCommand: "%s"' % event.getActionCommand()
        pwd = self.pwd.getPassword()
        if pwd == jarray.array( 'test', 'c' ) :
            result = 'correct'
        else :
            result = 'wrong!'
        self.msg.setText( 'Password is %s' % result )
        #-----------------------------------------------------------------------
        # For security reasons, we may want to zero fill the password array,
        # but this seems to be a moot point if we have the password string
        # in clear text in our jarray.array() constructor call...
        #-----------------------------------------------------------------------
#       for i in range( len( pwd ) ) :
#           pwd[ i ] = chr( 0 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( PasswordDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
