#-------------------------------------------------------------------------------
#    Name: ListPorts.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: wsadmin script used to display the configured port numbers for the
#          current WebSphere Application Server cell
#    Note: A WebSphere Application Server environment is required.
#          This script does not use the Swing classes.
#   Usage: wsadmin -f ListPorts.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/11/05  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import re, sys

#-------------------------------------------------------------------------------
# Format string used to display server details above the port number list
#-------------------------------------------------------------------------------
formatString  = '''
Profile name: %(profName)s
Host name(s): %(hosts)s
   Node name: %(nodeName)s
 Server name: %(servName)s\n
 Port | EndPoint Name
------+--------------'''

#-------------------------------------------------------------------------------
# Name: getHostnames( serverEntry )
# Role: Return the list of hostnames (and possibly IP addresses) configured for
#       a given ServerEntry object
# Note: exclude identifies the hostnames & ip addresses to be ignored
#       232.133.104.73 == Default IPv4 multicast host address for node agents
#       ff01::1        == Default IPv6 multicast host address for node agents
#-------------------------------------------------------------------------------
def getHostnames( serverEntry ) :
    exclude = [
        '*',
        'localhost',
        '${LOCALHOST_NAME}',
        '232.133.104.73',
        'ff01::1'
    ]
    result = []
    for nep in AdminConfig.list(
        'NamedEndPoint',
        serverEntry
    ).splitlines() :
        epId = getAttributeValue( nep, 'endPoint' )
        host = getAttributeValue( epId, 'host' )
        if host not in exclude :
            result.append( host )
            exclude.append( host )
    return result

#-------------------------------------------------------------------------------
# Name: profileName()
# Role: Return the name of the current profile, or '<unknown>'
# Note: nodeID is the configuration ID for the current node
#       A RegExp is used to split() because Managed nodes could be on any OS type.
#-------------------------------------------------------------------------------
def profileName( nodeID ) :
    for var in AdminConfig.list(
        'VariableSubstitutionEntry',
        nodeID
    ).splitlines () :
        if getAttributeValue( var, 'symbolicName'
        ) == 'USER_INSTALL_ROOT' :
            return re.split(
                '[\\\/]',
                getAttributeValue( var, 'value' )
            )[ -1 ]
    return '<unknown>'

#-------------------------------------------------------------------------------
# Name: getAttributeValue()
# Role: Return the specified attribute value from the given configuration object
# Note: cfgId = configuration ID for configuration object
#       name  = the attribute name to be returned
#-------------------------------------------------------------------------------
def getAttributeValue( cfgId, attr  ) :
    return AdminConfig.showAttribute( cfgId, attr )

#-------------------------------------------------------------------------------
# Name: ListPorts()
# Role: Display the Port Numbers configured for each configured server
# Note: The information will be sorted (numerically) by port number
#-------------------------------------------------------------------------------
def ListPorts() :
    gAV = getAttributeValue  # For line shortening purposes
    #---------------------------------------------------------------------------
    # names == dictionary holding values displayed using formatString (above)
    #---------------------------------------------------------------------------
    names = {}
    nodes = 0
    for node in AdminConfig.list( 'Node' ).splitlines() :
        nodes += 1
        names[ 'nodeName' ] = gAV( node, 'name' )
        names[ 'profName' ] = profileName( node )
        SEs = AdminConfig.list( 'ServerEntry', node )
        servers = 0
        for se in SEs.splitlines() :
            servers += 1
            names[ 'servName' ] = gAV( se, 'serverName' )
            names[ 'hosts' ] = ', '.join( getHostnames( se ) )
            print formatString % names
            data = []
            NEPs = AdminConfig.list( 'NamedEndPoint', se )
            for nep in NEPs.splitlines() :
                name = gAV( nep, 'endPointName' )
                epId = gAV( nep, 'endPoint' )
                port = gAV( epId, 'port' )
                data.append( ( port, name ) )

            #-------------------------------------------------------------------
            # Numeric sort using endpoint name
            #-------------------------------------------------------------------
            data.sort( lambda a, b : cmp( a[ 1 ], b[ 1 ] ) )
            for port, name in data :
                print '%5d | %s' % ( port, name )
            print
        else :
            if servers == 0 :
                print 'Error: No "Server" entries found in Node:', names[ 'nodeName' ]
    else :
        if nodes == 0 :
            print 'Error: No "Node" entries found.'

#-------------------------------------------------------------------------------
# Name: anonymous
# Role: main entry point - this is where the script execution "begins"
# Note: Verify that the script was executed, not imported.
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        ListPorts()
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f ListPorts.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
