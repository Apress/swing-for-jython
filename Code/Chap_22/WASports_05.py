#-------------------------------------------------------------------------------
#    Name: WASports_05.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Display information about the ports configured within a cell
#    Note: This script requires a WebSphere Application Server environment
#   Usage: wsadmin -f WASports_05.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 14/04/19  rag  0.5   Add - Display cell & node info when selected
# 14/04/19  rag  0.4   Add - Selecting a tree item updates the right pane
# 14/04/19  rag  0.3   Add - Add the cell hierarchy tree to left side
# 14/04/19  rag  0.2   Add - Add a (vertically) split pane to the internal frame
# 14/04/19  rag  0.1   Add - Display the JFrame with an empty internal frame
# 14/04/19  rag  0.0   New - Initial iteration - simply display an empty Frame
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Import the necessary Java, AWT, Swing, & Python modules
#-------------------------------------------------------------------------------
import java

from   java.lang         import System

import os

from   socket            import gethostbyname

from   java.awt          import Dimension
from   java.awt          import EventQueue
from   java.awt          import Font
from   java.awt          import Point
from   java.awt          import Toolkit

from   javax.swing       import JDesktopPane
from   javax.swing       import JFrame
from   javax.swing       import JLabel
from   javax.swing       import JInternalFrame
from   javax.swing       import JScrollPane
from   javax.swing       import JSplitPane
from   javax.swing       import JTree

from   javax.swing.event import TreeSelectionListener

from   javax.swing.tree  import DefaultMutableTreeNode
from   javax.swing.tree  import TreeSelectionModel

#-------------------------------------------------------------------------------
# Define the Font constant to be used throughout the application
#-------------------------------------------------------------------------------
MONOFONT = Font( 'Monospaced', Font.PLAIN, 14 )

#-------------------------------------------------------------------------------
# Define the format strings used to display Cell, Node, server information
#-------------------------------------------------------------------------------
CELLINFO = '''
    Cell: %s
    Home: %s
 Version: %s
 Profile: %s
'''

NODEINFO = '''
    Cell: %s
    Node: %s
    Home: %s
 Version: %s
 Profile: %s
Hostname: %s
 IP addr: %s
'''

leafFormatString = (
    '<html>\nParent: %s\n  Node: %s'
).replace( '\n', '<br/>' ).replace( ' ', '&nbsp;' )

#-------------------------------------------------------------------------------
#  Name: findScopedTypes()
#  Role: Return the list of configuration IDs for resources of the specified
#        type having a given attribute value, within an optional scope.
#  Note: Passing a scope of None is just like not specifying one.
#      - Default attr value is "name"
# Usage: # Find all servers having a name of "server1"
#        servers = findScopedTypes( 'Server', 'server1' )
#-------------------------------------------------------------------------------
def findScopedTypes( Type, value, scope = None, attr = None ) :
    if not attr :
        attr = 'name'
    return [
        x for x in AdminConfig.list( Type, scope ).splitlines()
        if getAttributeValue( x, attr ) == value
    ]

#-------------------------------------------------------------------------------
# Name: getAttributeValue()
# Role: Return the specified attribute value from the given configuration object
# Note: cfgId = configuration ID for configuration object
#       name  = the attribute name to be returned
#-------------------------------------------------------------------------------
def getAttributeValue( cfgId, attr  ) :
    return AdminConfig.showAttribute( cfgId, attr )

#-------------------------------------------------------------------------------
# Name: getIPaddresses( hostnames )
# Role: Return the list of unique IP addresses for the specified hostnames
# Note: The list of hostnames may include aliases.  The result will contain the
#       list of unique IP addresses without duplicates.
#-------------------------------------------------------------------------------
def getIPaddresses( hostnames ) :
    result = []
    for hostname in hostnames :
        try :
            addr = gethostbyname( hostname )
            if addr not in result :
                result.extend( addr.split( ',' ) )
        except :
            pass
    return result

#-------------------------------------------------------------------------------
# Name: getHostnames( nodeName, serverName )
# Role: Return the list of hostnames configured for the specified server
# Note: exclude identifies the hostnames & ip addresses to be ignored
# Note: 232.133.104.73 == Node agent IPv4 multicast address
#       ff01::1        == Node agent IPv6 multicase address
#-------------------------------------------------------------------------------
def getHostnames( nodeName, serverName ) :
    exclude = [
        '*',
        'localhost',
        '${LOCALHOST_NAME}',
        '232.133.104.73',
        'ff01::1'
    ]
    result = []
    node   = findScopedTypes( 'Node', nodeName )[ 0 ]
    server = findScopedTypes(
        'ServerEntry',
        serverName,
        node,
        'serverName'
    )[ 0 ]
    NEPs = AdminConfig.list( 'NamedEndPoint', server )
    for nep in NEPs.splitlines() :
        epId = getAttributeValue( nep, 'endPoint' )
        host = getAttributeValue( epId, 'host' )
        if host not in exclude :
            result.append( host )
            exclude.append( host )
    return result

