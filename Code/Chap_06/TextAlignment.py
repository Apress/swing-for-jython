#-------------------------------------------------------------------------------
#    Name: TextAlignment.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script to demonstrate some JTextField text
#          alignment properties.
#   Usage: wsadmin -f TextAlignment.py
#            or
#          jython TextAlignment.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.awt    import GridLayout
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JTextField

#-------------------------------------------------------------------------------
# Name: TextAlignment()
# Role: Display a JFrame instance with various JTextField alignments
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class TextAlignment( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'TextAlignment',
            layout = GridLayout( 0, 2 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        data = [
            [ 'Left'    , JTextField.LEFT     ],
            [ 'Center'  , JTextField.CENTER   ],
            [ 'Right'   , JTextField.RIGHT    ],
            [ 'Leading' , JTextField.LEADING  ],
            [ 'Trailing', JTextField.TRAILING ]
        ]
        for label, align in data :
            frame.add( JLabel( label ) )
            text = frame.add(
                JTextField(
                    5,
                    text = str( align ),
                    horizontalAlignment = align
                )
            )
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( TextAlignment() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
