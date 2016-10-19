#-------------------------------------------------------------------------------
#    Name: ButtonDemo_02.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: A sample Jython script showing how to react to a button pressed event
#          using a more convenient Jython multiple inheritance technique
#   Usage: wsadmin -f ButtonDemo_02.py
#            or
#          jython ButtonDemo_02.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt       import EventQueue
from   java.awt.event import ActionListener
from   java.lang      import Runnable
from   javax.swing    import JButton
from   javax.swing    import JFrame

#-------------------------------------------------------------------------------
# Name: ButtonDemo_02()
# Role: Adding a button to our application
#-------------------------------------------------------------------------------
class ButtonDemo_02( Runnable, ActionListener ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame( 'ButtonDemo_02' )
        frame.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE )
        button = frame.add( JButton( 'Press me' ) )
        button.addActionListener( self )
        frame.pack()
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: actionPerformed()
    # Role: Invoked when the associated button is pressed
    #---------------------------------------------------------------------------
    def actionPerformed( self, e ) :
        print 'button pressed'

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( ButtonDemo_02() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
