#-------------------------------------------------------------------------------
#    Name: FrameMethods.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script to compare JFrame and JInternalFrame
#          methods.
#    Note: The following files are expected to be present in the current working
#          directory:
#          1. "JFrame Methods.txt"
#          2. "JInternalFrame Methods.txt"
#   Usage: wsadmin -f FrameMethods.py
#            or
#          jython FrameMethods.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/30  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import Color
from   java.awt    import EventQueue
from   java.awt    import Font
from   java.awt    import GridLayout

from   javax.swing import JCheckBoxMenuItem
from   javax.swing import JComboBox
from   javax.swing import JFrame
from   javax.swing import JMenu
from   javax.swing import JMenuBar
from   javax.swing import JMenuItem
from   javax.swing import JTextArea
from   javax.swing import JScrollPane

#-------------------------------------------------------------------------------
# Name: FrameMethods()
# Role: Application class
# Note: Instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class FrameMethods( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: exit()
    # Role: Terminate the applicaiton
    #---------------------------------------------------------------------------
    def exit( self, event ) :
        sys.exit()

    #---------------------------------------------------------------------------
    # Name: findNot()
    # Role: Filter the text, removing lines containing specified text
    #---------------------------------------------------------------------------
    def findNot( self, data, text ) :
        return '\n'.join(
            [
                line for line in data.splitlines()
                if line.lower().find( text ) < 0
            ]
        )

    #---------------------------------------------------------------------------
    # Name: parse()
    # Role: Parse the specified text, returning a string
    #---------------------------------------------------------------------------
    def parse( self, text ) :
       data = [ line.split( ' | ' ) for line in text.splitlines() ]
       width = max(
           [ len( result ) for result, sign, desc in data ]
       )
       return '\n'.join(
           [
               '%*s %s' % ( width, result, sign )
               for result, sign, desc in data
           ]
       )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'FrameMethods',
            size = ( 1000, 500 ),
            locationRelativeTo = None,
            layout = GridLayout( 0, 2 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        self.one = self.parse(
            self.textFile( 'JFrame Methods.txt' )
        )
        self.left = JTextArea(
            self.one,
            20,
            40,
            editable = 0,
            font = Font( 'Courier' , Font.PLAIN, 12 )
        )

        frame.add( JScrollPane( self.left ) )

        self.two = self.parse( 
            self.textFile( 'JInternalFrame Methods.txt' )
        )
        self.right = JTextArea(
            self.two,
            20,
            40,
            editable = 0,
            font = Font( 'Courier' , Font.PLAIN, 12 )
        )
        frame.add( JScrollPane( self.right ) )

        frame.setJMenuBar( self.makeMenu() )

        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: makeMenu()
    # Role: Create and return the application menu bar
    #---------------------------------------------------------------------------
    def makeMenu( self ) :
        menuBar = JMenuBar(
            background = Color.blue,
            foreground = Color.white
        )

        showMenu = JMenu(
            'Show',
            background = Color.blue,
            foreground = Color.white
        )

        self.deprecated =  JCheckBoxMenuItem(
            'Deprecated',
            1,
            actionPerformed = self.showItems
        )
        showMenu.add( self.deprecated )

        self.protected =  JCheckBoxMenuItem(
            'Protected',
            1,
            actionPerformed = self.showItems
        )
        showMenu.add( self.protected )

        showMenu.addSeparator()
        showMenu.add(
            JMenuItem(
                'Exit',
                actionPerformed = self.exit
            )
        )
        menuBar.add( showMenu )
        return menuBar

    #---------------------------------------------------------------------------
    # Name: showItems()
    # Role: Change the list of methods to be displayed
    #---------------------------------------------------------------------------
    def showItems( self, event ) :
        item = event.getActionCommand()
        one = self.one
        two = self.two
        if not self.deprecated.isSelected() :
            one = self.findNot( one, 'deprecated' )
            two = self.findNot( two, 'deprecated' )
        if not self.protected.isSelected() :
            one = self.findNot( one, 'protected' )
            two = self.findNot( two, 'protected' )
        self.left.setText( one )
        self.right.setText( two )
        
    #---------------------------------------------------------------------------
    # Name: textFile()
    # Role: Load and return the contents of specified file.
    #---------------------------------------------------------------------------
    def textFile( self, filename ) :
        result = ''
        try :
            f = open( filename )
            result = f.read()
            f.close()
        except :
            Type, value = sys.exc_info()[ :2 ]
            result = '%s\n%s' % ( Type, value )
        return result

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( FrameMethods() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
