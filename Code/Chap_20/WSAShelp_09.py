#-------------------------------------------------------------------------------
#    Name: WSAShelp_09.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: wsadmin Jython script to display wsadmin scripting object help text.
#          This iteration replaces the input field with a menu item as well as
#          adding Help -> About and Help -> Notice items.
#    Note: This requires a WebSphere Application Server environment.
#   Usage: wsadmin -f WSAShelp_09.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 13/01/11  rag  0.09  Chg - Move text input to menu item & add help items
# 13/01/11  rag  0.08  Add - Respond to table row selection events
# 13/01/11  rag  0.07  Add - highlighting to table text
# 13/01/02  rag  0.06  Add - Shows scripting object methods in a table
# 12/12/13  rag  0.05  Add - user specified text highlighting
# 12/12/12  rag  0.04  Add - tabbed pane event listener method tabPicked()
# 12/12/11  rag  0.03  Add - Separate the scripting object help from method help
# 12/12/10  rag  0.02  New - Add a tabbed pane
# 12/12/10  rag  0.01  New - Initial application
#-------------------------------------------------------------------------------

'''
Command: WSAShelp_09.py
Purpose: A wsadmin Jython script demonstrating some techniques for graphically
         displaying information about the wsadmin scripting objects using Java
         Swing components.
 Author: Robert A. (Bob) Gibson <bgibson@us.ibm.com>
   Note: This script is provided "AS IS". See the "Help -> Notice" for details.
  Usage: wsadmin -f WSAShelp_09.py
Example: ./wsadmin.sh -f WSAShelp_09.py\n
Version: 0.09
Updated: 30 Dec 2012
'''

import java
import re
import sys

#-------------------------------------------------------------------------------
# If SwingWorker doesn't exist, we have a problem...
#-------------------------------------------------------------------------------
try :
    from javax.swing import SwingWorker
except :
    print '\nThis application requires WebSphere Application Server verison 7.0 or higher.'
    sys.exit()

from   java.awt    import BorderLayout
from   java.awt    import Color
from   java.awt    import Dimension
from   java.awt    import EventQueue
from   java.awt    import Font
from   java.awt    import Toolkit

from   java.lang   import String

from   java.util   import Date

from   javax.swing import JDialog
from   javax.swing import JFrame
from   javax.swing import JLabel
from   javax.swing import JMenu
from   javax.swing import JMenuBar
from   javax.swing import JMenuItem
from   javax.swing import JPanel
from   javax.swing import JOptionPane
from   javax.swing import JSeparator
from   javax.swing import JScrollPane
from   javax.swing import JSplitPane
from   javax.swing import JTabbedPane
from   javax.swing import JTable
from   javax.swing import JTextArea
from   javax.swing import JTextField
from   javax.swing import JTextPane
from   javax.swing import ListSelectionModel

from   javax.swing.event import ListSelectionListener

from   javax.swing.table import DefaultTableCellRenderer
from   javax.swing.table import DefaultTableModel

from   javax.swing.text  import DefaultHighlighter

