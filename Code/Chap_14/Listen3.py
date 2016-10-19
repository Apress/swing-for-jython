#-------------------------------------------------------------------------------
#    Name: Listen3.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script demonstrating how a key listener might be
#          used
#   Usage: wsadmin -f Listen3.py
#            or
#          jython Listen3.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/27  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt       import EventQueue
from   java.awt       import FlowLayout

from   java.awt.event import KeyListener

from   javax.swing    import JButton
from   javax.swing    import JLabel
from   javax.swing    import JFrame
from   javax.swing    import JScrollPane
from   javax.swing    import JTextArea
from   javax.swing    import JTextField
from   javax.swing    import SwingConstants

#-------------------------------------------------------------------------------
# Name: listener()
# Role: Used to monitor KeyStroke events
#-------------------------------------------------------------------------------
class listener( KeyListener ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Instantiate our KeyListener class
    # Note: In order to access the using component, it needs to be provided
    #---------------------------------------------------------------------------
    def __init__( self, textArea ) :
        self.textArea = textArea

    #---------------------------------------------------------------------------
    # Name: keyPressed()
    # Role: Log the event
    #---------------------------------------------------------------------------
    def keyPressed( self, me ) :
        self.logEvent( me )

    #---------------------------------------------------------------------------
    # Name: keyReleased()
    # Role: Log the event
    #---------------------------------------------------------------------------
    def keyReleased( self, me ) :
        self.logEvent( me )

    #---------------------------------------------------------------------------
    # Name: keyTyped()
    # Role: Log the event
    #---------------------------------------------------------------------------
    def keyTyped( self, me ) :
        self.logEvent( me )

    #---------------------------------------------------------------------------
    # Name: logEvent()
    # Role: Update the user text area with details of the current event
    #---------------------------------------------------------------------------
    def logEvent( self, me ) :
        self.textArea.append( me.toString() + '\n' )

#-------------------------------------------------------------------------------
# Name: Listen3()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Listen3( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Listen3',
            layout = FlowLayout(),
            locationRelativeTo = None,
            size = ( 512, 256 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add(
            JLabel(
                'Input:',
                horizontalAlignment = SwingConstants.RIGHT
            )
        )
        self.text = frame.add( JTextField( 8 ) )
        frame.add(
            JButton(
                'Clear',
                actionPerformed = self.clear
            )
        )
        self.textArea = JTextArea( rows = 10, columns = 40 ) 
        frame.add( JScrollPane( self.textArea ) )
        self.text.addKeyListener( listener( self.textArea ) )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: clear()
    # Role: Event handler used to clear the application text area
    #---------------------------------------------------------------------------
    def clear( self, event ) :
        self.text.setText( '' )
        self.textArea.setText( '' )
        self.text.requestFocusInWindow()

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( Listen3() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
