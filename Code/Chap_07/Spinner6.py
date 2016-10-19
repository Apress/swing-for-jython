#-------------------------------------------------------------------------------
#    Name: Spinner6.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script used to display a JSpinner constructed
#          using a SpinnerDateModel() object instantiated using specified values
#          and a DateEditor() to identify how dates should be displayed.
#   Usage: wsadmin -f Spinner6.py
#            or
#          jython Spinner6.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.awt    import FlowLayout
from   java.util   import Date
from   java.util   import Calendar
from   javax.swing import JFormattedTextField
from   javax.swing import JFrame
from   javax.swing import JSpinner
from   javax.swing import SpinnerDateModel

#-------------------------------------------------------------------------------
# Name: Spinner6()
# Role: Used to demonstrate how to create, and display a JSpinner instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Spinner6( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Spinner6',
            layout = FlowLayout(),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        spinner = JSpinner(
            SpinnerDateModel(
                Date( 2000,  2,  1 ),   # zero origin month
                None,                   # minimum
                None,                   # maximum
                Calendar.DAY_OF_MONTH   # Ignored by GUI
            )
        )
        spinner.setEditor(
            JSpinner.DateEditor(
                spinner,
                'dd MMM yy'
            )
        )
        frame.add( spinner )
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( Spinner6() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
