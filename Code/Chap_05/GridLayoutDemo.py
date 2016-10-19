#-------------------------------------------------------------------------------
#    Name: GridLayoutDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script that positions application components
#          using a GridLayout layout manager.  Additionally, the buttons can be
#          used to changed the horizontal and vertical gaps between components.
#    Note: The button ActionListener event hander method changes either the
#          horizontal or vertical gap between buttons.
#   Usage: wsadmin -f GridLayoutDemo.py
#            or
#          jython GridLayoutDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/22  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.awt    import GridLayout
from   javax.swing import BoxLayout
from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JPanel

#-------------------------------------------------------------------------------
# Name: GridLayoutDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
#-------------------------------------------------------------------------------
class GridLayoutDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'GridLayoutDemo',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        main = JPanel()
        main.setLayout( BoxLayout( main, BoxLayout.Y_AXIS ) )
        self.panes = []
        self.addButtons( main, 'Horizontal:' )
        self.addButtons( main, 'Vertical:' )
        frame.add( main )

        frame.setSize( 500, 250 )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: addButtons()
    # Role: Add buttons to the specified container using a GridLayout manager
    #---------------------------------------------------------------------------
    def addButtons( self, container, prefix ) :
        pane = JPanel( GridLayout( 0, 3 ) )
        self.panes.append( pane )
        for size in '0,2,4,8,16'.split( ',' ) :
            pane.add(
                JButton(
                    '%s %s' % ( prefix, size ),
                    actionPerformed = self.buttonPress
                )
            )
        container.add( pane )

    #---------------------------------------------------------------------------
    # Name: buttonPress()
    # Role: Event handler
    #---------------------------------------------------------------------------
    def buttonPress( self, event ) :
        dir, size = event.getActionCommand().split( ' ' )
        if dir[ 0 ] == 'H' :
            for pane in self.panes :
                layout = pane.getLayout()
                layout.setHgap( int( size ) )
                layout.layoutContainer( pane )
        else :
            for pane in self.panes :
                layout = pane.getLayout()
                layout.setVgap( int( size ) )
                layout.layoutContainer( pane )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( GridLayoutDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
