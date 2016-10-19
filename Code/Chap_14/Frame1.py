#-------------------------------------------------------------------------------
#    Name: Frame1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample Jython Swing script used to show / adjust application frame
#          size
#    Note: Listen for changes to width & height
#   Usage: wsadmin -f Frame1.py
#            or
#          jython Frame1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/28  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt       import EventQueue

from   java.awt.event import ComponentAdapter

from   javax.swing    import JFrame
from   javax.swing    import JLabel
from   javax.swing    import JTextField

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
    # Name: componentResized()
    # Role: Update the width & height text fields to reflect current frame size
    #---------------------------------------------------------------------------
    def componentResized( self, ce ) :
        app   = self.app
        size  = app.frame.getSize()
        app.width.setText( `size.width` )
        app.height.setText( `size.height` )

#-------------------------------------------------------------------------------
# Name: Frame1()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Frame1( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'Frame1',
            size = ( 200, 200 ),
            layout = None,
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.addComponentListener( listener( self ) )
        insets = frame.getInsets()
#       print '\n',insets
        self.width  = JTextField( 4 )
        self.height = JTextField( 4 )
        items = [
            [ JLabel( 'Width:'  ),  7,  7 ],
            [ self.width         , 50,  5 ],
            [ JLabel( 'Height:' ),  7, 31 ],
            [ self.height        , 50, 30 ]
        ]
        for item in items :
            thing = frame.add( item[ 0 ] )
            size  = thing.getPreferredSize()
            thing.setBounds(
                insets.left + item[ 1 ],
                insets.top  + item[ 2 ],
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
    EventQueue.invokeLater( Frame1() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