#-------------------------------------------------------------------------------
# Name: WASversion()
# Role: Return the version of WebSphere for the specified id, which should be
#       either a Node, or Cell configId
#-------------------------------------------------------------------------------
def WASversion( id ) :
    if AdminConfig.getObjectType( id ) == 'Cell' :
        nodeName = System.getProperty( 'local.node' )
    else :
        nodeName = getAttributeValue( id, 'name' )
    return AdminTask.getNodeBaseProductVersion(
        '[-nodeName %s]' % nodeName
    )

#-------------------------------------------------------------------------------
# Name: WASprofileName()
# Role: Return the name of the current profile, or None
#-------------------------------------------------------------------------------
def WASprofileName( id ) :
    result = WASvarLookup( id, 'USER_INSTALL_ROOT' )
    if result :
        result = result.split( os.sep )[ -1 ]
    return result

#-------------------------------------------------------------------------------
# Name: WAShome()
# Role: Return the value of the WAS_INSTALL_ROOT variable, or None
#-------------------------------------------------------------------------------
def WAShome( id ) :
    return WASvarLookup( id, 'WAS_INSTALL_ROOT' )

#-------------------------------------------------------------------------------
# Name: WASvarLookup()
# Role: Return the specified value of the indicated WAS variable
#-------------------------------------------------------------------------------
def WASvarLookup( id, name ) :
    VSE = AdminConfig.list( 'VariableSubstitutionEntry', id )
    for var in VSE.splitlines () :
        if getAttributeValue( var, 'symbolicName' ) == name :
            result = getAttributeValue( var, 'value' )
            break
    else :
        result = None
    return result

