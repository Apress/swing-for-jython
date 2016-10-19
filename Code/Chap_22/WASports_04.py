#-------------------------------------------------------------------------------
#    Name: WASports_04.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Display information about the ports configured within a cell
#    Note: This script requires a WebSphere Application Server environment
#   Usage: wsadmin -f WASports_04.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 14/04/19  rag  0.4   Add - Selecting a tree item updates the right pane
# 14/04/19  rag  0.3   Add - Add the cell hierarchy tree to left side
# 14/04/19  rag  0.2   Add - Add a (vertically) split pane to the internal frame
# 14/04/19  rag  0.1   Add - Display the JFrame with an empty internal frame
# 14/04/19  rag  0.0   New - Initial iteration - simply display an empty Frame
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Import the necessary Java, AWT & Swing modules
#-------------------------------------------------------------------------------
import java

from   java.awt          import Dimension
from   java.awt          import EventQueue
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
# Name: cellTSL
# Role: TreeSelectionListener for cell hierarchy tree
#-------------------------------------------------------------------------------
class cellTSL( TreeSelectionListener ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    # Note: pane is a reference to the (right) pane to be updated based upon the
    #       user selection and name2cfgId is the configId dictionary
    #---------------------------------------------------------------------------
    def __init__( self, tree, pane, name2cfgId ) :
        self.tree = tree
        self.pane = pane
        self.name2cfgId = name2cfgId

    #---------------------------------------------------------------------------
    # Name: valueChanged()
    # Role: TreeSelectionListener method called when a selection event occurs on
    #       the tree
    # Note: Event handlers should perform a minimum amount of processing.
    #---------------------------------------------------------------------------
    def valueChanged( self, tse ) :
        #-----------------------------------------------------------------------
        # Initialize the format string using HTML tags
        # Note: The only reason this isn't a single (long) line is for the book
        #-----------------------------------------------------------------------
        format = (
            '<html>&nbsp;&nbsp;node:&nbsp;%s<br/>' +
            'isLeaf:&nbsp;%s<br/>parent:&nbsp;%s'
        )
        pane = self.pane

        node = self.tree.getLastSelectedPathComponent()
        if node :
            text = format % (
                node,
                [ 'No', 'Yes' ][ node.isLeaf() ],
                node.getParent()
            )
            if node.isLeaf() :
                key = ( str( node.getParent() ), str( node ) )
            else :
                key = node.toString()
            if self.name2cfgId.has_key( key ) :
                text += '<br/><br/>%s' % self.name2cfgId[ key ]
            else :
                text += '<br/><br/> key missing: %s' % key
        else :
            text = 'Nothing selected'
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
    def __init__( self, title, size, location, closable = 0 ) :
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
        tree, self.name2cfgId = self.cellTree()
        tree.getSelectionModel().setSelectionMode(
            TreeSelectionModel.SINGLE_TREE_SELECTION
        )
#       print self.name2cfgId
        self.status = JLabel( 'Right' )
        tree.addTreeSelectionListener(
            cellTSL(
                tree,
                self.status,
                self.name2cfgId
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
    def cellTree( self ) :
        #-----------------------------------------------------------------------
        # Use the cellName as the tree root node
        #-----------------------------------------------------------------------
        cell = AdminConfig.list( 'Cell' )
        cellName = self.getName( cell )
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

        return JTree( root ), result

    #---------------------------------------------------------------------------
    # Name: getName()
    # Role: Return the name attribute value from the specified configId
    # Note: This "hides" java.awt.Component.getName()
    #---------------------------------------------------------------------------
    def getName( self, configId ) :
        return AdminConfig.showAttribute( configId, 'name' )

#-------------------------------------------------------------------------------
# Name: WASports_04
# Role: Display a table of the Ports and associated End Point Names
#-------------------------------------------------------------------------------
class WASports_04( java.lang.Runnable ) :

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
            'WASports_04',
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
            size = Dimension( w >> 1, h >> 1 ),
            location = Point( 5, 5 )
        )
        desktop.add( internal )

        frame.setContentPane( desktop )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
# Role: main entry point - verify that the script was executed, not imported.
#-------------------------------------------------------------------------------
if __name__ == '__main__' :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( WASports_04() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f WASports_04.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
