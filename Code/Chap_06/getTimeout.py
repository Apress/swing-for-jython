#-------------------------------------------------------------------------------
#    Name: getTimeout.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample wsadmin Jython function that returns the current admin console
#          inactivity timeout value, or None.
#    Note: The AdminConfig scripting object must exist
#   Usage: wsadmin -f getTimeout.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
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
