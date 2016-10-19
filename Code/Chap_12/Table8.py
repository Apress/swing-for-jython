#-------------------------------------------------------------------------------
#    Name: Table8.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script with adjusting Table column widths
#    Note: This uses the Preferred size, based upon the datatype of the column
#   Usage: wsadmin -f Table8.py
#            or
#          jython Table8.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/25  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue

from   java.lang   import Boolean
from   java.lang   import Float
from   java.lang   import Double
from   java.lang   import Integer

from   java.util   import Date

from   java.text   import DateFormat
from   java.text   import NumberFormat

from   javax.swing import JFormattedTextField
from   javax.swing import JFrame
from   javax.swing import JTable
from   javax.swing import JTextField
from   javax.swing import ListSelectionModel
from   javax.swing import JScrollPane

from   javax.swing.table import DefaultTableCellRenderer
from   javax.swing.table import DefaultTableModel

#-------------------------------------------------------------------------------
# Name: myRenderer
# Role: This renderer extends a component.
# Note: It is used each time a cell must be displayed.
#-------------------------------------------------------------------------------
class myRenderer( DefaultTableCellRenderer ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor - instantiate the JFormattedTextField to be used
    #---------------------------------------------------------------------------
    def __init__( self ) :
        nf = NumberFormat.getInstance()
        nf.setMinimumFractionDigits( 2 )
        nf.setMaximumFractionDigits( 2 )
        self.result = JFormattedTextField(
            nf,
            border = None,
            horizontalAlignment = JTextField.RIGHT
        )
        self.DTCR = DefaultTableCellRenderer()

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
        row,                 # int     - Row # (0..N)
        col                  # int     - Col # (0..N)
    ) :
        comp = self.DTCR.getTableCellRendererComponent(
            table, value, isSelected, hasFocus, row, col
        )
        result = self.result
        result.setForeground( comp.getForeground() )
        result.setBackground( comp.getBackground() )
        result.setBorder( comp.getBorder() )
        result.setValue( value )
        return result

#-------------------------------------------------------------------------------
# Name: myTM()
# Role: Personalize the table model to provide appropriate column data types
#-------------------------------------------------------------------------------
class myTM( DefaultTableModel ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor - invoke the DefaultTableModel constructor
    #---------------------------------------------------------------------------
    def __init__( self, data, headings ) :
        info = []
        df   = DateFormat.getDateInstance( DateFormat.SHORT )
        for tf, date, size, f, d in data :
            info.append(
                [
                    Boolean( tf == '1' ),
                    df.parse( date ),
                    Integer( size.strip().replace( ',', '' ) ),
                    Float( f ),
                    Double( d )
                ]
            )
        DefaultTableModel.__init__( self, info, headings )

    #---------------------------------------------------------------------------
    # Name: getColumnClass()
    # Role: Return the column specific datatype
    #---------------------------------------------------------------------------
    def getColumnClass( self, col ) :
        return [ Boolean, Date, Integer, Float, Double ][ col ]

#-------------------------------------------------------------------------------
# Name: Table8()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Table8( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        info = r'''
1|08/22/2011|   726| 0.0| 3.14159
0|05/12/2010| 2,535| 1.1| 6.28318
1|06/23/2009| 1,715| 2.2| 9.42477
0|05/03/2008| 1,697| 3.3|12.56636
1|04/23/2008|   506| 4.4|15.70795
'''
        self.data = [                       # list comprehension
            line.split( '|' )               # each row is an array
            for line in info.splitlines()   # each line is a row
            if line                         # ignore blank lines
        ]

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Table8',
            size = ( 300, 150 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        headings = 'T/F,Date,Integer,Float,Double'.split( ',' )
        model = myTM( self.data, headings )
        table = JTable(
            model,
            selectionMode = ListSelectionModel.SINGLE_SELECTION
        )
        table.getColumnModel().getColumn(
            model.getColumnCount() - 1 # i.e., last column
        ).setCellRenderer(
            myRenderer()
        )

        #----------------------------------------------------------
        # Adjust the width of the columns using only header text
        #----------------------------------------------------------
        hRenderer = table.getTableHeader().getDefaultRenderer()
        for col in range( model.getColumnCount() ) :
            column = table.getColumnModel().getColumn( col )
            comp = hRenderer.getTableCellRendererComponent(
                None,                       # Table
                column.getHeaderValue(),    # value
                0,                          # isSelected = false 
                0,                          # hasFocus = false
                -1,                         # row #
                col                         # col #
            )
            width = comp.getPreferredSize().width
#           print 'col: %d  previous: %d  current: %d' % ( col, column.getPreferredWidth(), width )
            column.setMinWidth( width )
            column.setMaxWidth( width )
#           column.setPreferredWidth( width )

        frame.add( JScrollPane( table ) )
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( Table8() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
