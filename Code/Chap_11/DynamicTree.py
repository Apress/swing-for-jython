#-------------------------------------------------------------------------------
#    Name: DynamicTree.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script showing how to monitor an editable tree
#   Usage: wsadmin -f DynamicTree.py
#            or
#          jython DynamicTree.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/25  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt          import BorderLayout
from   java.awt          import Dimension
from   java.awt          import EventQueue
from   java.awt          import GridLayout

from   javax.swing       import JButton
from   javax.swing       import JFrame
from   javax.swing       import JPanel
from   javax.swing       import JScrollPane
from   javax.swing       import JTree

from   javax.swing.tree  import DefaultMutableTreeNode
from   javax.swing.tree  import DefaultTreeModel
from   javax.swing.tree  import MutableTreeNode
from   javax.swing.tree  import TreePath
from   javax.swing.tree  import TreeSelectionModel

from   javax.swing.event import TreeModelListener
from   javax.swing.event import TreeSelectionListener

#-------------------------------------------------------------------------------
#  Name: myTreeModelListener
#  Role: personalized TreeModelListener class
#-------------------------------------------------------------------------------
class myTreeModelListener( TreeModelListener ) :

    #---------------------------------------------------------------------------
    # Name: getNode
    # Role: Common routine used to locate the affected node
    #---------------------------------------------------------------------------
    def getNode( self, event ) :
        try :
            parent = self.getParent( event )
            node = parent.getChildAt(
                event.getChildIndices()[ 0 ]
            )
        except :
            node = event.getSource().getRoot()
        return node

    #---------------------------------------------------------------------------
    # Name: getParent
    # Role: Common routine used to locate the parent of the affected node
    #---------------------------------------------------------------------------
    def getParent( self, event ) :
        try :
            #-------------------------------------------------------------------
            # Path to the parent of the modified TreeNode
            # Traverse the tree to locate the parent node
            #-------------------------------------------------------------------
            path = event.getTreePath().getPath()
            parent = path[ 0 ]         # Start with root node
            for node in path[ 1: ] :   # Get parent of changed node
                parent = parent.getChildAt(
                    parent.getIndex( node )
                )
        except :
            parent = None
        return parent

    #---------------------------------------------------------------------------
    # Name: treeNodesChanged
    # Role: Invoked when the monitored TreeMode instance event occurs
    #---------------------------------------------------------------------------
    def treeNodesChanged( self, event ) :
        node = self.getNode( event )
        print ' treeNodesChanged():', node.getUserObject()

    #---------------------------------------------------------------------------
    # Name: treeNodesInserted
    # Role: Invoked when the monitored TreeMode instance event occurs
    #---------------------------------------------------------------------------
    def treeNodesInserted( self, event ) :
        node = self.getNode( event )
        print 'treeNodesInserted():', node.getUserObject()

    #---------------------------------------------------------------------------
    # Name: treeNodesRemoved
    # Role: Invoked when the monitored TreeMode instance event occurs
    #---------------------------------------------------------------------------
    def treeNodesRemoved( self, event ) :
        print ' treeNodesRemoved(): child %d under "%s"' % (
            event.getChildIndices()[ 0 ],
            self.getParent( event )
        )

    #---------------------------------------------------------------------------
    # Name: treeStructureChanged
    # Role: Invoked when the monitored TreeMode instance event occurs
    #---------------------------------------------------------------------------
    def treeStructureChanged( self, event ) :
        print 'treeStructureChanged():'

