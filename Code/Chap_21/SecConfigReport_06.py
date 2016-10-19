#-------------------------------------------------------------------------------
#    Name: SecConfigReport_06.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple wsadmin Jython script to display the results of the AdminTask
#          generateSecConfigReport() command
#    Note: This script requires a WebSphere Application Server environment.
#   Usage: wsadmin -f SecConfigReport_06.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 13/01/08  rag  0.6   Add - first try at determining the right column widths
# 13/01/05  rag  0.5   Fix - resolve heading rows highlighting deficiencies
# 13/01/05  rag  0.4   Fix - highlight heading rows using color
# 13/01/05  rag  0.3   Add - TableModel & CellRenderer to make heading rows bold
# 13/01/05  rag  0.2   Fix - Ignore the trailing (empty delimiter)
# 13/01/05  rag  0.1   New - Initial try - simple display of text data
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import Color
from   java.awt    import Dimension
from   java.awt    import EventQueue
from   java.awt    import Font

from   java.lang   import String

from   javax.swing import JLabel
from   javax.swing import JFrame
from   javax.swing import JTable
from   javax.swing import JScrollPane
from   javax.swing import ListSelectionModel

from   javax.swing.table import DefaultTableCellRenderer
from   javax.swing.table import DefaultTableModel

#-------------------------------------------------------------------------------
# Define some global font related variables
#-------------------------------------------------------------------------------
plainFont = Font( 'Dialog', Font.PLAIN, 12 )
boldFont  = Font( 'Dialog', Font.BOLD , 12 )
fmPlain   = JLabel().getFontMetrics( plainFont )
fmBold    = JLabel().getFontMetrics( boldFont  )

