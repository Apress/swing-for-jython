#-------------------------------------------------------------------------------
#    Name: Menu8.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing how to use KeyEvents on menu items
#   Usage: wsadmin -f Menu8.py
#            or
#          jython Menu8.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/11/24  rag  0.1  Chg - Based upon the revised Menu7.py
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt       import EventQueue
from   java.awt.event import KeyEvent
from   javax.swing    import ButtonGroup
from   javax.swing    import JCheckBoxMenuItem
from   javax.swing    import JFrame
from   javax.swing    import JMenu
from   javax.swing    import JMenuBar
from   javax.swing    import JMenuItem
from   javax.swing    import JRadioButtonMenuItem
from   javax.swing    import JSeparator

#-------------------------------------------------------------------------------
# Name: Menu8()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Menu8( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: createMenuBar()
    # Role: Used to create the menu bar, and associated menu & menu items
    #---------------------------------------------------------------------------
    def createMenuBar( self ) :
        menuBar = JMenuBar()

        fileMenu = JMenu( 'File' )
        exitItem = fileMenu.add(
            JMenuItem(
                'Exit',
                KeyEvent.VK_X,
                actionPerformed = self.exit
            )
        )
        menuBar.add( fileMenu )

        codeMenu = JMenu( 'Encoding' )

        data = [
            [ 'ANSI'                , KeyEvent.VK_A ],
            [ 'UTF-8'               , KeyEvent.VK_U ],
            [ 'UCS-2 Big Endian'    , KeyEvent.VK_B ],
            [ 'UCS-2 Little Endian' , KeyEvent.VK_L ]
        ]

        bGroup = ButtonGroup()
        for suffix, mnemonic in data :
            name = 'Encoding in ' + suffix
            rb = JRadioButtonMenuItem(
                name,
                mnemonic = mnemonic,
                selected = ( suffix == 'ANSI' )
            )
            bGroup.add( rb )
            codeMenu.add( rb )
        menuBar.add( codeMenu )

        viewMenu = JMenu( 'View' )
        viewMenu.add( JCheckBoxMenuItem( 'Full screen' ) )
        viewMenu.add( JSeparator() )   # Using JSeparator()
#       viewMenu.addSeparator()        # Using addSeparator()
#       viewMenu.insertSeparator( 1 )  #
        viewMenu.add( JCheckBoxMenuItem( 'Word wrap' ) )
        menuBar.add( viewMenu )

        return menuBar

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Menu8',
            size = ( 200, 125 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.setJMenuBar( self.createMenuBar() )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: exit()
    # Role: Event handler for "File" -> "Exit" menu item
    #---------------------------------------------------------------------------
    def exit( self, event ) :
        sys.exit()

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( Menu8() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