#-------------------------------------------------------------------------------
# Name: cellTSL
# Role: TreeSelectionListener for cell hierarchy tree
#-------------------------------------------------------------------------------
class cellTSL( TreeSelectionListener ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    # Note: pane is a reference to the (right) pane to be updated based upon the
    #       user selection
    #     - data is a reference to the singleton cellInfo class instance
    #---------------------------------------------------------------------------
    def __init__( self, tree, pane, data ) :
        self.tree = tree
        self.pane = pane
        self.data = data

    #---------------------------------------------------------------------------
    # Name: valueChanged()
    # Role: TreeSelectionListener method called when a selection event occurs on
    #       the tree
    # Note: Event handlers should perform a minimum amount of processing.
    #---------------------------------------------------------------------------
    def valueChanged( self, tse ) :
        pane = self.pane
        node = self.tree.getLastSelectedPathComponent()
        if node :
            if node.isLeaf() :
                text = leafFormatString % (
                    node.getParent(),
                    node
                )
            else :
                text = self.data.getInfoValue( node.toString() )
        else :
            text = '<html><br/><b>Nothing selected<b/>'
        pane.setText( text )

#-------------------------------------------------------------------------------
# Name: InternalFrame
# Role: Provide a class for our internal frames
#-------------------------------------------------------------------------------
class InternalFrame( JInternalFrame ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    #---------------------------------------------------------------------------
    def __init__(
        self, title, size, location, data, closable = 0
    ) :
        JInternalFrame.__init__(
            self,
            title,
            resizable   = 1,
            closable    = closable,
            maximizable = 1,
            iconifiable = 1,
            size        = size
        )
        self.setLocation( location )

        #-----------------------------------------------------------------------
        # Create the JTree, with only 1 item selectable
        # Note: Secondary value is a dictionary
        #-----------------------------------------------------------------------
        tree = self.cellTree( data )
        tree.getSelectionModel().setSelectionMode(
            TreeSelectionModel.SINGLE_TREE_SELECTION
        )

        self.status = JLabel(
            'Nothing selected',
            font = MONOFONT
        )
        tree.addTreeSelectionListener(
            cellTSL(
                tree,
                self.status,
                data
            )
        )
        pane = self.add(
            JSplitPane(
                JSplitPane.HORIZONTAL_SPLIT,
                JScrollPane( tree ),
                JScrollPane( self.status )
            )
        )
        pane.setDividerLocation( size.width >> 1 )

        self.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: cellTree()
    # Role: create a tree representation of the WebSphere cell hierarchy
    #---------------------------------------------------------------------------
    def cellTree( self, data ) :

        #-----------------------------------------------------------------------
        # Use the cellName as the tree root node
        #-----------------------------------------------------------------------
        cell = AdminConfig.list( 'Cell' )
        cellName = self.getName( cell )

        #-----------------------------------------------------------------------
        # Note: data is the one and only instance of the inner cellInfo class
        #-----------------------------------------------------------------------
        data.addInfoValue(
            cellName,
            CELLINFO % (
                cellName,
                WAShome( cell ),
                WASversion( cell ),
                WASprofileName( cell )
            )
        )

        root = DefaultMutableTreeNode( cellName )

        #-----------------------------------------------------------------------
        # Build an item name to configId dictionary
        #-----------------------------------------------------------------------
        result = { cellName : cell }

        #-----------------------------------------------------------------------
        # Use the node name for the branches
        #-----------------------------------------------------------------------
        for node in AdminConfig.list( 'Node' ).splitlines() :
            nodeName = self.getName( node )
            here = DefaultMutableTreeNode(
                nodeName
            )

            #-------------------------------------------------------------------
            # Add this node to the dictionary
            #-------------------------------------------------------------------
            result[ nodeName ] = node
            #-------------------------------------------------------------------
            # and the server name for each leaf
            #-------------------------------------------------------------------
            servers = AdminConfig.list( 'Server', node )
            for server in servers.splitlines() :
                name = self.getName( server )
                leaf = DefaultMutableTreeNode( name )
                #---------------------------------------------------------------
                # Add this server to the dictionary
                # Note: Server names are not guaranteed to be unique in the cell
                #---------------------------------------------------------------
                result[ ( nodeName, name ) ] = server
                here.add( leaf )
            root.add( here )

            hostnames = getHostnames( nodeName, name )
            ipaddr    = getIPaddresses( hostnames )

            data.addInfoValue(
                nodeName,
                NODEINFO % (
                    cellName,
                    nodeName,
                    WAShome( node ),
                    WASversion( node ),
                    WASprofileName( node ),
                    ', '.join( hostnames ),
                    ', '.join( ipaddr )
                )
            )

        #-----------------------------------------------------------------------
        # Note: data is the one and only instance of the inner cellInfo class
        #-----------------------------------------------------------------------
        data.setNames( result )

        return JTree( root )

    #---------------------------------------------------------------------------
    # Name: getName()
    # Role: Return the name attribute value from the specified configId
    # Note: This "hides" java.awt.Component.getName()
    #---------------------------------------------------------------------------
    def getName( self, configId ) :
        return getAttributeValue( configId, 'name' )

#-------------------------------------------------------------------------------
# Name: WASports_05
# Role: Display a table of the Ports and associated End Point Names
#-------------------------------------------------------------------------------
class WASports_05( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: cellInfo
    # Role: Serialized singleton class for holding cell information
    # Note: Use an inner class to emphasize the fact that only one object exists
    #---------------------------------------------------------------------------
    class cellInfo :

        #-----------------------------------------------------------------------
        # Name: __init__()
        # Role: constructor
        # Note: The index of names & info dictionaries is a node name for branch
        #       nodes, or the ( nodeName, serverName ) tuple for leaf nodes
        #-----------------------------------------------------------------------
        def __init__( self ) :
            self.names = {}       # Dict[ name ] -> configId
            self.info  = {}       # Dict[ name ] -> node info

        #-----------------------------------------------------------------------
        # Name: getNames()
        # Role: names getter
        #-----------------------------------------------------------------------
        def getNames( self ) :
            return self.names

        #-----------------------------------------------------------------------
        # Name: setNames()
        # Role: names setter
        #-----------------------------------------------------------------------
        def setNames( self, names ) :
            self.names = names

        #-----------------------------------------------------------------------
        # Name: addInfoValue()
        # Role: Info value adder
        #-----------------------------------------------------------------------
        def addInfoValue( self, index, value ) :
            self.info[ index ] = '<html>' + (
                value.replace( '&', '&amp;' ).replace( '<',
                '&lt;' ).replace( '>', '&gt;' ).replace( ' ',
                '&nbsp;' ).replace( '\n', '<br/>' )
            )

        #-----------------------------------------------------------------------
        # Name: getInfoValue()
        # Role: Info value getter
        #-----------------------------------------------------------------------
        def getInfoValue( self, index ) :
            return self.info[ index ]

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        self.cellData = self.cellInfo()

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Called by Swing Event Dispatcher thread
    #---------------------------------------------------------------------------
    def run( self ) :

        #-----------------------------------------------------------------------
        # Starting width, height & location of the application frame
        #-----------------------------------------------------------------------
        screenSize = Toolkit.getDefaultToolkit().getScreenSize()
        w = screenSize.width  >> 1          # 1/2 screen width
        h = screenSize.height >> 1          # 1/2 screen height
        x = ( screenSize.width  - w ) >> 1  # Top left corner
        y = ( screenSize.height - h ) >> 1  #   of app frame

        #-----------------------------------------------------------------------
        # Center the application frame in the window
        #-----------------------------------------------------------------------
        frame = self.frame = JFrame(
            'WASports_05',
            bounds = ( x, y, w, h ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        #-----------------------------------------------------------------------
        # Internal frames require us to use a JDesktopPane()
        #-----------------------------------------------------------------------
        desktop = JDesktopPane()

        #-----------------------------------------------------------------------
        # Create our initial internal frame, and add it to the desktop
        #-----------------------------------------------------------------------
        internal = InternalFrame(
            'InternalFrame',
            Dimension( w >> 1, h >> 1 ),
            Point( 5, 5 ),
            self.cellData
        )
        desktop.add( internal )

        frame.setContentPane( desktop )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
# Role: main entry point - verify that the script was executed, not imported.
#-------------------------------------------------------------------------------
if __name__ == '__main__' :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( WASports_05() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f WASports_05.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
