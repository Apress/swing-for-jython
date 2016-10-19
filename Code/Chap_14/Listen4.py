#-------------------------------------------------------------------------------
#    Name: Listen4.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing how multiple listeners can be used
#   Usage: wsadmin -f Listen4.py
#            or
#          jython Listen4.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/27  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt       import EventQueue
from   java.awt       import GridLayout

from   java.awt.event import KeyAdapter

from   javax.swing    import JFrame
from   javax.swing    import JLabel
from   javax.swing    import JTextField
from   javax.swing    import SwingConstants

#-------------------------------------------------------------------------------
# Name: listener()
# Role: Used to monitor the specified text field for KeyStroke entries
#-------------------------------------------------------------------------------
class listener( KeyAdapter ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Instantiate our MouseListener class
    # Note: In order to access the using component, it needs to be provided
    #---------------------------------------------------------------------------
    def __init__( self, input, msg, fun ) :
        self.input = input
        self.msg   = msg
        self.fun   = fun

    #---------------------------------------------------------------------------
    # Name: keyReleased()
    # Role: Check the input field after the KeyReleased Event event
    #---------------------------------------------------------------------------
    def keyReleased( self, ke ) :
        text = self.input.text
        if text :
            try :
                value = int( self.input.text )
                msg = [ 'No', 'Yes' ][ self.fun( value ) ]
            except :
                msg = 'invalid integer'
        else :
            msg = ''
        self.msg.setText( msg )

#-------------------------------------------------------------------------------
# Name: Listen4()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Listen4( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :

        #-----------------------------------------------------------------------
        # Name: isEven()
        # Role: Return true (1) if the specified value is an even integer
        #-----------------------------------------------------------------------
        def isEven( num ) :
            return not ( num & 1 )


        #-----------------------------------------------------------------------
        # Name: isOdd()
        # Role: Return true (1) if the specified value is an odd integer
        #-----------------------------------------------------------------------
        def isOdd( num ) :
            return num & 1

        #-----------------------------------------------------------------------
        # Name: isPrime()
        # Role: Return true (1) if and only if the specified value is a prime
        #       integer
        #-----------------------------------------------------------------------
        def isPrime( num ):
            result = 0                      # Default = False
            if num == abs( int( num ) ) :   # Only integers allowed
                if num == 1 :               # Special case
                    pass                    #   use default (false)
                elif num == 2 :             # Special case
                    result = 1              #
                elif num & 1 :              # Only odd numbers...
                    for f in xrange( 3, int( num**0.5 ) + 1, 2 ) :
                        if not num % f :
                            break           # f is a factor...
                    else :
                        result = 1          # we found a prime
            return result

        #---------------------------------------------------------------------------
        # Name: label()
        # Role: Instantiate a Right aligned label with the specified text
        #---------------------------------------------------------------------------
        def label( text ) :
            return JLabel(
                    text + ' ',
                    horizontalAlignment = SwingConstants.RIGHT
                )

        frame = JFrame(
            'Listen4',
            layout = GridLayout( 0, 2 ),
            locationRelativeTo = None,
            size = ( 200, 128 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add( label( 'Integer:' ) )
        text  = frame.add( JTextField( 10 ) )
        frame.add( label( 'Even?' ) )
        even  = frame.add( JLabel( '' ) )
        text.addKeyListener( listener( text, even, isEven ) )
        frame.add( label( 'Odd?' ) )
        odd   = frame.add( JLabel( '' ) )
        text.addKeyListener( listener( text, odd, isOdd ) )
        frame.add( label( 'Prime?' ) )
        prime = frame.add( JLabel( '' ) )
        text.addKeyListener( listener( text, prime, isPrime ) )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( Listen4() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
