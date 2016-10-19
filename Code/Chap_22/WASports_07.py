#-------------------------------------------------------------------------------
#    Name: WASports_07.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Display information about the ports configured within a cell
#    Note: This script requires a WebSphere Application Server environment
#   Usage: wsadmin -f WASports_07.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 14/04/19  rag  0.7   Fix - Compute preferred table column widths
# 14/04/19  rag  0.6   Add - Display port number info in right pane
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

from   java.lang         import Integer
from   java.lang         import String
from   java.lang         import System

import os

from   socket            import gethostbyname

import sys

import threading

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
from   javax.swing       import JTable
from   javax.swing       import JTree
from   javax.swing       import ListSelectionModel

from   javax.swing.event import TreeSelectionListener

from   javax.swing.table import DefaultTableModel

from   javax.swing.tree  import DefaultMutableTreeNode
from   javax.swing.tree  import TreeSelectionModel

#-------------------------------------------------------------------------------
# If SwingWorker doesn't exist, we have a problem...
#-------------------------------------------------------------------------------
try :
    from javax.swing import SwingWorker
except :
    print '\nThis script requires WebSphere Application Server verison 7.0 or higher.'
    sys.exit()

#-------------------------------------------------------------------------------
# Define the Font constant to be used throughout the application
#-------------------------------------------------------------------------------
MONOFONT = Font( 'Monospaced', Font.PLAIN, 14 )

#-------------------------------------------------------------------------------
# Define the format strings used to display Cell & Node details
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
        if AdminConfig.showAttribute( x, attr ) == value
    ]

