#-------------------------------------------------------------------------------
#    Name: SecConfigReport_12.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple wsadmin Jython script to display the results of the AdminTask
#          generateSecConfigReport() command
#    Note: This script requires a WebSphere Application Server environment.
#          Variable row heights "break" page up/down function
#   Usage: wsadmin -f SecConfigReport_12.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 13/01/26  rag  0.12  Add - Menu item to find text
# 13/01/25  rag  0.11  Add - Menu items including collapse & expand all
# 13/01/25  rag  0.10  Fix - Remove rowFinder class and add upDownAction   
# 13/01/19  rag  0.9   Add - ChangeListener to locate displayed rows better
# 13/01/12  rag  0.8   Fix - row selection color within cell renderer class
# 13/01/11  rag  0.7   Add - frame resize listener & better display of cell data
# 13/01/08  rag  0.6   Add - first try at determining the right column widths
# 13/01/05  rag  0.5   Fix - resolve heading rows highlighting deficiencies
# 13/01/05  rag  0.4   Fix - highlight heading rows using color
# 13/01/05  rag  0.3   Add - TableModel & CellRenderer to make heading rows bold
# 13/01/05  rag  0.2   Fix - Ignore the trailing (empty delimiter)
# 13/01/05  rag  0.1   New - Initial try - simple display of text data
#-------------------------------------------------------------------------------

'''
Command: SecConfigReport_12.py
Purpose: A wsadmin Jython script demonstrating some techniques for graphically
         displaying information about the WebSphere Application Server security
         configuration report using Java Swing components.
 Author: Robert A. (Bob) Gibson <bgibson@us.ibm.com>
   Note: This script is provided "AS IS". See the "Help -> Notice" for details.
  Usage: wsadmin -f SecConfigReport_12.py
Example: ./wsadmin.sh -f SecConfigReport_12.py\n
Version: 0.12
Updated: 26 Jan 2013
'''

import java
import re
import sys

from   java.awt          import Color
from   java.awt          import Dimension
from   java.awt          import EventQueue
from   java.awt          import Font
from   java.awt          import Point

from   java.lang         import ArrayIndexOutOfBoundsException
from   java.lang         import String

from   javax.swing       import AbstractAction
from   javax.swing       import JComponent
from   javax.swing       import JLabel
from   javax.swing       import JFrame
from   javax.swing       import JMenu
from   javax.swing       import JMenuBar
from   javax.swing       import JMenuItem
from   javax.swing       import JOptionPane
from   javax.swing       import JSeparator
from   javax.swing       import JScrollPane
from   javax.swing       import JTable
from   javax.swing       import KeyStroke
from   javax.swing       import ListSelectionModel
from   javax.swing       import RowFilter

from   javax.swing.event import ChangeListener

from   javax.swing.table import DefaultTableCellRenderer
from   javax.swing.table import DefaultTableModel

#-----------------------------------------------------------------------
# Font used to display help text
#-----------------------------------------------------------------------
monoFont  = Font( 'Courier', Font.PLAIN, 12 )

#-------------------------------------------------------------------------------
# Define some global font related variables
#-------------------------------------------------------------------------------
plainFont = Font( 'Dialog', Font.PLAIN, 12 )
boldFont  = Font( 'Dialog', Font.BOLD , 12 )
fmPlain   = JLabel().getFontMetrics( plainFont )
fmBold    = JLabel().getFontMetrics( boldFont  )

#-----------------------------------------------------------------------
# HTML tag to highlight findText
#-----------------------------------------------------------------------
hilightHTML = '<font bgcolor="green" color="yellow">%s</font>'

#-----------------------------------------------------------------------
# Disclaimer notice displayed by the Help -> Notice event handler
#-----------------------------------------------------------------------
Disclaimer = '''
By accessing and/or using these sample files, you acknowledge that you have
read, understood, and agree, to be bound by these terms. You agree to the
binding nature of these english language terms and conditions regardless of
local language restrictions. If you do not agree to these terms, do not use the
files. International Business Machines corporation provides these sample files
on an "As Is" basis for your internal, non-commercial use and IBM disclaims all
warranties, express or implied, including, but not limited to, the warranty of
non-infringement and the implied warranties of merchantability or fitness for a
particular purpose.  IBM shall not be liable for any direct, indirect,
incidental, special or consequential damages arising out of the use or operation
of this software.  IBM has no obligation to provide maintenance, support,
updates, enhancements or modifications to the sample files provided.
'''

