#-------------------------------------------------------------------------------
#    Name: Menu6.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing how to use CheckBox menu items
#   Usage: wsadmin -f Menu6.py
#            or
#          jython Menu6.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Command: Menu6
# Purpose: Creating a menu bar with menu and menu items
#   Usage: wsadmin -f Menu6.py
# Example: ./wsadmin.sh -f Menu6.py
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue
from   javax.swing import JCheckBoxMenuItem
from   javax.swing import JFrame
from   javax.swing import JMenu
from   javax.swing import JMenuBar
from   javax.swing import JMenuItem

#-------------------------------------------------------------------------------
# Name: Menu6()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Menu6( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: createMenuBar()
    # Role: Used to create the menu bar, and associated menu & menu items
    #---------------------------------------------------------------------------
    def createMenuBar( self ) :
        menuBar = JMenuBar()

        fileMenu = JMenu( 'File' )

        data = [
            [ 'Spam' , self.spam  ],
            [ 'Eggs' , self.eggs  ],
            [ 'Bacon', self.bacon ]
        ]

        for name, handler in data :
            fileMenu.add(
                JCheckBoxMenuItem(
                    name,
                    actionPerformed = handler
                )
            )

        exitItem = fileMenu.add(
            JMenuItem(
                'Exit',
                actionPerformed = self.exit
            )
        )
        menuBar.add( fileMenu )

        helpMenu = JMenu( 'Help' )
        aboutItem = helpMenu.add(
            JMenuItem(
                'About',
                actionPerformed = self.about
            )
        )
        menuBar.add( helpMenu )

        return menuBar

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Menu6',
            size = ( 200, 125 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.setJMenuBar( self.createMenuBar() )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: spam()
    # Role: Event handler for "File" -> "Spam" menu item
    #---------------------------------------------------------------------------
    def spam( self, event )  : print 'Menu6.spam()'

    #---------------------------------------------------------------------------
    # Name: eggs()
    # Role: Event handler for "File" -> "Eggs" menu item
    #---------------------------------------------------------------------------
    def eggs( self, event )  : print 'Menu6.eggs()'

    #---------------------------------------------------------------------------
    # Name: bacon()
    # Role: Event handler for "File" -> "Bacon" menu item
    #---------------------------------------------------------------------------
    def bacon( self, event ) : print 'Menu6.bacon()'

    #---------------------------------------------------------------------------
    # Name: about()
    # Role: Event handler for "Help" -> "About" menu item
    #---------------------------------------------------------------------------
    def about( self, event ) : print 'Menu6.about()'

    #---------------------------------------------------------------------------
    # Name: exit()
    # Role: Event handler for "File" -> "Exit" menu item
    #---------------------------------------------------------------------------
    def exit( self, event ) :
        print 'Menu6.exit()'
        sys.exit()

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( Menu6() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