#-------------------------------------------------------------------------------
#  Name: firstNamedConfigType()
#  Role: To return the first configId of the resource of the specified Type
#        having the specified attribute value.
#  Note: Passing a scope of None is just like not specifying one.
#        Default value of attr is "name"
# Usage: ...
#        server = firstNamedConfigType( 'Server', 'server1' )
#        if server :
#          # Do something with server resource
#          ...
#        else :
#          ...
#-------------------------------------------------------------------------------
def firstNamedConfigType(
    Type, value, scope = None, attr = None
) :
    items = findScopedTypes( Type, value, scope, attr )
    if len( items ) :
        result = items[ 0 ]
    else :
        result = None
    return result

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
    # Note: data is the cellInfo object instance (see cellTree() method)
    #---------------------------------------------------------------------------
    def __init__( self, tree, pane, data ) :
        self.tree = tree
        self.pane = pane     # Reference to splitpane
        self.data = data

    #---------------------------------------------------------------------------
    # Name: valueChanged()
    # Role: TreeSelectionListener method called when a selection event occurs on
    #       the tree
    # Note: Event handlers should perform a minimum amount of processing.
    #---------------------------------------------------------------------------
    def valueChanged( self, tse ) :
        pane = self.pane
        loc  = pane.getDividerLocation()

        node = self.tree.getLastSelectedPathComponent()
        if node :
            if node.isLeaf() :
                pane.setRightComponent (
                    JScrollPane(
                      self.data.getPortTable(
                          (
                              str( node.getParent() ),
                              str( node )
                          )
                      )
                  )
                )
            else :
                pane.setRightComponent (
                    JScrollPane(
                        JLabel(
                            self.data.getInfoValue( str( node ) ),
                            font = MONOFONT
                        )
                    )
                )
        else :
            pane.setRightComponent (
                JScrollPane(
                    JLabel(
                        '<html><br/><b>Nothing selected<b/>',
                        font = MONOFONT
                    )
                )
            )
        pane.setDividerLocation( loc )

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
        pane = self.add(
                   JSplitPane(
                       JSplitPane.HORIZONTAL_SPLIT,
                       JScrollPane( tree ),
                       JScrollPane( self.status )
                   )
               )
        pane.setDividerLocation( size.width >> 1 )
        tree.addTreeSelectionListener(
            cellTSL(
                tree,
                pane,
                data
            )
        )

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
                servName = self.getName( server )
                leaf = DefaultMutableTreeNode( servName )
                #---------------------------------------------------------------
                # Add this server to the dictionary
                # Note: Server names are not guaranteed to be unique in the cell
                #---------------------------------------------------------------
                result[ ( nodeName, servName ) ] = server
                here.add( leaf )

                hostnames = getHostnames( nodeName, servName )
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
                PortLookupTask( nodeName, servName, data ).execute()

            root.add( here )

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
# Name: PortLookupTask
# Role: Background processing of potentially long running WSAS scripting object
#       calls to query the WSAS configuation to determine the port numbers that
#       are configured for a specified application server.
# Note: WebSphere Application Server (WSAS)
# Note: Instances of SwingWorker are not reusuable; new ones must be created.
#-------------------------------------------------------------------------------
class PortLookupTask( SwingWorker ) :

    #---------------------------------------------------------------------------
    # Thread lock used to synchronize calls to this class
    #---------------------------------------------------------------------------
    lock = threading.Lock()

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    # Note: This class retrieves the port information for the specified Server
    #       and updates the specified dictionary once the lookup is complete.
    #---------------------------------------------------------------------------
    def __init__(
        self,
        nodeName,
        serverName,
        data
    ) :
        self.nodeName = nodeName
        self.servName = serverName
        self.data     = data
        SwingWorker.__init__( self )

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Call the AdminConfig scripting object in the background
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        self.lock.acquire()
        try :
            pDict = self.getPorts( self.nodeName, self.servName )
            ports = pDict.keys()
            #-----------------------------------------------------------------------
            # Convert the port/endPointName dictionary to an ordered array
            # Note: The dictionary keys are numeric port number strings, so we need
            #       to sort them as integers
            #-----------------------------------------------------------------------
            ports.sort( lambda x,y: cmp( int( x ), int( y ) ) )
            result = []
            for port in ports :
                result.append( [ port, pDict[ port ] ] )

            table = JTable(
                PortTableModel( result ),
                autoResizeMode = JTable.AUTO_RESIZE_OFF,
                selectionMode = ListSelectionModel.SINGLE_SELECTION
            )
            table.getTableHeader().setReorderingAllowed( 0 )
            self.setColumnWidths( table )
            self.data.addPortTable(
                ( self.nodeName, self.servName ),
                table
            ) 
        except :
            print '\nError: %s\nvalue: %s' % sys.exc_info()[ :2 ]
        self.lock.release()

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #---------------------------------------------------------------------------
    def done( self ) :
        pass
    
    #-------------------------------------------------------------------------------
    # Name: getPorts()
    # Role: Return a dictionary, indexed by port number, of the named EndPoints for
    #       the specified server.
    #-------------------------------------------------------------------------------
    def getPorts( self, nodeName, serverName ) :
        #---------------------------------------------------------------------------
        # Use the nodeName to find it's configId
        #---------------------------------------------------------------------------
        scope = firstNamedConfigType( 'Node', nodeName  )

        #---------------------------------------------------------------------------
        # Locate the named (and optionally scoped) 'ServerEntry'
        #---------------------------------------------------------------------------
        serverEntry = firstNamedConfigType(
            'ServerEntry',
            serverName,
            scope,
            'serverName'
        )
        result = {}
        if serverEntry :
            #-----------------------------------------------------------------------
            # for each NamedEndPoint on this server...
            #-----------------------------------------------------------------------
            nEPs = AdminConfig.list(
                'NamedEndPoint',
                serverEntry
            )
            for namedEndPoint in nEPs.splitlines() :
                Name = getAttributeValue(
                    namedEndPoint,
                    'endPointName'
                )
                epId = getAttributeValue(
                    namedEndPoint,
                    'endPoint'
                )
                port = getAttributeValue( epId, 'port' )
                result[ port ] = Name
        #---------------------------------------------------------------------------
        # Return either an empty dictionary or one indexed by Port number containing
        # the associated end point names.
        #---------------------------------------------------------------------------
        return result

    #---------------------------------------------------------------------------
    # Name: setColumnWidths()
    # Role: Compute, and set the preferred column widths for the table
    # Note: We know all about the kind of table specified, so some liberties are 
    #       taken
    #---------------------------------------------------------------------------
    def setColumnWidths( self, table ) :
    
        #-----------------------------------------------------------------------
        # Variables used to access the table properties and data
        #-----------------------------------------------------------------------
        tcm    = table.getColumnModel()     # Table Column Model
        data   = table.getModel()           # To access table data
        margin = tcm.getColumnMargin()      # gap between columns

        #-----------------------------------------------------------------------
        # Preferred width of Port number column
        #-----------------------------------------------------------------------
        render = table.getCellRenderer( 0, 0 )
        comp = render.getTableCellRendererComponent(
            table,                       # table being processed
            '65535',                     # max port number
            0,                           # not selected
            0,                           # not in focus
            0,                           # row num
            0                            # col num
        )
        cWidth = comp.getPreferredSize().width

        col = tcm.getColumn( 0 )
        col.setPreferredWidth( cWidth + margin )
       
        #-----------------------------------------------------------------------
        # Compute the max width required for the data values in this column
        #-----------------------------------------------------------------------
        cWidth = -1
        for row in range( data.getRowCount() ) :
            render = table.getCellRenderer( row, 1 )
            comp = render.getTableCellRendererComponent(
                table,
                data.getValueAt( row, 1 ),   # cell value
                0,                           # not selected
                0,                           # not in focus
                row,                         # row num
                1                            # col num
            )
            cWidth = max(
                cWidth,
                comp.getPreferredSize().width
            )

        #-----------------------------------------------------------------------
        # Preferred width of "Named Endpoint" column
        #-----------------------------------------------------------------------
        col = tcm.getColumn( 1 )
        col.setPreferredWidth( cWidth + margin )

