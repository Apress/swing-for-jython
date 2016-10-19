#-------------------------------------------------------------------------------
#    Name: Frame4.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample Jython Swing script used to show / adjust application frame
#          size
#    Note: Use the JFormattedTextField & PropertyChangeListener
#   Usage: wsadmin -f Frame4.py
#            or
#          jython Frame4.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/28  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt       import EventQueue

from   java.awt.event import ComponentAdapter

from   java.text      import NumberFormat

from   javax.swing    import JFormattedTextField
from   javax.swing    import JFrame
from   javax.swing    import JLabel

#-------------------------------------------------------------------------------
# Name: listener()
# Role: Component adapter used to monitor frame resize events
#-------------------------------------------------------------------------------
class listener( ComponentAdapter ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Save a reference to the application instance so we can manipulate
    #       its attributes
    #---------------------------------------------------------------------------
    def __init__( self, app ) :
        self.app = app

    #---------------------------------------------------------------------------
    # Name: updateInfo()
    # Role: Update the text fields to reflect current frame size & position
    #---------------------------------------------------------------------------
    def updateInfo( self ) :
        app    = self.app
        bounds = app.frame.getBounds()
        app.width.setText( `bounds.width` )
        app.height.setText( `bounds.height` )
        app.x.setText( `bounds.x` )
        app.y.setText( `bounds.y` )

    #---------------------------------------------------------------------------
    # Name: componentMoved()
    # Role: Update the text fields to reflect current frame size & position
    #---------------------------------------------------------------------------
    def componentMoved( self, ce ) :
        self.updateInfo()

    #---------------------------------------------------------------------------
    # Name: componentResized()
    # Role: Update the text fields to reflect current frame size & position
    #---------------------------------------------------------------------------
    def componentResized( self, ce ) :
        self.updateInfo()

    #---------------------------------------------------------------------------
    # Name: componentShown()
    # Role: Update the text fields to reflect current frame size & position
    #---------------------------------------------------------------------------
    def componentShown( self, ce ) :
        self.updateInfo()

#-------------------------------------------------------------------------------
# Name: Frame4()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Frame4( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'Frame4',
            size = ( 200, 200 ),
            layout = None,
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.addComponentListener( listener( self ) )
        self.width  = JFormattedTextField(
            NumberFormat.getIntegerInstance(),
            columns = 4
        )
        self.height = JFormattedTextField(
            NumberFormat.getIntegerInstance(),
            columns = 4
        )
        self.x      = JFormattedTextField(
            NumberFormat.getIntegerInstance(),
            columns = 4
        )
        self.y      = JFormattedTextField(
            NumberFormat.getIntegerInstance(),
            columns = 4
        )
        items = [
            [ JLabel( 'Width:' ) , 11,  7 ],
            [ self.width         , 50,  5 ],
            [ JLabel( 'Height:' ),  7, 31 ],
            [ self.height        , 50, 30 ],
            [ JLabel( 'X:' )     , 35, 55 ],
            [ self.x             , 50, 53 ],
            [ JLabel( 'Y:' )     , 35, 79 ],
            [ self.y             , 50, 78 ]
        ]
        for item in items :
            thing = frame.add( item[ 0 ] )
            size  = thing.getPreferredSize()
            thing.setBounds(
                item[ 1 ],
                item[ 2 ],
                size.width,
                size.height
            )

        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( Frame4() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
