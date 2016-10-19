#-------------------------------------------------------------------------------
#    Name: TableSelection3.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample Jython Swing script using a JTabbedPane to show the state of
#          the Row, Column, and Cell selection allowed/enabled settings after
#          various setters are used.
#    Note: The table that is used to display these results does not have these
#          settings.
#   Usage: wsadmin -f TableSelection3.py
#            or
#          jython TableSelection3.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/25  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue
from   java.awt    import BorderLayout

from   java.lang   import Boolean

from   javax.swing import JButton
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JPanel
from   javax.swing import JScrollPane
from   javax.swing import JTabbedPane
from   javax.swing import JTable
from   javax.swing import ListSelectionModel as LSM
from   javax.swing import SwingConstants

from   javax.swing.table import DefaultTableCellRenderer
from   javax.swing.table import DefaultTableModel

#-------------------------------------------------------------------------------
# Name: boolRenderer
# Role: This renderer extends a component.
# Note: It is used each time a cell must be displayed.
#-------------------------------------------------------------------------------
class boolRenderer( DefaultTableCellRenderer ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        self.result = JLabel(
            horizontalAlignment = SwingConstants.CENTER
        )

    #---------------------------------------------------------------------------
    # Name: getTableCellRendererComponent()
    # Role: Return the component containing the rendered value
    # Note: Called frequently, don't create a new component each time
    #---------------------------------------------------------------------------
    def getTableCellRendererComponent(
        self,
        table,               # JTable  - table containing value
        value,               # Object  - value being rendered
        isSelected,          # boolean - Is value selected?
        hasFocus,            # boolean - Does this cell have focus?
        rowIndex,            # int     - Row # (0..N)
        vColIndex            # int     - Col # (0..N)
    ) :

        # Configure the component with the specified value
        result = str( value )
        #-----------------------------------------------------------------------
        # Note: The bool type in Standard Jython requires special handling...
        #-----------------------------------------------------------------------
        if result in [ 'False', 'True' ] :
            result = str( [ 'False', 'True' ].index( result ) )
        self.result.setText( result )

        return self.result

#-------------------------------------------------------------------------------
# Name: booleanTM()
# Role: Every cell is a boolean, to be displayed as a centered digit
#-------------------------------------------------------------------------------
class booleanTM( DefaultTableModel ) :

    #---------------------------------------------------------------------------
    # Name: getColumnClass()
    # Role: Return the column specific datatype
    #---------------------------------------------------------------------------
    def getColumnClass( self, col ) :
        return Boolean

#-------------------------------------------------------------------------------
# Name: TableSelection3()
# Role: Used to demonstrate how to create, and display a JFrame instance
#-------------------------------------------------------------------------------
class TableSelection3( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
           'TableSelection3',
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        self.addTabs( frame.getContentPane() )

        frame.setSize( 500, 200 )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: settings()
    # Role: .
    #---------------------------------------------------------------------------
    def settings( self, table ) :
        def getState( table ) :
            return [
                Boolean( table.getRowSelectionAllowed() ),
                Boolean( table.getColumnSelectionAllowed() ),
                Boolean( table.getCellSelectionEnabled() )
            ]

        result = []
        result.append( getState( table ) )       # Expected [ 1, 0, 0 ]
        table.setColumnSelectionAllowed( 1 )
        result.append( getState( table ) )       # Expected [ 1, 1, 1 ]
        table.setRowSelectionAllowed( 0 )
        result.append( getState( table ) )       # Expected [ 0, 1, 0 ]
        table.setRowSelectionAllowed( 1 )
        result.append( getState( table ) )       # Expected [ 1, 1, 1 ]
        table.setCellSelectionEnabled( 0 )
        result.append( getState( table ) )       # Expected [ 0, 0, 0 ]
        table.setCellSelectionEnabled( 1 )
        result.append( getState( table ) )       # Expected [ 1, 1, 1 ]

        return result

    #---------------------------------------------------------------------------
    # Name: addTabs()
    # Role: Add the tab panels
    #---------------------------------------------------------------------------
    def addTabs( self, container ) :

        head = 'Row,Col,Cell'.split( ',' )
        junk = 'False,True'.split( ',' )
        data = [ [ 0, 1 ], [ 0, 1 ] ]

        info = JTable(  # Used to get default attributes
            data,
            head,
            selectionMode = LSM.SINGLE_SELECTION
        )

        bTable = JTable(
            booleanTM(
                self.settings( info ),
                head
            )
        )
        bTable.setDefaultRenderer( Boolean, boolRenderer() )
        tab1 = JPanel()
        tab1.add( JScrollPane( bTable ) )

        info = JTable(
            data,
            head,
            selectionMode = LSM.SINGLE_INTERVAL_SELECTION
        )

        bTable = JTable(
            booleanTM(
                self.settings( info ),
                head
            )
        )
        bTable.setDefaultRenderer( Boolean, boolRenderer() )
        tab2 = JPanel()
        tab2.add( JScrollPane( bTable ) )

        info = JTable(
            data,
            head,
            selectionMode = LSM.MULTIPLE_INTERVAL_SELECTION
        )

        bTable = JTable(
            booleanTM(
                self.settings( info ),
                head
            )
        )
        bTable.setDefaultRenderer( Boolean, boolRenderer() )
        tab3 = JPanel()
        tab3.add( JScrollPane( bTable ) )

        tabs = JTabbedPane()
        tabs.addTab( 'Single'     , tab1 )
        tabs.addTab( 'One Group'  , tab2 )
        tabs.addTab( 'Multi-Group', tab3 )

        container.add( tabs )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( TableSelection3() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
