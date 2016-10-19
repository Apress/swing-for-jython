#-------------------------------------------------------------------------------
#    Name: LayeredPaneDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing how JLayeredPane objects work
#    Note: 
#   Usage: wsadmin -f LayeredPaneDemo.py
#            or
#          jython LayeredPaneDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/30  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import Color
from   java.awt    import Dimension
from   java.awt    import EventQueue
from   java.awt    import Point

from   javax.swing import BorderFactory
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JLayeredPane

#-------------------------------------------------------------------------------
# Name: LayeredPaneDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class LayeredPaneDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'LayeredPaneDemo',
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.setContentPane( self.createLayeredPane() )
        frame.pack()
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: createColoredLabel()
    # Role: Create & return a colorful label
    #---------------------------------------------------------------------------
    def createColoredLabel( self, text, color ) :
        return JLabel(
            text,
            opaque = 1,
            size = ( 150, 130 ),
            background = color,
            foreground = Color.black,
            verticalAlignment = JLabel.TOP,
            horizontalAlignment = JLabel.CENTER,
            border = BorderFactory.createLineBorder( Color.black )
        )

    #---------------------------------------------------------------------------
    # Name: createLayeredPane()
    # Role: Create & return a layeredPane example
    #---------------------------------------------------------------------------
    def createLayeredPane( self ) :
        colors = [
            ( 'Red'   , Color.red    ),
            ( 'Orange', Color.orange ),
            ( 'Yellow', Color.yellow ),
            ( 'Green' , Color.green  ),
            ( 'Blue'  , Color.blue   ),
            ( 'Indigo', Color(  75, 0, 130 ) ),
            ( 'Violet', Color( 143, 0, 255 ) )
        ]
        result = JLayeredPane(
            border = BorderFactory.createTitledBorder(
                'Layered Pane'
            ),
            preferredSize = Dimension( 290, 280 )
        )
        position, level = Point( 10, 20 ), 0
        for name, color in colors :
            label = self.createColoredLabel(
                'Layer %d = %s' % ( level, name ),
                color
            )
            label.setLocation( position )
            position.x += 20
            position.y += 20
            result.add( label, level, 0 )
#           result.add( label, level )
#           print level, result.getLayer( label ), result.getPosition( label )
            level += 1
        return result

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( LayeredPaneDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
