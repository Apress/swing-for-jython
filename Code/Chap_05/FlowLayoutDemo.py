#-------------------------------------------------------------------------------
#    Name: FlowLayoutDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample / example wsadmin Jython script that positions application
#          components using a FlowLayout layout manager
#    Note: None of the buttons have an ActionListener event handler assigned
#   Usage: wsadmin -f FlowLayoutDemo.py
#            or
#          jython FlowLayoutDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import ComponentOrientation
from   java.awt    import EventQueue
from   java.awt    import FlowLayout
from   javax.swing import JButton
from   javax.swing import JFrame

#-------------------------------------------------------------------------------
# Name: FlowLayoutDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
#-------------------------------------------------------------------------------
class FlowLayoutDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'FlowLayout',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        cp = frame.getContentPane()
        #-----------------------------------------------------------------------
        # The alignment can be one of the following values:
        #-----------------------------------------------------------------------
#       cp.setLayout( FlowLayout( FlowLayout.LEFT ) )
#       cp.setLayout( FlowLayout( FlowLayout.RIGHT ) )
        cp.setLayout( FlowLayout() )   # FlowLayout.CENTER  is the default value
#       cp.setLayout( FlowLayout( FlowLayout.LEADING ) )
#       cp.setLayout( FlowLayout( FlowLayout.TRAILING ) )

        for name in '1,two,Now is the time...'.split( ',' ) :
            frame.add( JButton( name ) )

        #-----------------------------------------------------------------------
        # The ComponentOrientation can be one of the following values
        # Note: The default value is related to the system locale
        #-----------------------------------------------------------------------
#       cp.setComponentOrientation( ComponentOrientation.LEFT_TO_RIGHT )
#       cp.setComponentOrientation( ComponentOrientation.RIGHT_TO_LEFT )

        frame.setSize( 350, 100 )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( FlowLayoutDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
