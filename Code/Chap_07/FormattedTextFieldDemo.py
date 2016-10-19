#-------------------------------------------------------------------------------
#    Name: FormattedTextFieldDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script that uses a JFormattedTextField field.
#    Note: 
#   Usage: wsadmin -f FormattedTextFieldDemo.py
#            or
#          jython FormattedTextFieldDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.awt    import GridLayout
from   java.text   import NumberFormat
from   javax.swing import JFormattedTextField
from   javax.swing import JFrame
from   javax.swing import JLabel

#-------------------------------------------------------------------------------
# Name: FormattedTextFieldDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class FormattedTextFieldDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: addFTF()
    # Role: Add a label, and a FormattedTextField using the specified format
    # Note: No verification of the "name" is performed which means that an
    #       exception could be raised if the value is invalid.
    #---------------------------------------------------------------------------
    def addFTF( self, name ) :
        pane = self.frame.getContentPane()
        pane.add( JLabel( name ) )
        pane.add(
            JFormattedTextField(
                eval( 'NumberFormat.' + name ),
                value = 12345.67890,
                columns = 10
            )
        )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'FormattedTextFieldDemo',
            layout = GridLayout( 0, 2 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        self.addFTF( 'getInstance()'         )
        self.addFTF( 'getCurrencyInstance()' )
        self.addFTF( 'getIntegerInstance()'  )
        self.addFTF( 'getNumberInstance()'   )
        self.addFTF( 'getPercentInstance()'  )
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( FormattedTextFieldDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