#-----------------------------------------------------------------------
# Font used to display help text
#-----------------------------------------------------------------------
monoFont = Font( 'Courier', Font.PLAIN, 12 )

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
# Name: cellSelector
# Role: Used to display the help text associated with the selected table cell
#-------------------------------------------------------------------------------
class cellSelector( ListSelectionListener ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    #---------------------------------------------------------------------------
    def __init__( self, table, WASobj ) :
        self.table  = table
        self.WASobj = WASobj
        self.objName = WASobj.help()[ :40 ].split( ' ' )[ 2 ]

    #---------------------------------------------------------------------------
    # Name: valueChanged()
    # Role: Event handler called when a table cell is selected
    #---------------------------------------------------------------------------
    def valueChanged( self, event ) :
        if not event.getValueIsAdjusting() :
            table = self.table
            row   = table.getSelectedRow()
            if row > -1 :
                method = table.getModel().getValueAt( row, 0 )
                title  = '%s.help( "%s" )' % ( self.objName, method )
                text   = self.WASobj.help( method )
                text   = JTextArea(
                    text,
                    20,
                    80,
                    font = monoFont
                )
                dialog = JDialog(
                    None,                  # owner
                    title,                 # title
                    1,                     # modal = true
                    layout = BorderLayout(),
                    locationRelativeTo = None
                )
                dialog.add(
                    JScrollPane(
                        text
                    ),
                    BorderLayout.CENTER
                )
                dialog.pack()
                dialog.setVisible( 1 )

#-------------------------------------------------------------------------------
# Name: methRenderer
# Role: Display the method table cells using the appropriate width & hilighting
# Note: It is used each time a cell must be displayed.
#-------------------------------------------------------------------------------
class methRenderer( DefaultTableCellRenderer ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    # Note: Instantiate a FontMetrics instance to be used to determine the size
    #       of the text to be displayed
    #---------------------------------------------------------------------------
    def __init__( self ) :
        self.fm = JLabel().getFontMetrics( monoFont )
        self.widths = [ 0, 0 ]
        self.hiText = ''

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
        # Name: camelWords()
        # Role: Return a list of words in the specified camelCase text
        #-----------------------------------------------------------------------
        def camelWords( name ) :
            prev, result = 0, []
            for i in range( len( name ) ) :
                ch = name[ i ]
                if ch == ch.upper() or ch == '_' :
                    result.append( name[ prev:i ] )
                    prev = i
            result.append( name[ prev: ] )
            return result

        #-----------------------------------------------------------------------
        # Start by retrieving the default renderer component (i.e., JLabel)
        #-----------------------------------------------------------------------
        comp = DefaultTableCellRenderer.getTableCellRendererComponent(
            self, table, value, isSelected, hasFocus, row, col
        )
        pWidth = self.widths[ col ]    # Preferred column width
        if pWidth :                    # Has it been set?
            #-------------------------------------------------------------------
            # Adjust the preferred width to keep ellipses from being displayed
            #-------------------------------------------------------------------
            pWidth -= 3
            if self.fm.stringWidth( value ) > pWidth :
                if col :
                    pad, words = ' ', value.split( ' ' )
                else :
                    pad, words = '', camelWords( value )
                result, curr = '<html>', ''
                for word in words :
                    if self.fm.stringWidth( curr + pad + word ) > pWidth :
                        result += curr + '<br>'
                        curr = ''
                    if curr :
                        curr += pad + word
                    else :
                        curr = word
                result += curr
                if self.hiText :
                    if value.count( self.hiText ) > 0 :
                        result = result.replace(
                            self.hiText,
                            '<font bgcolor=yellow>%s</font>' % self.hiText
                        )
                comp.setText( result )
            else :
                if self.hiText :
                    if value.count( self.hiText ) > 0 :
                        value = value.replace(
                            self.hiText,
                            '<font bgcolor=yellow>%s</font>' % self.hiText
                        )
                    comp.setText( '<html>' + value )
        return comp

    #---------------------------------------------------------------------------
    # Name: setHiText()
    # Role: Save the text to be hilighted during rendering, or an empty string
    #---------------------------------------------------------------------------
    def setHiText( self, text ) :
#       print 'setHiText( "%s" )' % text
        self.hiText = text

    #---------------------------------------------------------------------------
    # Name: setWidths()
    # Role: Return the component containing the rendered value
    #---------------------------------------------------------------------------
    def setWidths( self, width0, width1 ) :
#       print 'setWidths( %d, %d )' % ( width0, width1 )
        self.widths = [ width0, width1 ]

#-------------------------------------------------------------------------------
# Name: methodTableModel
# Role: Define table data characteristics
#-------------------------------------------------------------------------------
class methodTableModel( DefaultTableModel ) :

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
# Name: tableTask
# Role: Background processing of text parsing to produce 2D array of method
#       names and their associated description.
# Note: Instances of SwingWorker are not reusuable, new ones must be created.
#-------------------------------------------------------------------------------
class tableTask( SwingWorker ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    # Note: When this task completes, it will replace the bottom component of
    #       the specified splitPane with a JTable
    #---------------------------------------------------------------------------
    def __init__( self, helpText, splitPane, tPanes, WASobj ) :
        SwingWorker.__init__( self )
        self.helpText  = helpText      # Help text string to be processed
        self.splitPane = splitPane     # SplitPane to be updated
        self.tPanes    = tPanes        # tPanes list to be updated
        self.WASobj    = WASobj        # wsadmin scripting object

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Call the AdminConfig scripting object in the background
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        #-----------------------------------------------------------------------
        # Simplify local references
        #-----------------------------------------------------------------------
        helpText = self.helpText

        #-----------------------------------------------------------------------
        # Name: fix()
        # Role: Return massaged text, with newlines replaced by a space, and
        #       leading, trailing and extra spaces removed
        #-----------------------------------------------------------------------
        def fix( text ) :
            text = text.replace( '\n', ' ' ).strip()
            return re.sub( '  +', ' ', text )

        #-----------------------------------------------------------------------
        # The description starts immediately after the method / scripting object
        # name, and can span multiple lines.  To parse the text, we locate each
        # "method" name, and figure out its description text using it's position
        # in the overall helpText string.
        #-----------------------------------------------------------------------
        methRE = re.compile( r'^(\w+)(?:\s+.*)$', re.MULTILINE )
        result = []
        #-----------------------------------------------------------------------
        # If text matching the pattern is found, a Match Object (mo) is returned
        #-----------------------------------------------------------------------
        name, mo = None, methRE.search( helpText )
        while mo :
            start, finish = mo.span( 1 )
            #-------------------------------------------------------------------
            # Add a row, but only if a name exists
            #-------------------------------------------------------------------
            if name :
                result.append(
                    [
                        name,
                        fix( helpText[ prev : start ] )
                    ]
                )
            #-------------------------------------------------------------------
            # Extract method / scripting object name located by RegExp
            #-------------------------------------------------------------------
            name = helpText[ start : finish ]
            #-------------------------------------------------------------------
            # Next search starting offset...
            # Additionally, this is the start of the description text
            #-------------------------------------------------------------------
            prev = finish + 1
            #-------------------------------------------------------------------
            # Look for the next method name starting at specified offset
            #-------------------------------------------------------------------
            mo = methRE.search( helpText, finish )
        #-----------------------------------------------------------------------
        # If trailing descriptive text occurs after a name was found, add a row
        # to the array.
        #-----------------------------------------------------------------------
        if name :
            result.append( [ name, fix( helpText[ prev: ] ) ] )

        #-----------------------------------------------------------------------
        # Save the result as a object instance attribute
        #-----------------------------------------------------------------------
        self.data = result

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #       Replace specified container (i.e., JSplitPane) component with the
    #       resulting table
    # Note: When any cell / row is selected, the ListSelectionListener event
    #       handler is executed to display the help for the specified method
    #---------------------------------------------------------------------------
    def done( self ) :
        table = JTable(
            methodTableModel(
                self.data,
                [ 'Method', 'Description / Abstract' ],
            ),
            font = monoFont,
            autoResizeMode = JTable.AUTO_RESIZE_LAST_COLUMN,
            selectionMode = ListSelectionModel.SINGLE_SELECTION
        )
        table.getSelectionModel().addListSelectionListener(
            cellSelector(
                table,
                self.WASobj
            )
        )
        table.setDefaultRenderer( String, methRenderer() )
        table.getTableHeader().setReorderingAllowed( 0 )
        self.tPanes.extend( self.getTableInfo( table ) )
        self.splitPane.setBottomComponent(
            JScrollPane( table )
        )

    #---------------------------------------------------------------------------
    # Name: getTableInfo()
    # Role: Compute, and return the row height, column margin, and preferred
    #       column widths for
    #       the specified table
    #---------------------------------------------------------------------------
    def getTableInfo( self, table ) :
        #-----------------------------------------------------------------------
        # We know that the table has a header
        #-----------------------------------------------------------------------
        header = table.getTableHeader()
    
        #-----------------------------------------------------------------------
        # Variables used to access the table properties and data
        #-----------------------------------------------------------------------
        tcm    = table.getColumnModel()         # Table Column Model
        data   = table.getModel()               # To access table data
        margin = tcm.getColumnMargin()          # gap between columns

        result = [ table, table.getRowHeight() ]
        #-----------------------------------------------------------------------
        # For each column, determine the maximum width required
        #-----------------------------------------------------------------------
        rows = data.getRowCount()               # Number of rows
        cols = tcm.getColumnCount()             # Number of cols

        for i in range( cols ) :                # For col 0..N
            col = tcm.getColumn( i )            # TableColumn: col i
            idx = col.getModelIndex()           # model index: col i
    
            #-------------------------------------------------------------------
            # To determine the preferred column width, we
            # must use the current renderer for this column
            #-------------------------------------------------------------------
            render = col.getHeaderRenderer()    # header renderer
    
            #-------------------------------------------------------------------
            # Get preferred header width for column i
            #-------------------------------------------------------------------
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
            #-------------------------------------------------------------------
            # Compute the max width required for the data values in this column
            #-------------------------------------------------------------------
            for row in range( rows ) :
                val = str( data.getValueAt( row, idx ) )
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

            result.append( cWidth + margin )

        return result

#-------------------------------------------------------------------------------
# Name: WSAShelp_09()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class WSAShelp_09( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Class constructor
    #---------------------------------------------------------------------------
    def __init__( self ) :
        #-----------------------------------------------------------------------
        # Painter instance used to highlight text
        # Note: See hilightTextPane()
        #-----------------------------------------------------------------------
        self.painter = DefaultHighlighter.DefaultHighlightPainter(
           Color.YELLOW
        )
        #-----------------------------------------------------------------------
        # Input field containing the text to be highlighted
        #-----------------------------------------------------------------------
        self.textField = JTextField( '' )
        #-----------------------------------------------------------------------
        # Dictionary, indexed by tab name, with info about tab contents
        #-----------------------------------------------------------------------
        self.tPanes  = {}
        #-----------------------------------------------------------------------
        # Tabbed Pane for information to be displayed
        #-----------------------------------------------------------------------
        self.tabs = JTabbedPane(
            stateChanged = self.tabPicked
        )

    #---------------------------------------------------------------------------
    # Name: TBD()
    # Role: Indicate work that needs To Be Done
    #---------------------------------------------------------------------------
    def TBD( self, event ) :
        JOptionPane.showMessageDialog(
                                       self.frame,
                                       'Not yet implemented',
                                      'TBD',
                                       JOptionPane.PLAIN_MESSAGE
                                     )

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
    # Name: center()
    # Role: Position the frame in the center of the screen
    # Note: The frame isn't allowed to be wider than 1/2 the screen width, or
    #       more than 1/2 the screen height.  It is resized, if necessary.
    # Note: The value of 640 is used to keep the AdminTask.help() text from
    #       wrapping
    #---------------------------------------------------------------------------
    def center( self, frame ) :
        screenSize = Toolkit.getDefaultToolkit().getScreenSize()
        frameSize  = frame.getSize()
        frameSize.width  = min( frameSize.width , screenSize.width  >> 1 )
        frameSize.width  = max( frameSize.width , 640 )
        frameSize.height = min( frameSize.height, screenSize.height >> 1 )
        if frameSize != frame.getSize() :
            frame.setSize( frameSize )
        frame.setLocation(
            ( screenSize.width  - frameSize.width  ) >> 1,
            ( screenSize.height - frameSize.height ) >> 1
        )

    #---------------------------------------------------------------------------
    # Name: Exit()
    # Role: ActionListener event handler called when user selects Show -> Exit
    #---------------------------------------------------------------------------
    def Exit( self, event ) :
        sys.exit()

    #---------------------------------------------------------------------------
    # Name: frameResized()
    # Role: Component Listener event handler for the componentResized event
    #---------------------------------------------------------------------------
    def frameResized( self, ce ) :
        try :
            index = self.tabs.getSelectedIndex()
            name  = self.tabs.getTitleAt( index )
            if len( self.tPanes[ name ] ) > 1 :
                table, rowHeight, w0, w1 = self.tPanes[ name ][ 1: ]
                width  = table.getParent().getExtentSize().getWidth()
                tcm    = table.getColumnModel() # Table Column Model
                margin = tcm.getColumnMargin()  # gap between columns
                if w0 + w1 + 2 * margin > width :
                    table.setRowHeight( rowHeight * 3 )
                    c0 = int( round( width * .23 ) )
                    c1 = int( width - c0 - margin )
                else :
                    table.setRowHeight( rowHeight )
                    c0 = w0 + margin
                    c1 = int( width - c0 - margin )
                tcr = table.getCellRenderer( 0, 0 )
                tcr.setWidths( c0, c1 )
                tcr.setHiText( self.textField.getText() )
                tcm.getColumn( 0 ).setPreferredWidth( c0 )
                tcm.getColumn( 1 ).setPreferredWidth( c1 )
                #-------------------------------------------------------------------
                # Redraw the table using the new column widths and row heights
                #-------------------------------------------------------------------
                table.repaint()
        except :
            print '\nError: %s\nvalue: %s' % sys.exc_info()[ :2 ]

    #---------------------------------------------------------------------------
    # Name: hilightText()
    # Role: Event handler called by Show -> Highlight Text
    #---------------------------------------------------------------------------
    def hilightText( self, event ) :
       result = JOptionPane.showInputDialog(
           self.frame,                           # parentComponent
           'What text do you want to highlight?' # message text
       )
       if result != None :
           self.textField.setText( result )
           index = self.tabs.getSelectedIndex()
           name  = self.tabs.getTitleAt( index )
           self.hilightTextPane( self.tPanes[ name ][ 0 ], result )
           if len( self.tPanes[ name ] ) > 1 :
               table = self.tPanes[ name ][ 1 ]
               table.getCellRenderer( 0, 0 ).setHiText( result )
               table.repaint()

    #---------------------------------------------------------------------------
    # Name: hilightTextPane()
    # Role: Find, and highlight every occurrance of text on specified JTextPane
    #---------------------------------------------------------------------------
    def hilightTextPane( self, tPane, text ) :
        hiliter = tPane.getHighlighter()
        hiliter.removeAllHighlights()
        if text :
            doc   = tPane.getDocument()
            info  = doc.getText( 0, doc.getLength() )
            start = 0
            here  = info.find( text, start )
            while here > -1 :
                hiliter.addHighlight(
                    here,
                    here + len( text ),
                    self.painter
                )
                start = here + len( text )
                here  = info.find( text, start )

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

        show.add( JMenuItem( 'Highlight text', actionPerformed = self.hilightText ) )

        show.add( JSeparator() )
        show.add( JMenuItem( 'Exit'          , actionPerformed = self.Exit ) )
        menu.add( show )

        #-----------------------------------------------------------------------
        # "Help" entry
        #-----------------------------------------------------------------------
        help = JMenu( 'Help' )
        help.add( JMenuItem( 'About' , actionPerformed = self.about  ) )
        help.add( JMenuItem( 'Notice', actionPerformed = self.notice ) )
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
            'WSAShelp_09',
            layout = BorderLayout(),
            componentResized = self.frameResized,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        #-----------------------------------------------------------------------
        # RegExp used to locate method names
        #-----------------------------------------------------------------------
        methRE = re.compile( r'^(\w+)(?:\s+.*)$', re.MULTILINE )

        #-----------------------------------------------------------------------
        # Add our menu bar to the frame
        #-----------------------------------------------------------------------
        frame.setJMenuBar( self.MenuBar() )

        #-----------------------------------------------------------------------
        # Create & Populate the JTabbedPane
        #-----------------------------------------------------------------------
        WASobjs = [
            ( 'wsadmin'     , None         ),    # Special case
            ( 'Help'        , Help         ),
            ( 'AdminApp'    , AdminApp     ),
            ( 'AdminConfig' , AdminConfig  ),
            ( 'AdminControl', AdminControl ),
            ( 'AdminTask'   , AdminTask    )
        ]
        tabs = self.tabs
        for name, WASobj in WASobjs :
            #-------------------------------------------------------------------
            # Use a single ScrollPane for the AdminTask help
            #-------------------------------------------------------------------
            if name in [ 'wsadmin', 'AdminTask' ] :
                if WASobj :
                    data = WASobj.help().expandtabs()
                else :
                    data = Help.wsadmin().expandtabs()
                pane = JTextPane(
                    text = data,
                    editable = 0,
                    font = monoFont
                )
                #---------------------------------------------------------------
                # Move the caret to ensure that the starting text is shown
                #---------------------------------------------------------------
                pane.moveCaretPosition( 0 )
                tabs.addTab( name, JScrollPane( pane ) )
                self.tPanes[ name ] = [ pane ]
            else :
                #---------------------------------------------------------------
                # Use a RegExp to identify where the 1st method starts.
                #---------------------------------------------------------------
                text = WASobj.help().expandtabs()
                mo   = re.search( methRE, text ) # Match Object
                desc = text[ :mo.start( 1 ) ].strip()
                meth = text[ mo.start( 1 ): ].strip()
                #---------------------------------------------------------------
                # The description section is before the 1st method
                #---------------------------------------------------------------
                topPane = JTextPane(
                    text = desc,
                    editable = 0,
                    font = monoFont
                )
                topPane.moveCaretPosition( 0 )
                top = JScrollPane( topPane )
                #---------------------------------------------------------------
                # For the other scripting objects, use a vertically split pane
                # with the top containing the description section, and the
                # bottom (eventually) containing the method details.
                #---------------------------------------------------------------
                splitPane = JSplitPane(
                    JSplitPane.VERTICAL_SPLIT,
                    top,
                    JLabel( 'One moment please...' ),
                    resizeWeight = 0.5, # divider position = 50%
                    oneTouchExpandable = 1
                )
                #---------------------------------------------------------------
                # Start a separate thread to parse the method text and build a
                # a JTable to be put into the bottom part of this splitPane
                #---------------------------------------------------------------
                self.tPanes[ name ] = [ topPane ]
                tableTask(
                    meth,                   # Help text to be parsed / processed
                    splitPane,              # SplitPane to be updated
                    self.tPanes[ name ],    # tPanes entry to be updated
                    WASobj                  # WAS scripting object
                ).execute()
                tabs.addTab(
                    name,
                    splitPane
                )

        #-----------------------------------------------------------------------
        # Add the tabbed pane to the frame & show the result
        #-----------------------------------------------------------------------
        frame.add( tabs, 'Center' )

        frame.pack()
        self.center( frame )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: tabPicked()
    # Role: ChangeListener event handler - called when a tab is selected
    #---------------------------------------------------------------------------
    def tabPicked( self, event ) :
        pane  = event.getSource()
        index = pane.getSelectedIndex()
        name  = pane.getTitleAt( index )
        try :
            tPane = self.tPanes[ name ][ 0 ]
            tPane.select( 0, 0 )
            hiText = self.textField.getText()
            self.hilightTextPane( tPane, hiText )
            if len( self.tPanes[ name ] ) > 1 :
                table, rowHeight, w0, w1 = self.tPanes[ name ][ 1: ]
                #---------------------------------------------------------------
                # Viewport width & preferred width for column 0
                #---------------------------------------------------------------
                width  = table.getParent().getExtentSize().getWidth()
                tcm    = table.getColumnModel()   # Table Column Model
                margin = tcm.getColumnMargin()    # gap between columns
                if w0 + w1 + 2 * margin > width :
                    table.setRowHeight( rowHeight * 3 )
                    c0 = int( round( width * .23 ) )
                    c1 = int( width - c0 - margin )
                else :
                    table.setRowHeight( rowHeight )
                    c0 = w0 + margin
                    c1 = int( width - c0 - margin )
                tcr = table.getCellRenderer( 0, 0 )
                tcr.setWidths( c0, c1 )
                tcr.setHiText( hiText )
                tcm.getColumn( 0 ).setPreferredWidth( c0 )
                tcm.getColumn( 1 ).setPreferredWidth( c1 )
        except :
            Type, value = sys.exc_info()[ :2 ]
            Type, value = str( Type ), str( value )
            if not ( Type.endswith( 'KeyError' ) and value == 'wsadmin' ) :
                print '\nError: %s\nvalue: %s' % ( Type, value )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( WSAShelp_09() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f WSAShelp_09.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
