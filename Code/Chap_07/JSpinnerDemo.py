#-------------------------------------------------------------------------------
#    Name: JSpinnerDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing how a JSpinner may be used.
#   Usage: wsadmin -f JSpinnerDemo.py
#            or
#          jython JSpinnerDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   java.awt    import FlowLayout
from   java.text   import DateFormatSymbols as DFS
from   javax.swing import JFormattedTextField
from   javax.swing import JFrame
from   javax.swing import JSpinner
from   javax.swing import SpinnerListModel

#-------------------------------------------------------------------------------
# Name: JSpinnerDemo()
# Role: Used to demonstrate how to create, and display a JSpinner instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class JSpinnerDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'JSpinnerDemo',
            layout = FlowLayout(),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        daysOfWeek = [ dow for dow in DFS().getWeekdays() if dow ]
        width = max( [ len( dow ) for dow in daysOfWeek ] )
        spinner = JSpinner( SpinnerListModel( daysOfWeek ) )
        spinner.getEditor().getTextField().setColumns( width )
        frame.add( spinner )
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( JSpinnerDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