#-------------------------------------------------------------------------------
#  Name: DynamicTree
#  Role: User application demonstrating the use of a TreeModelListener to
#        monitor changes to the tree
#-------------------------------------------------------------------------------
class DynamicTree( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: __init__
    # Role: class constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        self.nodeSuffix = 0

    #---------------------------------------------------------------------------
    # Name: getSuffix
    # Role: return next suffix value to be used, after incrementing it
    #---------------------------------------------------------------------------
    def getSuffix( self ) :
        self.nodeSuffix += 1
        return self.nodeSuffix

    #---------------------------------------------------------------------------
    # Name: run
    # Role: Create, populate, & display application frame
    # Note: Called by Swing event dispatch thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'DynamicTree',
            layout = BorderLayout(),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        self.tree  = self.makeTree()      # Keep references handy
        self.model = self.tree.getModel()
        frame.add(
            JScrollPane(
                self.tree,
                preferredSize = Dimension( 300, 150 )
            ),
            BorderLayout.CENTER
        )
        frame.add( self.buttonRow(), BorderLayout.SOUTH )
        frame.pack()
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: buttonRow
    # Role: Create and return a panel holding a row of buttons
    #---------------------------------------------------------------------------
    def buttonRow( self ) :
        buttonPanel = JPanel( GridLayout( 0, 3 ) )
        data = [
            [ 'Add'   , self.addEvent ],
            [ 'Remove', self.delEvent ],
            [ 'Clear' , self.clsEvent ]
        ]
        self.buttons = {}
        for name, handler in data :
            self.buttons[ name ] = buttonPanel.add (
                JButton(
                    name,
                    actionPerformed = handler,
                    enabled = name != 'Remove'
                )
            )
        return buttonPanel

    #---------------------------------------------------------------------------
    # Name: addEvent()
    # Role: actionperformed() method for 'Add' button
    #---------------------------------------------------------------------------
    def addEvent( self, event ) :
        sPath = self.tree.getSelectionModel().getSelectionPath()
        if sPath :                     # Use selected node
            parent = sPath.getLastPathComponent()
        else :                         # Nothing selected, use root
            parent = self.model.getRoot()
        kids = parent.getChildCount()
        child = DefaultMutableTreeNode(
            'New node %d' % self.getSuffix()
        )
        self.model.insertNodeInto( child, parent, kids )
        self.tree.scrollPathToVisible(
            TreePath( child.getPath() )
        )

    #---------------------------------------------------------------------------
    # Name: delEvent()
    # Role: actionperformed() method for 'Remove' button
    # Note: This button is only enabled when a non-root node is selected
    #---------------------------------------------------------------------------
    def delEvent( self, event ) :
        currentSelection = self.tree.getSelectionPath()
        if currentSelection :
            currentNode = currentSelection.getLastPathComponent()
            if currentNode.getParent() :
                self.model.removeNodeFromParent( currentNode )
                return

    #---------------------------------------------------------------------------
    # Name: clsEvent()
    # Role: actionperformed() method for 'Clear' button
    #---------------------------------------------------------------------------
    def clsEvent( self, event ) :
        self.model.getRoot().removeAllChildren()
        self.model.reload()

    #---------------------------------------------------------------------------
    # Name: makeTree()
    # Role: Create, populate and return an editable JTree()
    #---------------------------------------------------------------------------
    def makeTree( self ) :
        #-----------------------------------------------------------------------
        # First, build the hierarchy of Tree nodes
        #-----------------------------------------------------------------------
        root = DefaultMutableTreeNode( 'Root Node' )
        for name in 'Parent 1,Parent 2'.split( ',' ) :
            here = DefaultMutableTreeNode( name )
            for child in 'Child 1,Child 2'.split( ',' ) :
                here.add( DefaultMutableTreeNode( child ) )
            root.add( here )
        #-----------------------------------------------------------------------
        # Next, use the hierarchy to create a Tree Model, with a listener
        #-----------------------------------------------------------------------
        model = DefaultTreeModel(
            root,
            treeModelListener = myTreeModelListener()
        )
        #-----------------------------------------------------------------------
        # Then, build our editable JTree() using this model
        #-----------------------------------------------------------------------
        tree = JTree(
            model,
            editable = 1,
            showsRootHandles = 1,
            valueChanged = self.select
        )
        #-----------------------------------------------------------------------
        # Only allow one node to be selectable at a time
        #-----------------------------------------------------------------------
        tree.getSelectionModel().setSelectionMode(
            TreeSelectionModel.SINGLE_TREE_SELECTION
        )
        return tree

    #---------------------------------------------------------------------------
    # Name: select()
    # Role: TreeSelectionListener valueChanged event handler
    #---------------------------------------------------------------------------
    def select( self, event ) :
        tree  = event.getSource()      # Get access to tree
        count = tree.getSelectionCount()
        sPath = tree.getSelectionModel().getSelectionPath()
        if sPath :                     # How deep is the pick?
            depth = sPath.getPathCount()
        else :                         # Nothing selected
            depth = 0
        self.buttons[ 'Remove' ].setEnabled( count and depth > 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( DynamicTree() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()