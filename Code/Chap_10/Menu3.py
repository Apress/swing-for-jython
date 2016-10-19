#-------------------------------------------------------------------------------
#    Name: Menu3.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script to show how easily a MenuBar can be
#          created.
#    Note: The MenuBar is colored Blue to make it visible to the user, and
#          the color choice of the menu items (white) makes them much easier
#          to read.
#   Usage: wsadmin -f Menu3.py
#            or
#          jython Menu3.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Command: Menu3
# Purpose: Creating a menu bar with menu and menu items
#   Usage: wsadmin -f Menu3.py
# Example: ./wsadmin.sh -f Menu3.py
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import Color
from   java.awt    import EventQueue
from   javax.swing import JFrame
from   javax.swing import JMenu
from   javax.swing import JMenuBar
from   javax.swing import JMenuItem

#-------------------------------------------------------------------------------
# Name: Menu3()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Menu3( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Menu3',
            size = ( 200, 125 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        menuBar = JMenuBar( background = Color.blue )
#       print '\nmenuBar size before:', menuBar.getPreferredSize()

        fileMenu = JMenu( 'File', foreground = Color.white )
        fileMenu.add( JMenuItem( 'Exit' ) )
        menuBar.add( fileMenu )
#       print 'menuBar size  after:', menuBar.getPreferredSize()

        helpMenu = JMenu( 'Help', foreground = Color.white )
        helpMenu.add( JMenuItem( 'About' ) )
        menuBar.add( helpMenu )

        frame.setJMenuBar( menuBar )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( Menu3() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
