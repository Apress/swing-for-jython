#-------------------------------------------------------------------------------
#    Name: SplitPane4.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython script using a frame containing nested JSplitPanes
#    Note: Each button has an ActionListener event handler assigned to display
#          component size attribute details (see debug() method).
#   Usage: wsadmin -f SplitPane4.py
#            or
#          jython SplitPane4.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/22  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JSplitPane

#-------------------------------------------------------------------------------
# Name: SplitPane4()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class SplitPane4( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'SplitPane4',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        button = self.button
        frame.add(
            JSplitPane(
                JSplitPane.VERTICAL_SPLIT,
                button( 'Top' ),
                JSplitPane(
                    JSplitPane.HORIZONTAL_SPLIT,
                    button( 'Left' ),
                    button( 'Right' ),
                )
            )
        )
        frame.pack()
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: button()
    # Role: Return a JButton() created with the specified text, and having the
    #       actionPerformed method assigned
    #---------------------------------------------------------------------------
    def button( self, text ) :
        return JButton( text, actionPerformed = self.debug )

    #---------------------------------------------------------------------------
    # Name: debug()
    # Role: Simple debug method used to display some component size attributes 
    #---------------------------------------------------------------------------
    def debug( self, event ) :
        b = event.getSource()
        print '\n%6s:' % b.getActionCommand(),
        s = b.getSize()
        print 'current %3d %3d' % ( s.width, s.height ),
        s = b.getMinimumSize()
        print 'min %3d %3d' % ( s.width, s.height ),
        s = b.getMaximumSize()
        print 'max %3d %3d' % ( s.width, s.height ),
        s = b.getPreferredSize()
        print 'preferred %3d %3d' % ( s.width, s.height ),

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( SplitPane4() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