#-------------------------------------------------------------------------------
# Name: PortTableModel
# Role: Define the Table Model for the server ports
#-------------------------------------------------------------------------------
class PortTableModel( DefaultTableModel ) :

    headings = 'Port#,EndPoint Name'.split( ',' )

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    #---------------------------------------------------------------------------
    def __init__( self, data ) :
        for row in range( len( data ) ) :
            data[ row ][ 0 ] = int( data[ row ][ 0 ] )
        DefaultTableModel.__init__( self, data, self.headings )

    #---------------------------------------------------------------------------
    # Name: getColumnClass()
    # Role: Used to identify the data type for each column
    # Note: Since the port numbers need to be sorted as an Integer, and the End
    #       Point Names need to be sorted as Strings, we need to return the true
    #       class type for each column.
    #---------------------------------------------------------------------------
    def getColumnClass( self, col ) :
        if col == 0 :
            return Integer
        else :
            return String

    #---------------------------------------------------------------------------
    # Name: isCellEditable()
    # Role: Returns true (1) if the specified column is editable
    #---------------------------------------------------------------------------
    def isCellEditable( self, row, col ) :
        return col == 0

    #---------------------------------------------------------------------------
    # Name: setValueAt()
    # Role: Used to validate and change a cell value
    # Note: Only column 0 (i.e., port#) is editable!
    # Note: This depends upon the order of menu items
    #---------------------------------------------------------------------------
    def setValueAt( self, value, row, col ) :
        if 0 <= value <= 65535 :
            index = ( self, row )
            DefaultTableModel.setValueAt( self, value, row, col )
        else :
            DefaultTableModel.setValueAt(
                self,
                self.getValueAt( row, col ),
                row,
                col
            )
        self.fireTableCellUpdated( row, col )

