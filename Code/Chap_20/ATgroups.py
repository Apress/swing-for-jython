#-------------------------------------------------------------------------------
#    Name: ATgroups.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: wsadmin Jython script to build a JTree of the AdminTask commandGroups
#    Note: This requires a WebSphere Application Server environment.
#          Empty groups are not added to the tree
#   Usage: wsadmin -f ATgroups.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/11/03  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import re
import sys

from   java.awt    import EventQueue
from   java.awt    import BorderLayout

from   javax.swing import JFrame
from   javax.swing import JScrollPane
from   javax.swing import JTree

from   javax.swing.tree import DefaultMutableTreeNode
from   javax.swing.tree import TreeSelectionModel

#-------------------------------------------------------------------------------
# Name: ATgroups()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class ATgroups( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: groupTree()
    # Role: create, and return, a tree representation of the
    #       AdminTask.help( '-commandGroups' ) hierarchy
    #---------------------------------------------------------------------------
    def groupTree( self ) :
        data = AdminTask.help( '-commandGroups' ).expandtabs().splitlines()
        root = DefaultMutableTreeNode( 'command groups' )

        for line in data[ 1: ] :
            mo = re.match( '([a-zA-Z ]+) -', line )
            if mo :
                groupName = mo.group( 1 )
                group = None
                text = AdminTask.help( groupName )
                cmds = text.find( 'Commands:' )
                if cmds > 0 :
                    for line in text[ cmds + 9: ].splitlines() :
                        mo = re.match( '([a-zA-Z_2]+) -', line )
                        if mo :
                            if not group :
                                group = DefaultMutableTreeNode(
                                    groupName
                                )
                            group.add(
                                DefaultMutableTreeNode(
                                    mo.group( 1 )
                                )
                            )
                    if group :
                        root.add( group )
                    else :
                        print 'Empty group:', groupName

        return JTree(
            root,
            rootVisible = 0 #,
#           valueChanged = self.select
        )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'AdminTask commandGroups',
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        tree = self.groupTree()
        tree.getSelectionModel().setSelectionMode(
            TreeSelectionModel.SINGLE_TREE_SELECTION
        )
        frame.add(
            JScrollPane(
                tree,
                preferredSize = ( 300, 300 )
            ),
            BorderLayout.CENTER
        )
        frame.pack()
        print frame.getSize()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( ATgroups() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f ATgroups.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
