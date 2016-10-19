#-------------------------------------------------------------------------------
#    Name: SecConfigReport_02.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple wsadmin Jython script to display the results of the AdminTask
#          generateSecConfigReport() command
#    Note: This script requires a WebSphere Application Server environment.
#   Usage: wsadmin -f SecConfigReport_02.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 13/01/05  rag  0.2   Fix - Ignore the trailing (empty delimiter)
# 13/01/05  rag  0.1   New - Initial try - simple display of text data
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue

from   javax.swing import JFrame
from   javax.swing import JTable
from   javax.swing import JScrollPane

#-------------------------------------------------------------------------------
# Name: SecConfigReport_02()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class SecConfigReport_02( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'SecConfigReport_02',
            size = ( 300, 300 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        data = []
        text = AdminTask.generateSecConfigReport()
        for line in text.splitlines()[ 2: ] :
            data.append(
                [
                    info.strip() for info in
                    line[ :-2 ].split( ';' )
                ]
            )

        frame.add(
            JScrollPane(
                JTable( data, ';;;'.split( ';' ) )
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
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( SecConfigReport_02() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f SecConfigReport_02.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
