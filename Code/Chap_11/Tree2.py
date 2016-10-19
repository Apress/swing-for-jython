#-------------------------------------------------------------------------------
#    Name: Tree2.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script that disallows tree node selection
#    Note: A WebSphere Application Server environment is required.
#   Usage: wsadmin -f Tree2.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/25  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue

from   javax.swing import JFrame
from   javax.swing import JScrollPane
from   javax.swing import JTree

from   javax.swing.tree import DefaultMutableTreeNode

#-------------------------------------------------------------------------------
# Name: Tree2()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Tree2( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: cellTree()
    # Role: create a tree representation of the WebSphere cell hierarchy
    #---------------------------------------------------------------------------
    def cellTree( self ) :
        # Use the cellName as the tree root node
        cell = AdminConfig.list( 'Cell' )
        root = DefaultMutableTreeNode( self.getName( cell ) )

        for node in AdminConfig.list( 'Node' ).splitlines() :
            here = DefaultMutableTreeNode(
                self.getName( node )
            )
            servers = AdminConfig.list( 'Server', node )
            for server in servers.splitlines() :
                leaf = DefaultMutableTreeNode(
                    self.getName( server )
                )
                here.add( leaf )
            root.add( here )

        return JTree( root )

    #---------------------------------------------------------------------------
    # Name: getName()
    # Role: Return the name attribute of the specified configuration object
    #---------------------------------------------------------------------------
    def getName( self, configId ) :
        return AdminConfig.showAttribute( configId, 'name' )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Tree2',
            size = ( 200, 200 ),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        tree = self.cellTree()
        tree.setSelectionModel( None )
        frame.add( JScrollPane( tree ) )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( Tree2() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f Tree2.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
