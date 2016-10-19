#-------------------------------------------------------------------------------
#    Name: Box1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample application using Box class to position some buttons
#    Note: None of the buttons have an ActionListener event handler assigned
#   Usage: wsadmin -f Box1.py
#            or
#          jython Box1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/22  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import Dimension
from   java.awt    import EventQueue

from   javax.swing import Box
from   javax.swing import JButton
from   javax.swing import JFrame

#-------------------------------------------------------------------------------
# Name: Box1()
# Role: Used to demonstrate how to create a Jython Swing application
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Box1( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Box1',
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        name = 'A'
        size = Dimension( 46, 26 )
        vBox = Box.createVerticalBox()
        for row in range( 5 ) :
            hBox = Box.createHorizontalBox()
            for col in range( 5 ) :
                button = JButton( name )
#               button = JButton(
#                   name,
#                   size = size,
#                   minimumSize = size,
#                   maximumSize = size,
#                   preferredSize = size
#               )
                hBox.add( button )
                self.showSizes( name, button )
                name = chr( ord( name ) + 1 )
            vBox.add( hBox )
        frame.add( vBox )
        frame.pack()
        frame.setVisible( 1 )

    def showSizes( self, name, obj ) :
        text = name
        size = obj.getSize()
        text += ' %2d %2d ' % ( size.width, size.height )
        size = obj.getMinimumSize()
        text += ' %2d %2d ' % ( size.width, size.height )
        size = obj.getMaximumSize()
        text += ' %2d %2d ' % ( size.width, size.height )
        size = obj.getPreferredSize()
        text += ' %2d %2d ' % ( size.width, size.height )
        print text

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( Box1() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
