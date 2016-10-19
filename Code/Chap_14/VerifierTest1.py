#-------------------------------------------------------------------------------
#    Name: VerifierTest1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample wsadmin Jython script demonstrating simple input verification
#    Note: Insufficient user feedback provided
#   Usage: wsadmin -f VerifierTest1.py
#            or
#          jython VerifierTest1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/28  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt           import BorderLayout
from   java.awt           import EventQueue

from   javax.swing        import InputVerifier
from   javax.swing        import JFrame
from   javax.swing        import JLabel
from   javax.swing        import JTextField

#-------------------------------------------------------------------------------
# Name: inputChecker()
# Role: Used to demonstrate how to verify input
#-------------------------------------------------------------------------------
class inputChecker( InputVerifier ) :

    #---------------------------------------------------------------------------
    # Name: verify()
    # Role: Return true (1) if the input field contains a valid value
    #---------------------------------------------------------------------------
    def verify( self, input ) :
        return input.getText() == "pass"

#-------------------------------------------------------------------------------
# Name: VerifierTest1()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class VerifierTest1( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'VerifierTest1',
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add(
            JTextField(
                'Enter "pass"',
                inputVerifier = inputChecker()
            ),
            BorderLayout.NORTH
        )
        frame.add(
            JTextField( 'TextField 2' ),
            BorderLayout.SOUTH
        )
        
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( VerifierTest1() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
