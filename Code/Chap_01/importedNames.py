#-------------------------------------------------------------------------------
#    Name: importedNames.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Demonstrate the use of simplified class names and the Swing
#          Event Dispatch Thread instantiation of the application class
#   Usage: C:\IBM\WebSphere\AppServer\bin\wsadmin -f importedNames.py
#            or
#          C:\jython2.5.3\bin\jython importedNames.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/20  rag  0.0  New
#-------------------------------------------------------------------------------
from java.lang   import Runnable
from java.awt    import EventQueue
from javax.swing import JFrame
import sys

#-------------------------------------------------------------------------------
# Name: myFrame
# Role: Example Swing class using imported name references
#-------------------------------------------------------------------------------
class myFrame :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: class constructor - used to instantiate and
    #       display a simple (empty) application frame
    #---------------------------------------------------------------------------
    def __init__( self ) :
        frame = JFrame( 
            'importedNames.py',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE,
            visible = 1
        )

#-------------------------------------------------------------------------------
# Name: Runnable
# Role: Define a Runnable class used to instantiate the
#       specified user class
#-------------------------------------------------------------------------------
class Runnable( Runnable ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: class constructor
    #---------------------------------------------------------------------------
    def __init__( self, fun ) :
        self.runner = fun

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Invoked on Event Dispatch thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.runner()

#-------------------------------------------------------------------------------
# Name: anonymous
# Role: Script entry point - verify that the script was executed
#       and not imported.  If so, instantiate the application on
#       the event dispatch thread via invokeLater() method call.
#-------------------------------------------------------------------------------
if __name__ == '__main__' :
    EventQueue.invokeLater( Runnable( myFrame ) )
    if 'AdminConfig' in dir() :
        #-----------------------------------------------------------------------
        # If executed using wsadmin, pressing <Enter> will terminate the script
        # C:\IBM\WebSphere\AppServer\bin\wsadmin -f importedNames.py
        #-----------------------------------------------------------------------
        raw_input( 'Press <Enter> to terminate the application: ' )
else :
    print 'Error - This script should be executed, not imported'
    if 'JYTHON_JAR' in dir( sys ) :
        print '\nUsage: jython %s.py' % __name__
    else :
        print '\nUsage: wsadmin -conntype none -f %s.py' % __name__