#-------------------------------------------------------------------------------
# Name: WASports_07
# Role: Display a table of the Ports and associated End Point Names
#-------------------------------------------------------------------------------
class WASports_07( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: cellInfo
    # Role: Serialized singleton class for holding cell information
    # Note: Use an inner class to emphasize the fact that only one object exists
    #---------------------------------------------------------------------------
    class cellInfo :

        #-----------------------------------------------------------------------
        # class lock used for serialization
        #-----------------------------------------------------------------------
        lock = threading.Lock()

        #-----------------------------------------------------------------------
        # Name: __init__()
        # Role: constructor
        # Note: The index of names & info dictionaries is a node name for branch
        #       nodes, or the ( nodeName, serverName ) tuple for leaf nodes
        #-----------------------------------------------------------------------
        def __init__( self ) :
            self.names = {}            # Dictionary[ name ]  -> configId
            self.info  = {}            # Dictionary[ name ]  -> node details
            self.ports = {}            # Dictionary[ index ] -> server JTable()

        #-----------------------------------------------------------------------
        # Name: getNames()
        # Role: names getter
        #-----------------------------------------------------------------------
        def getNames( self ) :
            self.lock.acquire()
            result = self.names
            self.lock.release()
            return result

        #-----------------------------------------------------------------------
        # Name: setNames()
        # Role: names setter
        #-----------------------------------------------------------------------
        def setNames( self, names ) :
            self.lock.acquire()
            self.names = names
            self.lock.release()

        #-----------------------------------------------------------------------
        # Name: addInfoValue()
        # Role: Info value adder
        # Note: The Info text is converted into HTML format for a nicer display
        #-----------------------------------------------------------------------
        def addInfoValue( self, index, value ) :
            self.lock.acquire()
            self.info[ index ] = '<html>' + (
                value.replace(
                    '&', '&amp;'
                ).replace(
                    '<', '&lt;'
                ).replace(
                    '>', '&gt;'
                ).replace(
                    ' ', '&nbsp;'
                ).replace(
                    '\n', '<br/>'
                )
            )
            self.lock.release()

        #-----------------------------------------------------------------------
        # Name: getInfoValue()
        # Role: Info value getter
        #-----------------------------------------------------------------------
        def getInfoValue( self, index ) :
            self.lock.acquire()
            result = self.info[ index ]
            self.lock.release()
            return result

        #-----------------------------------------------------------------------
        # Name: addPortTable()
        # Role: Ports value adder
        # Note: The ports index should be a ( nodeName, serverName ) tuple
        #-----------------------------------------------------------------------
        def addPortTable( self, index, value ) :
            self.lock.acquire()
            self.ports[ index ] = value
            self.lock.release()

        #-----------------------------------------------------------------------
        # Name: getPortTable()
        # Role: Ports value getter
        # Note: The ports index should be a ( nodeName, serverName ) tuple
        #-----------------------------------------------------------------------
        def getPortTable( self, index ) :
            self.lock.acquire()
            result = self.ports[ index ]
            self.lock.release()
            return result

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
        w = screenSize.width  >> 1          # Use 1/2 screen width
        h = screenSize.height >> 1          # and 1/2 screen height
        x = ( screenSize.width  - w ) >> 1  # Top left corner of frame
        y = ( screenSize.height - h ) >> 1

        #-----------------------------------------------------------------------
        # Center the application frame in the window
        #-----------------------------------------------------------------------
        frame = self.frame = JFrame(
            'WASports_07',
            bounds = ( x, y, w, h ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        #-----------------------------------------------------------------------
        # Internal frames require us to use a JDesktopPane()
        #-----------------------------------------------------------------------
        desktop = JDesktopPane()

        cellName = AdminConfig.showAttribute(
            AdminConfig.list( 'Cell' ),
            'name'
        )
        #-----------------------------------------------------------------------
        # Create our initial internal frame, and add it to the desktop
        #-----------------------------------------------------------------------
        internal = InternalFrame(
            cellName,
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
        EventQueue.invokeLater( WASports_07() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f WASports_07.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
