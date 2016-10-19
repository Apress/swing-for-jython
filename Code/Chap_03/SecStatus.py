#-------------------------------------------------------------------------------
#    Name: SecStatus.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: A sample wsadmin script used to display the global security status
#    Note: This script requires a WebSphere Application Server environment
#   Usage: wsadmin -f SecStatus.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt    import EventQueue
from   javax.swing import JFrame
from   javax.swing import JLabel

#-------------------------------------------------------------------------------
# Name: SecStatus()
# Role: Used to display the WebSphere Application Server Global Security Status
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class SecStatus( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame( 'Global Security' )
        frame.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE )
        security = AdminConfig.list( 'Security' )
        status = AdminConfig.showAttribute( security, 'enabled' )
        frame.add( JLabel( 'Security enabled: ' + status ) )
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( SecStatus() )
        raw_input( '\nPress <Enter> to terminate the application: ' )
    else :
        print 'Error: This script must be executed by the WebSphere Application'
        print '       Server wsadmin utility.\n'
        print 'wsadmin -f SecStatus.py'
else :
    print 'Error: This script should be executed, not imported.\n'
    if 'JYTHON_JAR' in dir( sys ) :
        print 'Error: This script must be executed by the WebSphere Application'
        print '       Server wsadmin utility.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()