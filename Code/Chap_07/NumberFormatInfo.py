#-------------------------------------------------------------------------------
#    Name: NumberFormatInfo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script that displays information about different
#          NumberFormat instance types.
#   Usage: wsadmin -f NumberFormatInfo.py
#            or
#          jython NumberFormatInfo.py
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
from   javax.swing import JTextField

#-------------------------------------------------------------------------------
# Name: NumberFormatInfo()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class NumberFormatInfo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: addFTF()
    # Role: Add a label, and a FormattedTextField using the specified format
    #---------------------------------------------------------------------------
    def addFTF( self, name ) :
        pane = self.frame.getContentPane()
        pane.add( JLabel( name ) )
        format = eval( 'NumberFormat.' + name )
        pane.add(
            JFormattedTextField(
                format,
                value = 12345.67890
            )
        )
        pane.add(
            JTextField(
                str( format.getMinimumIntegerDigits() ),
                horizontalAlignment = JTextField.CENTER
            )
        )
        pane.add(
            JTextField(
                str( format.getMaximumIntegerDigits() ),
                horizontalAlignment = JTextField.CENTER
            )
        )
        pane.add(
            JTextField(
                str( format.getMinimumFractionDigits() ),
                horizontalAlignment = JTextField.CENTER
            )
        )
        pane.add(
            JTextField(
                str( format.getMaximumFractionDigits() ),
                horizontalAlignment = JTextField.CENTER
            )
        )
        pane.add(
            JTextField(
                str( format.getRoundingMode() ),
                horizontalAlignment = JTextField.CENTER
            )
        )
        pane.add(
            JTextField(
                str( format.isGroupingUsed() ),
                horizontalAlignment = JTextField.CENTER
            )
        )
        pane.add(
            JTextField(
                str( format.isParseIntegerOnly() ),
                horizontalAlignment = JTextField.CENTER
            )
        )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'NumberFormatInfo',
            layout = GridLayout( 0, 9 ),
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
    EventQueue.invokeLater( NumberFormatInfo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
