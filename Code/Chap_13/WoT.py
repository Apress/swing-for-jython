#-------------------------------------------------------------------------------
#    Name: WoT.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script demonstrating the findEditableCell() class
#   Usage: wsadmin -f WoT.py
#            or
#          jython WoT.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/27  rag  0.0  New - ...
#-------------------------------------------------------------------------------
import java

from   java.awt          import Dimension
from   java.awt          import EventQueue
from   java.awt          import GridLayout
from   java.awt          import Toolkit

from   java.lang         import Boolean
from   java.lang         import Integer
from   java.lang         import String

from   javax.swing       import AbstractAction
from   javax.swing       import JFrame
from   javax.swing       import JPanel
from   javax.swing       import JScrollPane
from   javax.swing       import JTable
from   javax.swing       import ListSelectionModel

from   javax.swing.table import DefaultTableModel

#-------------------------------------------------------------------------------
# Name: tableModel()
# Role: An implementation that populates the table with data
#-------------------------------------------------------------------------------
class tableModel( DefaultTableModel ) :
    columnNames = [ 'First Name', 'Last Name', 'Married?' ]
    dataType    = [ String, String, Boolean ]
    data = [
        [ 'Rand'    , "al'Thor" , Boolean( 1 ) ],
        [ 'Egwene'  , "al'Vere" , Boolean( 0 ) ],
        [ 'Matrim'  , 'Cauthon' , Boolean( 1 ) ],
        [ 'Perrin'  , 'Aybara'  , Boolean( 1 ) ],
        [ 'Moiraine', 'Damodred', Boolean( 0 ) ]
    ]

    def getColumnCount( self )           : return len( self.columnNames )

    def getRowCount( self )              : return len( self.data )

    def getColumnName( self, col )       : return self.columnNames[ col ]

    def getValueAt( self, row, col )     : return self.data[ row ][ col ]

    def getColumnClass( self, col )      : return self.dataType[ col ]

    def isCellEditable( self, row, col ) : return col > 1

    def setValueAt( self, value, row, col ) :
        try :
            self.data[ row ][ col ] = self.dataType[ col ]( value )
        except :
            Type = str( self.dataType[ col ] ).split( '.' )[ -1 ]
            print '\nError: invalid %s value ignored: "%s"' % ( Type, value ),
        self.fireTableCellUpdated( row, col )

#-------------------------------------------------------------------------------
# Name: findEditableCell()
# Role: Action implementation to locate the next editable cell
# Note: The constructor saves the original action and the instantiation will use
#       this saved action to be sure to go in the appropirate direction.
#-------------------------------------------------------------------------------
class findEditableCell( AbstractAction ) :

    def __init__( self, table, action ) :
        self.table    = table
        self.original = table.getActionMap().get( action )
        self.table.getActionMap().put( action, self )
        self.beep     = Toolkit.getDefaultToolkit().beep

    def actionPerformed( self, actionEvent ) :
        table = self.table
        numCells = table.getRowCount() * table.getColumnCount()
        for cell in range( numCells ) :
            self.original.actionPerformed( actionEvent )
            if table.isCellEditable(
               table.getSelectedRow(),
               table.getSelectedColumn()
            ) :
                return
        self.beep()

#-------------------------------------------------------------------------------
# Name: WoT()
# Role: Jython Swing script that demonstrates how to use the findEditableCell()
#       class
#-------------------------------------------------------------------------------
class WoT( java.lang.Runnable ) :

    def run( self ) :
        frame = JFrame(
            'WoT',
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        table = JTable(
            tableModel(),
            fillsViewportHeight = 1,
            cellSelectionEnabled = 1,
            selectionMode = ListSelectionModel.SINGLE_SELECTION,
            preferredScrollableViewportSize = Dimension( 250, 80 )
        )

        findEditableCell( table, 'selectNextColumnCell' )
        findEditableCell( table, 'selectPreviousColumnCell' )

        panel = JPanel(
            GridLayout( 1, 0 ),
            opaque = 1
        )
        panel.add( JScrollPane( table ) )

        frame.add( panel )
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( WoT() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
