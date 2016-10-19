#-------------------------------------------------------------------------------
#    Name: consoleTimeout1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample wsadmin Jython script that allow the user to view / modify the
#          Admin console inactivity timeout value
# Warning: This particular example does not use the best practice of calling the
#          wsadmin scripting object using a separate thread.
#   Usage: wsadmin -f consoleTimeout1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import re
import sys

from   java.awt    import EventQueue
from   java.awt    import FlowLayout

from   javax.swing import BoxLayout
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JPanel
from   javax.swing import JTextField

#-------------------------------------------------------------------------------
# Name: getTimeout()
# Role: Return the initial / current admin console timeout value, if possible.
#       If not, return None
# Note: AdminConfig scripting object must exist
#-------------------------------------------------------------------------------
def getTimeout() :
    dep = AdminConfig.getid( '/Deployment:isclite/' )
    if not dep :
        timeout = None
    else :
        #-----------------------------------------------------------------------
        # To manipulate the AdminConsole app we need to locate the Application-
        # Deployment object associated with the app, and the ApplicationConfig
        # object associated with the ApplicationDeployment object. If no
        # ApplicationConfig object exists, we will create one.
        #-----------------------------------------------------------------------
        appDep    = AdminConfig.list( 'ApplicationDeployment', dep )
        appConfig = AdminConfig.list( 'ApplicationConfig', appDep )
        if not appConfig :
            appConfig = AdminConfig.create( 'ApplicationConfig', appDep, [] )

        #-----------------------------------------------------------------------
        # Does a SessionManager exist?  If not, create one
        # Note: Save a reference to it (sesMgmt) in the application
        #-----------------------------------------------------------------------
        sesMgmt = AdminConfig.list( 'SessionManager', appDep )
        if not sesMgmt :
            sesMgmt = AdminConfig.create( 'SessionManager', appConfig, [] )

        #-----------------------------------------------------------------------
        # Get the tuningParams config ID, if one exists.
        # Note: Save a reference to it (tuningParms) in the application
        #-----------------------------------------------------------------------
        tuningParms = AdminConfig.showAttribute( sesMgmt, 'tuningParams' )
        if not tuningParms :
            timeout = None
            print "Error: tuningParams object doesn't exist."
        else :
            timeout = AdminConfig.showAttribute(
                tuningParms,
                'invalidationTimeout'
            )
    return timeout 

#-------------------------------------------------------------------------------
# Name: setTimeout()
# Role: Attempt to modify the Admin console inactivity timeout value.
#       A message is returned indicating the success, or failure
# Note: AdminConfig scripting object must exist
#-------------------------------------------------------------------------------
def setTimeout( value ) :
    dep = AdminConfig.getid( '/Deployment:isclite/' )
    if not dep :
        result = 'Deployment object not found: isclite'
    else :
        #-----------------------------------------------------------------------
        # To manipulate the AdminConsole app we need to locate the Application-
        # Deployment object associated with the app, and the ApplicationConfig
        # object associated with the ApplicationDeployment object. If no
        # ApplicationConfig object exists, we may create one.
        #-----------------------------------------------------------------------
        appDep    = AdminConfig.list( 'ApplicationDeployment', dep )
        appConfig = AdminConfig.list( 'ApplicationConfig', appDep )
        if not appConfig :
            appConfig = AdminConfig.create( 'ApplicationConfig', appDep, [] )

        #-----------------------------------------------------------------------
        # Does a SessionManager exist?  If not, create one
        #-----------------------------------------------------------------------
        sesMgmt = AdminConfig.list( 'SessionManager', appDep )
        if not sesMgmt :
            sesMgmt = AdminConfig.create( 'SessionManager', appConfig, [] )

        #-----------------------------------------------------------------------
        # Get the tuningParams config ID, if one exists.
        # Note: Save a reference to it (tuningParms) in the application
        #-----------------------------------------------------------------------
        tuningParms = AdminConfig.showAttribute( sesMgmt, 'tuningParams' )
        if not tuningParms :
            timeout = None
            result = "Error: tuningParams object doesn't exist."
        else :
            AdminConfig.modify(
                                tuningParms,
                                [[ 'invalidationTimeout', value ]]
                              )
            AdminConfig.save()
            result = 'Update successful.'
    return result

#-------------------------------------------------------------------------------
# Name: consoleTimeout1()
# Role: Create, and display our simple application
#-------------------------------------------------------------------------------
class consoleTimeout1( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Build and display our graphical application
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'Console timeout',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        #-----------------------------------------------------------------------
        # The frame (i.e., it's ContentPane) should use a vertically aligned
        # BoxLayout layout manager (i.e., along the Y_AXIS)
        #-----------------------------------------------------------------------
        cp = frame.getContentPane()
        cp.setLayout( BoxLayout( cp, BoxLayout.Y_AXIS ) )

        #-----------------------------------------------------------------------
        # The JTextField will be preceeded, and followed by JLabel components
        # identifying the value being displayed, and the associated time units.
        # However, we want them displayed horizontally, so we put them into a
        # single JPanel instance using a FlowLayout layout manager
        #-----------------------------------------------------------------------
        input = JPanel( layout = FlowLayout() )
        input.add( JLabel( 'Timeout:' ) )
        self.text = JTextField( 3, actionPerformed = self.update )
        input.add( self.text )
        self.text.setText( getTimeout() )
        input.add( JLabel( 'minutes' ) )
        cp.add( input )

        #-----------------------------------------------------------------------
        # Then, we add a message area beneath
        #-----------------------------------------------------------------------
        self.msg  = cp.add( JLabel() )

        frame.setSize( 290, 100 )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: update()
    # Role: TextField event handler - invoked when user presses <Enter>
    #---------------------------------------------------------------------------
    def update( self, event ) :
        value = self.text.getText().strip()
        if re.search( '^\d+$', value ) :
            self.msg.setText( setTimeout( value ) )
        else :
            msg = 'Invalid value "%s" ignored.' % value
            self.msg.setText( msg )
            self.text.setText( getTimeout() )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in globals().keys() :
        EventQueue.invokeLater( consoleTimeout1() )
        raw_input( '\nPress <Enter> to terminate the application: ' )
    else :
        print '\nError: This script requires a WebSphere Application Server.\n'
        print 'Usage: wsadmin -f consoleTimeout1.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()