#-------------------------------------------------------------------------------
# Name: reportTableModel
# Role: Define table data characteristics
#-------------------------------------------------------------------------------
class reportTableModel( DefaultTableModel ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Class constructor
    # Note: Save the initial data for easy highlight removal
    #---------------------------------------------------------------------------
    def __init__( self, data, headings ) :
        DefaultTableModel.__init__( self, data, headings )

    #---------------------------------------------------------------------------
    # Name: isCellEditable()
    # Role: Each cell in the table is read-only
    #---------------------------------------------------------------------------
    def isCellEditable( self, row, col ) :
        return 0

    #---------------------------------------------------------------------------
    # Name: getColumnClass()
    # Role: Each cell in the table is a java.lang.String
    #---------------------------------------------------------------------------
    def getColumnClass( self, col ) :
        return String

#-------------------------------------------------------------------------------
# Name: reportRenderer
# Role: Display the method table cells using the appropriate width & hilighting
# Note: It is used each time a cell must be displayed.
#-------------------------------------------------------------------------------
class reportRenderer( DefaultTableCellRenderer ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Class constructor
    # Note: Initialize the default cell background & foreground color variables
    #---------------------------------------------------------------------------
    def __init__( self ) :
        self.bg = self.fg = None

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
        row,                 # int     - Row # ( 0 .. N-1 )
        col                  # int     - Col # ( 0 .. N-1 )
    ) :
        #-----------------------------------------------------------------------
        # Start by retrieving the default renderer component (i.e., JLabel)
        #-----------------------------------------------------------------------
        DTCR = DefaultTableCellRenderer
        comp = DTCR.getTableCellRendererComponent(
            self, table, value, isSelected, hasFocus, row, col
        )
        if self.bg == self.fg :
            self.bg = comp.getBackground()
            self.fg = comp.getForeground()
#           print comp.getFont()
        if value :
            if table.getValueAt( row, 0 ).startswith( '_' ) :
                comp.setBackground( Color.blue )
                comp.setForeground( Color.white )
                if col == 0 :
                    value = value[ 1: ]
                comp.setText( value )
                comp.setFont( boldFont )
            else :
                comp.setBackground( self.bg )
                comp.setForeground( self.fg )
                comp.setFont( plainFont )

        return comp

#-------------------------------------------------------------------------------
# Name: SecConfigReport_06()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class SecConfigReport_06( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'SecConfigReport_06',
            size = ( 500, 300 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        data = []
        text = AdminTask.generateSecConfigReport()
        for line in text.splitlines()[ 2: ] :
            data.append(
                [
                    info.strip() for info in
                    line[ :-2 ].split( ';' )
                ]
            )

        table =  JTable(
            reportTableModel(
                data, ';;;'.split( ';' ),
            ),
            selectionMode = ListSelectionModel.SINGLE_SELECTION
        )
        table.setDefaultRenderer( String, reportRenderer() )
        self.setColumnWidths( table )
        frame.add( JScrollPane( table ) )

        frame.pack()
        frame.setVisible( 1 )
        print 'frame:', frame.getSize()
        print 'vPort:', table.getParent().getExtentSize()


    #---------------------------------------------------------------------------
    # Name: setColumnWidths()
    # Role: Compute, and set the preferred column widths and viewport size
    # Note: This table doesn't have a header row
    #---------------------------------------------------------------------------
    def setColumnWidths( self, table ) :

        #-----------------------------------------------------------------------
        # Set up some variables to access the table properties and data
        #-----------------------------------------------------------------------
        tcm    = table.getColumnModel() # Table Column Model
        model  = table.getModel()       # access the table data
        margin = tcm.getColumnMargin()  # gap between columns

        #-----------------------------------------------------------------------
        # For each column, determine the maximum width required
        #-----------------------------------------------------------------------
        rows = model.getRowCount()      # How many rows    exist?
        cols = tcm.getColumnCount()     # How many columns exist?

        labels = [
            JLabel( font = plainFont ),
            JLabel( font = boldFont  )
        ]
        print '                Now Min Pre Max'
        print '---------------+---+---+---+---'
        metrics = [ fmPlain, fmBold ]
        tWidth = 0                      # Table width
        section = 0                     # is this row a section?
        sections = 0                    # Number of sections
        for i in range( cols ) :        # i == column index
            col = tcm.getColumn( i )
            idx = col.getModelIndex()
            #-------------------------------------------------------------------
            # Find the maximum width required for the data values in this column
            # Note: Use the column adjustments to compute the best width
            #-------------------------------------------------------------------
            cWidth = 0                  # Initial column width
            for row in range( rows ) :
                v0  = model.getValueAt( row, 0 )
                if v0.startswith( '_' ) :
                    section = 1
                    sections += 1
                else :
                    section = 0
                comp = labels[ section ]
                fm   = metrics[ section ]        # FontMetric
                r = table.getCellRenderer( row, i )
                v = model.getValueAt( row, idx )
                if v.startswith( '_' ) :
                    v = v[ 1: ]
                comp.setText( v )
                cWidth = max(
                    cWidth,
                    comp.getPreferredSize().width
                )

            if cWidth > 0 :
                col.setMinWidth( 128 + margin )
                col.setPreferredWidth( 128 + margin )
                col.setMaxWidth( cWidth + margin )
                print 'Col: %d  widths |%3d|%3d|%3d|%d' % (
                    i,
                    col.getWidth(),
                    col.getMinWidth(),
                    col.getPreferredWidth(),
                    col.getMaxWidth()
                )

            #-------------------------------------------------------------------
            # Add current column (preferred) width to the total table width
            #-------------------------------------------------------------------
            tWidth += col.getPreferredWidth()

        print '---------------+---+---+---+---'
        h0 = table.getRowHeight()
        print 'rowHeight:', h0
        sections /= cols
        print '#Sections:', sections

        for row in range( rows ) :
            lines = 1
            for i in range( cols ) :
                col = tcm.getColumn( i )
                pre = col.getPreferredWidth()
                idx = col.getModelIndex()
                val = model.getValueAt( row, idx )
                if not i :
                    section = val.startswith( '_' )
                fm    = metrics[ section ]       # FontMetric
                lines = max(
                    lines, int(
                        round( fm.stringWidth( val ) / pre ) + 1
                    )
                )
            table.setRowHeight( row, lines * h0 )

        #-----------------------------------------------------------------------
        # Set the preferred viewport size so we don't (initially) see scrollbars
        #-----------------------------------------------------------------------
        table.setPreferredScrollableViewportSize(
            Dimension(
                tWidth,
                sections * table.getRowHeight()
            )
        )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( SecConfigReport_06() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f SecConfigReport_06.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