#-------------------------------------------------------------------------------
# Name: upDownAction
# Role: Modify the action for the specified KeyStroke to align the top, or
#       bottom row with the top or bottom of the viewport.  The alignment 
#       coincides with the user specified direction (i.e., up == top, and
#       down == bottom).
#-------------------------------------------------------------------------------
class upDownAction( AbstractAction ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Class constructor
    # Note: Save the table and initial action for specified key
    #---------------------------------------------------------------------------
    def __init__( self, table, keyName ) :
        self.table   = table
        ks           = KeyStroke.getKeyStroke( keyName )
        self.up      = keyName.find( 'UP' ) > -1
        self.action  = action = table.getInputMap(
            JComponent.WHEN_ANCESTOR_OF_FOCUSED_COMPONENT
        ).get( ks )
        self.original = table.getActionMap().get( action )
        self.table.getActionMap().put( action, self )

    #---------------------------------------------------------------------------
    # Name: actionPerformed()
    # Role: Implement new action using original version
    #---------------------------------------------------------------------------
    def actionPerformed( self, actionEvent ) :
        table = self.table
        self.original.actionPerformed( actionEvent )
        #-----------------------------------------------------------------------
        # Unfortunately, tables with variable row heights don't reposition to
        # the end of table correctly the first time, especially from top row.
        #-----------------------------------------------------------------------
        if self.action == 'selectLastRow' :
            self.original.actionPerformed( actionEvent )
        #-----------------------------------------------------------------------
        # Since the JTable() is within a JScrollPane, its parent is a JViewport
        # Determine which table rows are currently visible in that viewport.
        #-----------------------------------------------------------------------
        vPort = table.getParent()
        rect  = vPort.getViewRect()
        #-----------------------------------------------------------------------
        # We don't want to realign the viewport if the selected row is already
        # completely visible in the viewport.  So, check for this first.
        #-----------------------------------------------------------------------
        row = table.getSelectedRow()
        if row > -1 :
            cRect = table.getCellRect( row, 0, 1 )
            if rect.y <= cRect.y and rect.y + rect.height >= cRect.y + cRect.height :
                return
        #-----------------------------------------------------------------------
        # Partial rows are likely, so we want to realign the table, within the
        # viewport, to align either the top row with the top of the viewport, or
        # the bottom row with the bottom of the viewport, depending upon the
        # kind of direction key (i.e., Up, or Down) that was pressed.
        #-----------------------------------------------------------------------
        if self.up :
            first = table.rowAtPoint( Point( 0, rect.y ) )
            cell  = table.getCellRect( first, 0, 1 )
            diff  = rect.y - cell.y
        else :
            if row > -1 :
                cell  = table.getCellRect( row, 0, 1 )
            else :
                last  = table.rowAtPoint( Point( 0, rect.y + rect.height - 1 ) )
                cell  = table.getCellRect( last, 0, 1 )
            bot   = rect.y + rect.height
            end   = cell.y + cell.height
            diff  = end - bot
        point = vPort.getViewPosition() 
        vPort.setViewPosition(
            Point( point.x, point.y + diff )
        )

#-------------------------------------------------------------------------------
# Name: sectionFilter
# Role: Used to show & hide section contents
#-------------------------------------------------------------------------------
class sectionFilter( RowFilter ) :

    #---------------------------------------------------------------------------
    # Name: include()
    # Role: Returns true (1) if the row should be displayed
    # Note: For a JTable instance, entry.getIdentifier() == row number (index)
    #---------------------------------------------------------------------------
    def include( self, entry ) :
        model    = entry.getModel()
        result   = model.isVisible( entry.getIdentifier() )
        findText = model.getFindText()
        if findText :
            for col in range( entry.getValueCount() ) :
                if entry.getStringValue( col ).find( findText ) > -1 :
                    result = 1
                    break
        return result

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
        self.visible  = [ 1 ] * len( data )
        self.findText = None

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

    #---------------------------------------------------------------------------
    # Name: isVisible()
    # Role: Used by sectionFilter to determine if row should be visible
    #---------------------------------------------------------------------------
    def isVisible( self, row ) :
        return self.visible[ row ]

    #---------------------------------------------------------------------------
    # Name: getFindText()
    # Role: Text to find in data, if found, row is made visible
    #---------------------------------------------------------------------------
    def getFindText( self ) :
        return self.findText

    #---------------------------------------------------------------------------
    # Name: setFindText()
    # Role: Text to find in data, if found, row is made visible
    #---------------------------------------------------------------------------
    def setFindText( self, text ) :
        self.findText = text

    #---------------------------------------------------------------------------
    # Name: setVisible()
    # Role: Indicate whether the specified row is visible, or not
    #---------------------------------------------------------------------------
    def setVisible( self, row, trueFalse ) :
        self.visible[ row ] = trueFalse

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
        self.bg = [ None, None ]
        self.fg = [ None, None ]

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
        comp = DefaultTableCellRenderer.getTableCellRendererComponent(
            self, table, value, isSelected, hasFocus, row, col
        )
        #-----------------------------------------------------------------------
        # The first time we encounter the foreground & background colors for the
        # JLabel being used to display table cells (based upon isSelected), we
        # we need to save these colors.
        # Note: This is not the only way that this could have been done.
        #-----------------------------------------------------------------------
        if not self.bg[ isSelected ] :
            self.bg[ isSelected ] = comp.getBackground()
            self.fg[ isSelected ] = comp.getForeground()

        #-----------------------------------------------------------------------
        # Set the section heading row colors differently
        #-----------------------------------------------------------------------
        if table.getValueAt( row, 0 ).startswith( '_' ) :
            if isSelected :
                comp.setBackground( Color.yellow )
                comp.setForeground( Color.blue  )
            else :
                comp.setBackground( Color.blue )
                comp.setForeground( Color.white )
            comp.setFont( boldFont )
            metrics = fmBold 
        else :
            comp.setBackground( self.bg[ isSelected ] )
            comp.setForeground( self.fg[ isSelected ] )
            comp.setFont( plainFont )
            metrics = fmPlain

        if value :
            if col == 0 and value.startswith( '_' ) :
                value = value[ 1: ]
            tcm    = table.getColumnModel()      # Table Column Model
            width  = tcm.getColumn( col ).getWidth()
            height = table.getRowHeight( row )   # Cell height

            result, here, nl = '', '', ''
            offset = done = 0

            while not done :
                if metrics.stringWidth( here + value[ offset ] ) < width :
                    here += value[ offset ]
                    offset += 1
                else :
                    result += nl + here
                    here, nl = '', '\n'
                done = offset == len( value )

            result = ( result + nl + here )
            lines  = result.count( '\n' ) + 1
            rHeight = lines * table.getRowHeight()
            if rHeight > height :
                table.setRowHeight( row, rHeight )
            result = result.replace(
                '>', '&gt;'
            ).replace( '\n', '<br>' )
            findText = table.getModel().getFindText()
            if findText :
                if result.find( findText ) > -1 :
                    result = result.replace(
                        findText,
                        hilightHTML % findText
                    )
            value  = '<html>' + result.replace( ' ', '&nbsp;' )

        comp.setText( value )
        return comp

#-------------------------------------------------------------------------------
# Name: SecConfigReport_12()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class SecConfigReport_12( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: about()
    # Role: Used to display information about the script / application
    # Note: One way to display the script docstring (i.e., __doc__) as it
    #       appears is to use <html> text.
    # Note: The first character (i.e., [ 0 ]) is a newline, and is ignored
    #---------------------------------------------------------------------------
    def about( self, event ) :
        message = __doc__[ 1: ].replace( ' ', '&nbsp;' )
        message = message.replace( '<', '&lt;' )
        message = message.replace( '>', '&gt;' )
        message = message.replace( '\n', '<br>' )
        message = '<html>' + message
        message = JLabel(
            message,
            font = monoFont
        )
        JOptionPane.showMessageDialog(
                                       self.frame,
                                       message,
                                      'About',
                                       JOptionPane.PLAIN_MESSAGE
                                     )

    #---------------------------------------------------------------------------
    # Name: collapse()
    # Role: Event handler for Show -> Collapse All
    # Note: Only Section rows will be visible
    #---------------------------------------------------------------------------
    def collapse( self, event ) :
        table = self.table
        model = table.getModel()
        for row in range( model.getRowCount() ) :
            model.setVisible(
                row, 
                model.getValueAt( row, 0 ).startswith( '_' )
            )
        table.getRowSorter().setRowFilter(
            sectionFilter()
        )

    #---------------------------------------------------------------------------
    # Name: Exit()
    # Role: ActionListener event handler called when user selects Show -> Exit
    #---------------------------------------------------------------------------
    def Exit( self, event ) :
        sys.exit()

    #---------------------------------------------------------------------------
    # Name: expand()
    # Role: Event handler for Show -> Expand All
    #---------------------------------------------------------------------------
    def expand( self, event ) :
        table = self.table
        model = table.getModel()
        for row in range( model.getRowCount() ) :
            model.setVisible( row, 1 )
        table.getRowSorter().setRowFilter(
            sectionFilter()
        )

    #---------------------------------------------------------------------------
    # Name: Find()
    # Role: Event handler for Show -> Find...
    #---------------------------------------------------------------------------
    def Find( self, event ) :
        result = JOptionPane.showInputDialog(
            self.frame,                 # parentComponent
            'Text to be found:'         # message text
        )
        self.table.getModel().setFindText( result )
        self.table.getRowSorter().setRowFilter(
            sectionFilter()
        )

    #---------------------------------------------------------------------------
    # Name: frameResized()
    # Role: Component Listener event handler for the componentResized event
    #---------------------------------------------------------------------------
    def frameResized( self, ce ) :
        try :
            table  = self.table
            model  = table.getModel()       # Used to access the table data
            width  = table.getParent().getExtentSize().getWidth()

            pWidth = int( width ) >> 2
            tcm    = table.getColumnModel() # Table Column Model
            margin = tcm.getColumnMargin()  # gap between columns
            cols   = tcm.getColumnCount()
            for c in range( cols ) :
                col = tcm.getColumn( c )
                w = min( col.getMaxWidth, pWidth )
                col.setWidth( w )
                col.setPreferredWidth( w )

            #-------------------------------------------------------------------
            # Reset the individual row heights, so cell renderer can determine
            # the "right" height for each.
            # Note: The number of visible rows is determined by the filter, and
            #       is <= the total number of rows of data.  The try / except
            #       clause is a simple way to catch the "error" condition when
            #       we try to access an invisible row.
            #-------------------------------------------------------------------
            height = table.getRowHeight()
            for r in range( model.getRowCount() ) :
                try:
                    row = table.convertRowIndexToModel( r )
                    table.setRowHeight( row, height )
                except ArrayIndexOutOfBoundsException :
                    break

            #-------------------------------------------------------------------
            # Redraw the table using the new column widths and row heights
            #-------------------------------------------------------------------
            table.repaint()
        except :
            print 'Error: %s\nvalue: %s' % sys.exc_info()[ :2 ]

    #---------------------------------------------------------------------------
    # Name: MenuBar()
    # Role: Create the application menu bar
    #---------------------------------------------------------------------------
    def MenuBar( self ) :

        #-----------------------------------------------------------------------
        # Start by creating our application menubar
        #-----------------------------------------------------------------------
        menu = JMenuBar()

        #-----------------------------------------------------------------------
        # "Show" entry
        #-----------------------------------------------------------------------
        show = JMenu( 'Show' )

        show.add( JMenuItem( 'Collapse all', actionPerformed = self.collapse ) )
        show.add( JMenuItem( 'Expand all'  , actionPerformed = self.expand   ) )

        show.add( JSeparator() )
        show.add( JMenuItem( 'Find...'     , actionPerformed = self.Find ) )

        show.add( JSeparator() )
        show.add( JMenuItem( 'Exit'        , actionPerformed = self.Exit ) )
        menu.add( show )

        #-----------------------------------------------------------------------
        # "Help" entry
        #-----------------------------------------------------------------------
        help = JMenu( 'Help' )
        help.add( JMenuItem( 'About'       , actionPerformed = self.about  ) )
        help.add( JMenuItem( 'Notice'      , actionPerformed = self.notice ) )
        menu.add( help )

        return menu

    #---------------------------------------------------------------------------
    # Name: notice()
    # Role: Used to display important information
    #---------------------------------------------------------------------------
    def notice( self, event ) :
        JOptionPane.showMessageDialog(
            self.frame,
            Disclaimer,
            'Notice',                  # Previously "Disclaimer"
            JOptionPane.WARNING_MESSAGE
        )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'SecConfigReport_12',
            size = ( 500, 300 ),
            locationRelativeTo = None,
            componentResized = self.frameResized,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        #-----------------------------------------------------------------------
        # Add our menu bar to the frame
        #-----------------------------------------------------------------------
        frame.setJMenuBar( self.MenuBar() )

        data = []
        text = AdminTask.generateSecConfigReport()
        #-----------------------------------------------------------------------
        # The RegExp was added to replace multiple blanks with a single one
        #-----------------------------------------------------------------------
        for line in text.splitlines()[ 2: ] :
            data.append(
                [
                    re.sub( '  +', ' ', info.strip() )
                    for info in line[ :-2 ].split( ';' )
                ]
            )

        self.table = table = JTable(
            reportTableModel(
                data, ';;;'.split( ';' ),
            ),
            autoCreateRowSorter = 1,
            selectionMode = ListSelectionModel.SINGLE_SELECTION
        )

        for key in 'UP,DOWN,PAGE_UP,PAGE_DOWN,ctrl END'.split( ',' ) :
            upDownAction( table, key )

        table.setDefaultRenderer( String, reportRenderer() )
        self.setColumnWidths( table )
        scroller = JScrollPane( table )
        frame.add( scroller )

        frame.pack()
        frame.setVisible( 1 )
        frame.setMinimumSize( frame.getSize() )

    #---------------------------------------------------------------------------
    # Name: setColumnWidths()
    # Role: Compute, and set the preferred column widths and viewport size
    # Note: This table doesn't have a header row
    #---------------------------------------------------------------------------
    def setColumnWidths( self, table ) :
    
        #-----------------------------------------------------------------------
        # Set up some variables to access the table properties and data
        #-----------------------------------------------------------------------
        tcm    = table.getColumnModel()          # Table Column Model
        model  = table.getModel()                # Used to access the table data
        margin = tcm.getColumnMargin()           # gap between columns
    
        #-----------------------------------------------------------------------
        # For each column, determine the maximum width required
        #-----------------------------------------------------------------------
        rows = model.getRowCount()               # How many rows    exist?
        cols = tcm.getColumnCount()              # How many columns exist?

        labels = [
            JLabel( font = plainFont ),
            JLabel( font = boldFont  )
        ]

        metrics = [ fmPlain, fmBold ]
        tWidth = 0                               # Table width
        section = 0                              # Boolean: current row is a section?
        sections = 0                             # Number of setion rows
        #-----------------------------------------------------------------------
        # Note: Since the columns can't be rearranged, we can use the column #
        #       directly, instead of having to use the index (i.e.,
        #       col.getModelIndex()
        #-----------------------------------------------------------------------
        for c in range( cols ) :                 # Note: c == column number
            col = tcm.getColumn( c )
            #-------------------------------------------------------------------
            # Find the maximum width required for the data values in this column
            # Note: Use the column adjustments to compute the best width
            #-------------------------------------------------------------------
            cWidth = 0                           # Initial column width    
            for row in range( rows ) :
                v0  = model.getValueAt( row, 0 )
                if v0.startswith( '_' ) :
                    section = 1
                    if not c :                   # Only increment for col == 0
                        sections += 1
                else :
                    section = 0
                comp = labels[ section ]
                fm   = metrics[ section ]        # FontMetric
                r = table.getCellRenderer( row, c )
                v = model.getValueAt( row, c )
                if v.startswith( '_' ) :
                    v = v[ 1: ]
                comp.setText( v )
                cWidth = max( cWidth, comp.getPreferredSize().width )

            col.setMinWidth( 128 + margin )
            col.setPreferredWidth( 128 + margin )
            if cWidth > 0 :
                col.setMaxWidth( cWidth + margin )
    
            #-------------------------------------------------------------------
            # Add current column (preferred) width to the total table width
            #-------------------------------------------------------------------
            tWidth += col.getPreferredWidth()

        #-----------------------------------------------------------------------
        # Set the preferred viewport size
        #-----------------------------------------------------------------------
        table.setPreferredScrollableViewportSize(
            Dimension(
                tWidth,
                24 * table.getRowHeight()
            )
        )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( SecConfigReport_12() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f SecConfigReport_12.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
