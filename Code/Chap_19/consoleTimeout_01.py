#-------------------------------------------------------------------------------
#    Name: consoleTimeout_01.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample wsadmin Jython script to display and modify the Admin console
#          inactivity timeout value.
#    Note: This script requires a WebSphere Application Server environment and
#          is based upon the Jacl script in the online documentation and does
#          not use Swing.
#    Long: http://publib.boulder.ibm.com/infocenter/wasinfo/v7r0/index.jsp?
#          topic=/com.ibm.websphere.nd.doc/info/ae/isc/cons_sessionto.html
#   Short: http://goo.gl/GvZOj
#   Usage: wsadmin -f consoleTimeout_01.py [value]
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/30  rag  0.0  New - ...
#-------------------------------------------------------------------------------
'''
Command: %(cmdName)s\n
Purpose: WebSphere (wsadmin) script used to display, or modify the Admin Console
         timeout value.\n
  Usage: wsadmin %(cmdName)s [value]\n
Where:
  value = An optional numeric value representing the number of minutes of
          inactivity that are allowed.  If no value is specified, the current
          Timeout value is displayed.\n
Examples:
  wsadmin -f %(cmdName)s.py\n
  ./wsadmin.sh -f %(cmdName)s.py 30
'''
#-------------------------------------------------------------------------------
# Import the Regular Express (RegExp) and system modules
#-------------------------------------------------------------------------------
import re, sys

#-------------------------------------------------------------------------------
# Define the global message strings
#-------------------------------------------------------------------------------
nonNumeric = '%(cmdName)s: Invalid numeric value specified: %(value)s'
noISCLite  = '%(cmdName)s: The AdminConsole application has not been deployed.'
noTPobj    = "%(cmdName)s: tuningParams object doesn't exist."
currentVal = '%(cmdName)s: Current Timeout = %(timeout)d minutes.'
saveConfig = '%(cmdName)s: Saving configuration changes.'

#-------------------------------------------------------------------------------
# Name: Usage()
# Role: Display script usage information, and exit (terminate script)
#-------------------------------------------------------------------------------
def Usage( cmdName ):
    print __doc__ % locals()
    sys.exit( 1 )

#-------------------------------------------------------------------------------
# Name: consoleTimeout_01()
# Role: Function used to display, or modify the Admin console timeout value
#-------------------------------------------------------------------------------
def consoleTimeout_01( cmdName = 'consoleTimeout_01' ) :
    argc = len( sys.argv )                  # Number of args
    if argc > 1 :                           # Too many?
        Usage( cmdName )                    #   show Usage info

    value = None
    if argc == 1 :
        value = sys.argv[ 0 ]
        if not re.search( re.compile( '^\d+$' ), value ) :
            print nonNumeric % locals()
            Usage( cmdName )

    #---------------------------------------------------------------------------
    # Has the AdminConsole application been deployed?
    #---------------------------------------------------------------------------
    dep = AdminConfig.getid( '/Deployment:isclite/' )
    if not dep :
        print noISCLite % locals()
        Usage( cmdName )

    #---------------------------------------------------------------------------
    # To manipulate the AdminConsole application we need to locate the
    # ApplicationDeployment object associated with the AdminConsole Application,
    # and the ApplicationConfig object associated with the Application.  If no
    # ApplicationConfig object exists, create one.
    #---------------------------------------------------------------------------
    appDep    = AdminConfig.list( 'ApplicationDeployment', dep )
    appConfig = AdminConfig.list( 'ApplicationConfig', appDep )
    if not appConfig :
        appConfig = AdminConfig.create(
            'ApplicationConfig',
            appDep,
            []
        )

    #-------------------------------------------------------------------
    # Does a SessionManager exist?  If not, create one.
    #-------------------------------------------------------------------
    sesMgmt = AdminConfig.list( 'SessionManager', appDep )
    if not sesMgmt :
        sesMgmt = AdminConfig.create(
            'SessionManager',
            appConfig,
            []
        )

    #-------------------------------------------------------------------
    # Get the tuningParams config ID, if one exists.
    #-------------------------------------------------------------------
    tuningParams = AdminConfig.showAttribute(
        sesMgmt,
        'tuningParams'
    )
    if value :
        if not tuningParams :
            AdminConfig.create(
                'TuningParams',
                sesMgmt,
                [[ 'invalidationTimeout', value ]]
            )
        else :
            AdminConfig.modify(
                tuningParams,
                [[ 'invalidationTimeout', value ]]
            )
    else :
        if not tuningParams :
            print noTPobj % locals()
        else :
            timeout = AdminConfig.showAttribute(
                tuningParams,
                'invalidationTimeout'
            )
            print currentVal % locals()

    if AdminConfig.hasChanges() :
        print saveConfig % locals()
        AdminConfig.save()
    
#-------------------------------------------------------------------------------
# Role: main entry point
# Note: Verify the script was executed, not imported.
#-------------------------------------------------------------------------------
if __name__ == '__main__' :
    if 'AdminConfig' in dir() :
        consoleTimeout_01()
    else :
        print '\n  Error: A WebSphere Application Server environment is required.'
        Usage( 'consoleTimeout_01' )
else :
    print '\n  Error: This script should be executed, not imported.'
    Usage( __name__ )