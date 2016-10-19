#-------------------------------------------------------------------------------
#    Name: Table11.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script with adjusted Table column widths
#    Note: Provides a menu entry to allow the user to specify AUTO_RESIZE value
#   Usage: wsadmin -f Table11.py
#            or
#          jython Table11.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/25  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import EventQueue
from   java.awt    import Dimension

from   java.lang   import Boolean
from   java.lang   import Float
from   java.lang   import Double
from   java.lang   import Integer
from   java.lang   import String

from   java.util   import Date

from   java.text   import DateFormat
from   java.text   import NumberFormat

from   javax.swing import ButtonGroup
from   javax.swing import JFormattedTextField
from   javax.swing import JFrame
from   javax.swing import JMenu
from   javax.swing import JMenuBar
from   javax.swing import JMenuItem
from   javax.swing import JRadioButtonMenuItem
from   javax.swing import JTable
from   javax.swing import JTextField
from   javax.swing import ListSelectionModel
from   javax.swing import JScrollPane

from   javax.swing.table import DefaultTableCellRenderer
from   javax.swing.table import DefaultTableModel

#-------------------------------------------------------------------------------
# Name: setColumnWidths()
# Role: Compute, and set the preferred column widths and viewport size
#-------------------------------------------------------------------------------
def setColumnWidths( table ) :
    #---------------------------------------------------------------------------
    # It's possible for this table to not have a header...
    #---------------------------------------------------------------------------
    header = table.getTableHeader()
    if header :
        hRenderer = header.getDefaultRenderer()
    else :
        hRenderer = None

    #---------------------------------------------------------------------------
    # Variables used to access the table properties and data
    #---------------------------------------------------------------------------
    tcm    = table.getColumnModel()         # Table Column Model
    data   = table.getModel()               # To access table data
    margin = tcm.getColumnMargin()          # gap between columns

    #---------------------------------------------------------------------------
    # For each column, determine the maximum width required
    #---------------------------------------------------------------------------
    rows = data.getRowCount()               # Number of rows
    cols = tcm.getColumnCount()             # Number of cols

    #---------------------------------------------------------------------------
    # Used for parse & format date strings & objects
    #---------------------------------------------------------------------------
    df   = DateFormat.getDateInstance( DateFormat.MEDIUM )

    tWidth = 0                              # Table width
    for i in range( cols ) :                # For col 0..N
        col = tcm.getColumn( i )            # TableColumn: col i
        idx = col.getModelIndex()           # model index: col i

        #-----------------------------------------------------------------------
        # To determine the preferred column width, we
        # must use the current renderer for this column
        #-----------------------------------------------------------------------
        render = col.getHeaderRenderer()    # header renderer,
        if not render :                     #   
            render = hRenderer              #   or a default

        #-----------------------------------------------------------------------
        # Get preferred header width for column i
        #-----------------------------------------------------------------------
        if render :
            comp = render.getTableCellRendererComponent(
                table,
                col.getHeaderValue(),
                0,
                0,
                -1,
                i
            )
            cWidth = comp.getPreferredSize().width
        else :
            cWidth = -1
        #-----------------------------------------------------------------------
        # Compute the maximum width required for the data values in this column
        #-----------------------------------------------------------------------
        Type = data.getColumnClass( i )          # dataType: col i
        for row in range( rows ) :
            v = data.getValueAt( row, idx )      # value
            if Type == Date :
                val = df.format( v )             # formatted date
                r = table.getDefaultRenderer( String )
            else :
                val = Type( v )
                r = table.getCellRenderer( row, i )
            comp = r.getTableCellRendererComponent(
                table,
                val,                             # formatted value
                0,                               # not selected
                0,                               # not in focus
                row,                             # row num
                i                                # col num
            )
            cWidth = max( cWidth, comp.getPreferredSize().width )

        if cWidth > 0 :
#           print 'col %d preferredWidth %d' % ( i, cWidth + margin )
            col.setPreferredWidth( cWidth + margin )

        #-----------------------------------------------------------------------
        # Table width = sum of column widths
        #-----------------------------------------------------------------------
        tWidth += col.getPreferredWidth()

    #---------------------------------------------------------------------------
    # Set the preferred viewport size so we don't (initially) see scrollbars
    # Note: This assumes a uniform row height for every row
    #---------------------------------------------------------------------------
    table.setPreferredScrollableViewportSize(
        Dimension(
            tWidth,
            rows * table.getRowHeight()
        )
    )
#   print 'table viewport width:', tWidth

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
# Name: Table11()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class Table11( java.lang.Runnable ) :

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
        self.info = [
            [ 'Off' , JTable.AUTO_RESIZE_OFF                ],
            [ 'Next', JTable.AUTO_RESIZE_NEXT_COLUMN        ],
            [ 'Rest', JTable.AUTO_RESIZE_SUBSEQUENT_COLUMNS ],
            [ 'Last', JTable.AUTO_RESIZE_LAST_COLUMN        ],
            [ 'All' , JTable.AUTO_RESIZE_ALL_COLUMNS        ]
        ]

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'Table11',
            size = ( 300, 170 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        menuBar = JMenuBar()
        resize  = JMenu( 'AUTO_RESIZE' )

        bGroup  = ButtonGroup()
        for name, value in self.info :
            rb = JRadioButtonMenuItem(
                name,
                actionPerformed = self.handler,
                selected = ( name == 'Rest' )
            )
            bGroup.add( rb )
            resize.add( rb )
        menuBar.add( resize )
        frame.setJMenuBar( menuBar )

        headings = 'T/F,Date,Integer,Float,Double'.split( ',' )
        model = myTM( self.data, headings )
        self.table = table = JTable(
            model,
            selectionMode = ListSelectionModel.SINGLE_SELECTION
        )
        table.getColumnModel().getColumn(
            model.getColumnCount() - 1 # i.e., last column
        ).setCellRenderer(
            myRenderer()
        )
        setColumnWidths( table )

        frame.add( JScrollPane( table ) )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: handler()
    # Role: Constructor
    #---------------------------------------------------------------------------
    def handler( self, event ) :
        cmd = event.getActionCommand()
        for name, value in self.info :
            if cmd == name :
                self.table.setAutoResizeMode( value )
                self.table.repaint()

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( Table11() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
