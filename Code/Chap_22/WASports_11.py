#-------------------------------------------------------------------------------
#    Name: WASports_10.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Display information about the ports configured within a cell
#    Note: This script requires a WebSphere Application Server environment
#   Usage: wsadmin -f WASports_10.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 14/04/19  rag  0.11  Add - Add Import functionality
# 14/04/19  rag  0.10  Add - Add Export functionality
# 14/04/19  rag  0.9   Add - Implement Save, Discard & Exit 
# 14/04/19  rag  0.8   Add - Add some simple menu items
# 14/04/19  rag  0.7   Fix - Compute preferred table column widths
# 14/04/19  rag  0.6   Add - Display port number info in right pane
# 14/04/19  rag  0.5   Add - Display cell & node info when selected
# 14/04/19  rag  0.4   Add - Selecting a tree item updates the right pane
# 14/04/19  rag  0.3   Add - Add the cell hierarchy tree to left side
# 14/04/19  rag  0.2   Add - Add a (vertically) split pane to the internal frame
# 14/04/19  rag  0.1   Add - Display the JFrame with an empty internal frame
# 14/04/19  rag  0.0   New - Initial iteration - simply display an empty Frame
#-------------------------------------------------------------------------------
'''
Command: WASports_11.py
Purpose: A wsadmin Jython script demonstrating various techniques to graphically
         display information about WebSphere Application Server port numbers.
 Author: Robert A. (Bob) Gibson <bgibson@us.ibm.com>
   Note: This script is provided "AS IS". See the "Help -> Notice" for details.
  Usage: wsadmin -f WASports_11.py
Example: ./wsadmin.sh -f WASports_11.py\n
Version: %(__version__)s
Updated: %(__updated__)s
'''

__version__ = '0.11'
__updated__ = '19 Apr 2014'

#-------------------------------------------------------------------------------
# Import the necessary Java, AWT, Swing, & Python library modules
#-------------------------------------------------------------------------------
import java

from   java.awt                   import Dimension
from   java.awt                   import EventQueue
from   java.awt                   import Font
from   java.awt                   import Point
from   java.awt                   import Toolkit

from   java.awt.event             import WindowAdapter

from   java.io                    import File
from   java.io                    import FileInputStream
from   java.io                    import FileOutputStream
from   java.io                    import InputStreamReader
from   java.io                    import OutputStreamWriter

from   java.lang                  import Integer
from   java.lang                  import String
from   java.lang                  import System

from   javax.swing                import JDesktopPane
from   javax.swing                import JFileChooser
from   javax.swing                import JFrame
from   javax.swing                import JLabel
from   javax.swing                import JInternalFrame
from   javax.swing                import JMenu
from   javax.swing                import JMenuBar
from   javax.swing                import JMenuItem
from   javax.swing                import JOptionPane
from   javax.swing                import JScrollPane
from   javax.swing                import JSeparator
from   javax.swing                import JSplitPane
from   javax.swing                import JTable
from   javax.swing                import JTree
from   javax.swing                import ListSelectionModel

from   javax.swing.event          import InternalFrameListener
from   javax.swing.event          import TreeSelectionListener

from   javax.swing.table          import DefaultTableModel

from   javax.swing.tree           import DefaultMutableTreeNode
from   javax.swing.tree           import TreePath
from   javax.swing.tree           import TreeSelectionModel

from   javax.swing.filechooser    import FileFilter

from   javax.xml.parsers          import SAXParserFactory

# XML Transformation classes - see ExportTask
from   javax.xml.transform        import OutputKeys
from   javax.xml.transform.sax    import SAXTransformerFactory
from   javax.xml.transform.stream import StreamResult

from   org.xml.sax                import InputSource
from   org.xml.sax.helpers        import AttributesImpl
from   org.xml.sax.helpers        import DefaultHandler

import os

from   os.path                    import abspath
from   os.path                    import exists
from   os.path                    import normpath

from   socket                     import gethostbyname

import sys

import threading

import time

#-------------------------------------------------------------------------------
# If SwingWorker doesn't exist, we have a problem...
#-------------------------------------------------------------------------------
try :
    from javax.swing import SwingWorker
except :
    print '\nThis script requires WebSphere Application Server verison 7.0 or higher.'
    sys.exit()

#-------------------------------------------------------------------------------
# Define the Font constant to be used throughout the application
#-------------------------------------------------------------------------------
MONOFONT = Font( 'Monospaced', Font.PLAIN, 14 )

#-------------------------------------------------------------------------------
# Encoding used by XML processing routines (i.e., ImportTask & ExportTask)
#-------------------------------------------------------------------------------
# ENCODING = 'UTF-8'
ENCODING = 'ISO-8859-1'

#-------------------------------------------------------------------------------
# Define the format strings used to display Cell & Node details
#-------------------------------------------------------------------------------
CELLINFO = '''
    Cell: %(cellName)s
    Home: %(WAShome)s
 Version: %(WASversion)s
 Profile: %(profile)s
'''

NODEINFO = '''
    Cell: %(cellName)s
    Node: %(nodeName)s
    Home: %(WAShome)s
 Version: %(WASversion)s
 Profile: %(profile)s
Hostname: %(hostnames)s
 IP addr: %(ipaddr)s
'''

#-------------------------------------------------------------------------------
# Define the Disclaimer message used by Help -> Notice
#-------------------------------------------------------------------------------
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
# Define the contents of the required DTD file in case one needs to be created
#-------------------------------------------------------------------------------
DTD = '''
<!ELEMENT WASports   (cell)>
<!ATTLIST WASports   version CDATA #REQUIRED>
<!ELEMENT cell       (name,WAShome,WASversion,profile,node+)>
<!ELEMENT node       (name,WAShome,WASversion,profile,hostname+,ipaddr,server+)>
<!ELEMENT server     (name,endpoint+)>
<!ELEMENT name       (#PCDATA)>
<!ELEMENT WAShome    (#PCDATA)>
<!ELEMENT WASversion (#PCDATA)>
<!ELEMENT profile    (#PCDATA)>
<!ELEMENT hostname   (#PCDATA)>
<!ELEMENT ipaddr     (#PCDATA)>
<!ELEMENT endpoint   (name,port)>
<!ELEMENT port       (#PCDATA)>
'''

#-------------------------------------------------------------------------------
# Name: appCleanup()
# Role: Called during exit processing to clean up application data structures
# Note: "frame" is expected to be a reference to the application frame
#-------------------------------------------------------------------------------
def appCleanup( frame ) :
    if AdminConfig.hasChanges() :
        answer = JOptionPane.showInternalConfirmDialog(
            frame.getContentPane(),
            'Save changes?'
        )
        if answer == JOptionPane.YES_OPTION :
            AdminConfig.save()
        elif answer in [ JOptionPane.CLOSED_OPTION, JOptionPane.CANCEL_OPTION ] :
            return
        else :
            AdminConfig.reset()
            print '\nConfiguration changes discarded.'
    System.gc()              # Ask the Java Garbage Collector to clean up
    time.sleep( 0.5 )        # Slight delay to give GC time to complete
    #---------------------------------------------------------------------------
    # Even wrapping sys.exit() in a try / except block doesn't keep any
    # exception messages from being displayed, so don't bother trying
    # (pun intended)
    #---------------------------------------------------------------------------
    sys.exit( 0 )

#-------------------------------------------------------------------------------
#  Name: findScopedTypes()
#  Role: Return the list of configuration IDs for resources of the specified
#        type having a given attribute value, within an optional scope.
#  Note: Passing a scope of None is just like not specifying one.
#      - Default attr value is "name"
# Usage: To find all servers having a name of "server1"
#        servers = findScopedTypes( 'Server', 'server1' )
#-------------------------------------------------------------------------------
def findScopedTypes( Type, value, scope = None, attr = None ) :
    if not attr :
        attr = 'name'
    return [
        x for x in AdminConfig.list( Type, scope ).splitlines()
        if AdminConfig.showAttribute( x, attr ) == value
    ]

#-------------------------------------------------------------------------------
#  Name: firstNamedConfigType()
#  Role: To return the first configId of the resource of the specified Type
#        having the specified attribute value.
#  Note: Passing a scope of None is just like not specifying one.
#        Default value of attr is "name"
# Usage: ...
#        server = firstNamedConfigType( 'Server', 'server1' )
#        if server :
#          # Do something with server resource
#          ...
#        else :
#          ...
#-------------------------------------------------------------------------------
def firstNamedConfigType(
    Type, value, scope = None, attr = None
) :
    items = findScopedTypes( Type, value, scope, attr )
    if len( items ) :
        result = items[ 0 ]
    else :
        result = None
    return result

#-------------------------------------------------------------------------------
# Name: getAttributeValue()
# Role: Return the specified attribute value from the given configuration object
# Note: cfgId = configuration ID for configuration object
#       name  = the attribute name to be returned
#-------------------------------------------------------------------------------
def getAttributeValue( cfgId, attr  ) :
    return AdminConfig.showAttribute( cfgId, attr )

#-------------------------------------------------------------------------------
# Name: getIPaddresses( hostnames )
# Role: Return the list of unique IP addresses for the specified hostnames
# Note: The list of hostnames may include aliases.  The result will contain the
#       list of unique IP addresses without duplicates.
#-------------------------------------------------------------------------------
def getIPaddresses( hostnames ) :
    result = []
    for hostname in hostnames :
        try :
            addr = gethostbyname( hostname )
            if addr not in result :
                result.extend( addr.split( ',' ) )
        except :
            pass
    return result

#-------------------------------------------------------------------------------
# Name: getHostnames( nodeName, serverName )
# Role: Return the list of hostnames configured for the specified server
# Note: exclude identifies the hostnames & ip addresses to be ignored
# Note: 232.133.104.73 == Node agent IPv4 multicast address
#       ff01::1        == Node agent IPv6 multicase address
#-------------------------------------------------------------------------------
def getHostnames( nodeName, serverName ) :
    exclude = [
        '*',
        'localhost',
        '${LOCALHOST_NAME}',
        '232.133.104.73',
        'ff01::1'
    ]
    result = []
    node   = firstNamedConfigType( 'Node', nodeName )
    server = firstNamedConfigType(
        'ServerEntry',
        serverName,
        node,
        'serverName'
    )
    NEPs = AdminConfig.list( 'NamedEndPoint', server )
    for nep in NEPs.splitlines() :
        epId = getAttributeValue( nep, 'endPoint' )
        host = getAttributeValue( epId, 'host' )
        if host not in exclude :
            result.append( host )
            exclude.append( host )
    return result

#-------------------------------------------------------------------------------
# Name: setColumnWidths()
# Role: Set the preferred column widths so "..." aren't used by the renderer
# Note: This code takes advantage of known table characteristics
#-------------------------------------------------------------------------------
def setColumnWidths( table ) :

    #---------------------------------------------------------------------------
    # Variables used to access the table properties and data
    #---------------------------------------------------------------------------
    tcm    = table.getColumnModel()    # Table Column Model
    data   = table.getModel()          # To access table data
    margin = tcm.getColumnMargin()     # gap between columns

    #---------------------------------------------------------------------------
    # Preferred width of Port number column
    #---------------------------------------------------------------------------
    render = table.getCellRenderer( 0, 0 )
    comp = render.getTableCellRendererComponent(
        table,                         # table being processed
        '65535',                       # max port number
        0,                             # not selected
        0,                             # not in focus
        0,                             # row num
        0                              # col num
    )
    cWidth = comp.getPreferredSize().width

    col = tcm.getColumn( 0 )
    col.setPreferredWidth( cWidth + margin )

    #---------------------------------------------------------------------------
    # Compute the max width required for the data values in this column
    #---------------------------------------------------------------------------
    cWidth = -1
    for row in range( data.getRowCount() ) :
        render = table.getCellRenderer( row, 1 )
        comp = render.getTableCellRendererComponent(
            table,
            data.getValueAt( row, 1 ),   # cell value
            0,                           # not selected
            0,                           # not in focus
            row,                         # row num
            1                            # col num
        )
        cWidth = max(
            cWidth,
            comp.getPreferredSize().width
        )
    #---------------------------------------------------------------------------
    # Preferred width of "Named Endpoint" column
    #---------------------------------------------------------------------------
    col = tcm.getColumn( 1 )
    col.setPreferredWidth( cWidth + margin )

#-------------------------------------------------------------------------------
# Name: WASversion()
# Role: Return the version of WebSphere for the specified id, which should be
#       either a Node, or Cell configId
#-------------------------------------------------------------------------------
def WASversion( id ) :
    if AdminConfig.getObjectType( id ) == 'Cell' :
        nodeName = System.getProperty( 'local.node' )
    else :
        nodeName = getAttributeValue( id, 'name' )
    return AdminTask.getNodeBaseProductVersion(
        '[-nodeName %s]' % nodeName
    )

#-------------------------------------------------------------------------------
# Name: WASprofileName()
# Role: Return the name of the current profile, or None
#-------------------------------------------------------------------------------
def WASprofileName( id ) :
    result = WASvarLookup( id, 'USER_INSTALL_ROOT' )
    if result :
        result = result.split( os.sep )[ -1 ]
    return result

#-------------------------------------------------------------------------------
# Name: WAShome()
# Role: Return the value of the WAS_INSTALL_ROOT variable, or None
#-------------------------------------------------------------------------------
def WAShome( id ) :
    return WASvarLookup( id, 'WAS_INSTALL_ROOT' )

#-------------------------------------------------------------------------------
# Name: WASvarLookup()
# Role: Return the specified value of the indicated WAS variable
#-------------------------------------------------------------------------------
def WASvarLookup( id, name ) :
    VSE = AdminConfig.list( 'VariableSubstitutionEntry', id )
    for var in VSE.splitlines () :
        if getAttributeValue( var, 'symbolicName' ) == name :
            result = getAttributeValue( var, 'value' )
            break
    else :
        result = None
    return result

#-------------------------------------------------------------------------------
# Name: cellInfo
# Role: Serialized class for holding cell information
# Note: An internal frame is used to display the information contained herein
#-------------------------------------------------------------------------------
class cellInfo :

    #---------------------------------------------------------------------------
    # class lock used for serialization
    #---------------------------------------------------------------------------
    lock = threading.Lock()

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    # Note: The index of names & info dictionaries is a node name for branch
    #       nodes, or the ( nodeName, serverName ) tuple for leaf nodes
    #---------------------------------------------------------------------------
    def __init__( self, debug = 0 ) :
        self.names      = {}       # Dictionary[ tuple ] -> configId
        self.infoDict   = {}       # Dictionary[ name ]  -> node details
        self.infoText   = {}       # Dictionary[ name ]  -> HTML text string
        self.portTables = {}       # Dictionary[ index ] -> server JTable()
        self.before     = {}       # Dictionary[ index ] -> original port value
        self.tree       = None     # JTree() associated with this data
        self.cellName   = None
        self.debug      = debug

    #---------------------------------------------------------------------------
    # Name: addOriginal()
    # Role: before "setter" - used to add a new "original" port value
    # Note: "before" is a dictionary containing the original port values
    #  See: PortTableModel.setValueAt()
    # Note: Only the first "original" value is saved.  Subsequent changes are
    #       ignored.
    #---------------------------------------------------------------------------
    def addOriginal( self, table, row, value ) :
        if self.debug :
            print 'addOriginal( row = "%d", value = "%s" )' % ( row, value )
        self.lock.acquire()
        index = ( table, row )
        if not self.before.has_key( index ) :
            self.before[ index ] = value
        self.lock.release()

    #---------------------------------------------------------------------------
    # Name: getOriginal()
    # Role: before getter
    # Note: "before" is a dictionary containing the original port values
    #  See: PortTableModel.setValueAt()
    #---------------------------------------------------------------------------
    def getOriginal( self ) :
        self.lock.acquire()
        result = self.before
        self.lock.release()
        if self.debug :
            print 'getOriginal():', result
        return result

    #---------------------------------------------------------------------------
    # Name: clearOriginals()
    # Role: before setter - set to empty
    #---------------------------------------------------------------------------
    def clearOriginals( self ) :
        self.lock.acquire()
        self.before = {}
        self.lock.release()
        if self.debug :
            print 'clearOriginals()'

    #---------------------------------------------------------------------------
    # Name: hasChanges()
    # Role: Return true (1) if port changes have been made false (0) otherwise
    #---------------------------------------------------------------------------
    def hasChanges( self ) :
        self.lock.acquire()
        result = self.before != {}
        self.lock.release()
        if self.debug :
            print 'hasChanges():', result
        return result

    #---------------------------------------------------------------------------
    # Name: getCellName()
    # Role: cellName getter
    #---------------------------------------------------------------------------
    def getCellName( self ) :
        self.lock.acquire()
        result = self.cellName
        self.lock.release()
        if self.debug :
            print 'getCellName():', result
        return result

    #---------------------------------------------------------------------------
    # Name: setCellName()
    # Role: cellName setter
    #---------------------------------------------------------------------------
    def setCellName( self, cellName ) :
        self.lock.acquire()
        self.cellName = cellName
        self.lock.release()
        if self.debug :
            print 'setCellName( "%s" ):' % cellName

    #---------------------------------------------------------------------------
    # Name: getNames()
    # Role: names getter
    # Note: names is index by ( nodeName, serverName ) tuple, to identify
    #       the indicated server configId value
    #---------------------------------------------------------------------------
    def getNames( self ) :
        self.lock.acquire()
        result = self.names
        self.lock.release()
        if self.debug :
            print 'getNames():', result
        return result

    #---------------------------------------------------------------------------
    # Name: setNames()
    # Role: names setter
    # Note: names is index by ( nodeName, serverName ) tuple, to identify
    #       the indicated server configId value
    #---------------------------------------------------------------------------
    def setNames( self, names ) :
        self.lock.acquire()
        self.names = names
        self.lock.release()
        if self.debug :
            print 'setNames():', names

    #---------------------------------------------------------------------------
    # Name: addInfoData()
    # Role: Add the specified information to the instance attributes
    # Note: data         : a dictionary of values
    #       formatString : the formatString used to create formatted output
    #  See: Global CELLINFO format string constant
    #---------------------------------------------------------------------------
    def addInfoData( self, index, formatString, data ) :
        self.lock.acquire()
        self.infoDict[ index ] = data
        textString = formatString % data
        self.infoText[ index ] = '<html>' + (
            textString.replace(
                '&', '&amp;'
            ).replace(
                '<', '&lt;'
            ).replace(
                '>', '&gt;'
            ).replace(
                ' ', '&nbsp;'
            ).replace(
                '\n', '<br/>'
            )
        )
        self.lock.release()
        if self.debug :
            print 'addInfoData( "%s" )' % index

    #---------------------------------------------------------------------------
    # Name: getInfoDict()
    # Role: Retrieve data dictionary for the specified index
    # Note: Using get() means this won't raise a KeyError, so result == None
    #---------------------------------------------------------------------------
    def getInfoDict( self, index ) :
        self.lock.acquire()
        result = self.infoDict.get( index )
        self.lock.release()
        if self.debug :
            print 'getInfoDict( "%s" )' % str( index )
        return result

    #---------------------------------------------------------------------------
    # Name: getInfoText()
    # Role: Retrieve html text string associated with specified index
    # Note: info contains formatted HTML text about the specified cell/node
    #---------------------------------------------------------------------------
    def getInfoText( self, index ) :
        self.lock.acquire()
        result = self.infoText[ index ]
        self.lock.release()
        if self.debug :
            print 'getInfoText( "%s" )' % str( index )
        return result

    #---------------------------------------------------------------------------
    # Name: addPortTable()
    # Role: Ports value adder
    # Note: index == ( nodeName, serverName ) tuple
    #       value == JTable instance
    #---------------------------------------------------------------------------
    def addPortTable( self, index, value ) :
        self.lock.acquire()
        self.portTables[ index ] = value
        self.lock.release()
        if self.debug :
            print 'addPortTable( "%s" )' % str( index )

    #---------------------------------------------------------------------------
    # Name: getPortTables()
    # Role: portTables (dicationary) getter
    #---------------------------------------------------------------------------
    def getPortTables( self ) :
        self.lock.acquire()
        result = self.portTables
        self.lock.release()
        if self.debug :
            print 'getPortTables()'
        return result

    #---------------------------------------------------------------------------
    # Name: getPortTable()
    # Role: portTables value getter, a JTable instance or None is returned
    # Note: The index should be a ( nodeName, serverName ) tuple
    #---------------------------------------------------------------------------
    def getPortTable( self, index ) :
        self.lock.acquire()
        result = self.portTables.get( index )
        self.lock.release()
        if self.debug :
            print 'getPortTable( "%s" )' % str( index )
        return result

    #---------------------------------------------------------------------------
    # Name: getTree()
    # Role: Tree getter
    # Note: Tree is the JTree associated with this structure
    #---------------------------------------------------------------------------
    def getTree( self ) :
        self.lock.acquire()
        result = self.tree
        self.lock.release()
        if self.debug :
            print 'getTree()'
        return result

    #---------------------------------------------------------------------------
    # Name: setTree()
    # Role: Tree setter
    # Note: Tree is the JTree associated with this structure
    #---------------------------------------------------------------------------
    def setTree( self, tree ) :
        self.lock.acquire()
        self.tree = tree
        self.lock.release()
        if self.debug :
            print 'setTree()'

    #---------------------------------------------------------------------------
    # Name: setDebugEnabled()
    # Role: Set the instance value of debug variable
    # Note: debug should be true (1) or false (0)
    #---------------------------------------------------------------------------
    def setDebugEnabled( self, debug ) :
        self.debug = debug

    #---------------------------------------------------------------------------
    # Name: isDebugEnabled()
    # Role: Retrieve the instance value of debug variable
    #---------------------------------------------------------------------------
    def isDebugEnabled( self, debug ) :
        return self.debug

#-------------------------------------------------------------------------------
# Name: cellTSL
# Role: TreeSelectionListener for cell hierarchy tree
#-------------------------------------------------------------------------------
class cellTSL( TreeSelectionListener ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    # Note: pane is a reference to the split pane to be updated based upon the
    #       user selection
    # Note: data is the cellInfo object instance; e.g., see getLocalCellInfo()
    #---------------------------------------------------------------------------
    def __init__( self, tree, pane, data ) :
        self.tree = tree
        self.pane = pane     # JSplitPane Reference
        self.data = data

    #---------------------------------------------------------------------------
    # Name: valueChanged()
    # Role: TreeSelectionListener method called when a selection event occurs
    # Note: Event handlers should perform a minimum amount of processing.
    #---------------------------------------------------------------------------
    def valueChanged( self, tse ) :
        pane = self.pane
        loc  = pane.getDividerLocation()

        node = self.tree.getLastSelectedPathComponent()
        if node :
            if node.isLeaf() :
                pane.setRightComponent (
                    JScrollPane(
                      self.data.getPortTable(
                          (
                              str( node.getParent() ),
                              str( node )
                          )
                      )
                  )
                )
            else :
                pane.setRightComponent (
                    JScrollPane(
                        JLabel(
                            self.data.getInfoText( str( node ) ),
                            font = MONOFONT
                        )
                    )
                )
        else :
            pane.setRightComponent (
                JScrollPane(
                    JLabel(
                        '<html><br/><b>Nothing selected<b/>',
                        font = MONOFONT
                    )
                )
            )
        pane.setDividerLocation( loc )

#-------------------------------------------------------------------------------
# Name: InternalFrame
# Role: Class for all internal frames
# Note: We can't use InternalFrameAdapter, using InternalFrameListener instead
#-------------------------------------------------------------------------------
class InternalFrame(
    JInternalFrame,
    InternalFrameListener
) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    #---------------------------------------------------------------------------
    def __init__(
        self,
        title,
        size,
        location,
        cellData,
        app,
        closable = 0,
        debug = 0
    ) :
        JInternalFrame.__init__(
            self,
            title,
            resizable   = 1,
            closable    = closable,
            maximizable = 1,
            iconifiable = 1,
            size        = size,
            internalFrameListener = self
        )
        self.setLocation( location )
        self.cellData = cellData
        self.app      = app
        self.title    = title
        self.debug    = debug

        #-----------------------------------------------------------------------
        # Build the split pane using the JTree reference from the cellInfo
        # instance.
        #-----------------------------------------------------------------------
        tree = cellData.getTree()
        self.status = JLabel(
            'Nothing selected',
            font = MONOFONT
        )
        pane = self.add(
            JSplitPane(
                JSplitPane.HORIZONTAL_SPLIT,
                JScrollPane( tree ),
                JScrollPane( self.status )
            )
        )
        if app.localFrame :
            loc = app.localFrame.getSplitPane().getDividerLocation()
        else :
            loc = size.width >> 1
        pane.setDividerLocation( loc )
        self.setSplitPane( pane )
        #-----------------------------------------------------------------------
        # The tree selection listener updates the right pane
        #-----------------------------------------------------------------------
        tree.addTreeSelectionListener(
            cellTSL(
                tree,
                pane,
                cellData
            )
        )
        self.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: getCellData()
    # Role: Return a reference to the cellData instance
    #---------------------------------------------------------------------------
    def getCellData( self ) :
        return self.cellData

    #---------------------------------------------------------------------------
    # Name: getSplitPane()
    # Role: Return a reference to the SplitPane within the internal frame
    #---------------------------------------------------------------------------
    def getSplitPane( self ) :
        return self.pane

    #---------------------------------------------------------------------------
    # Name: setSplitPane()
    # Role: Save a reference to the SplitPane within the internal frame
    #---------------------------------------------------------------------------
    def setSplitPane( self, pane ) :
        self.pane = pane

    #---------------------------------------------------------------------------
    # Name: internalFrameActivated()
    # Role: Update Portzilla.inner to reference active InternalFrame
    # Note: Invoked when an internal frame is activated.
    #---------------------------------------------------------------------------
    def internalFrameActivated( self, e ) :
        frames = self.app.frames
        for frame, fileName in frames :
            if frame == self :
                if self.debug :
                    print '  Activated( "%s" )' % self.title
                self.app.setActiveFrame( self )
                self.app.ChangesMI.setEnabled(
                    self.getCellData().hasChanges()
                )
                break
        else :
            print '\ninternalFrameClosed() Error - frame not found!'

    #---------------------------------------------------------------------------
    # Name: internalFrameClosed()
    # Role: Update Portzilla.inner to remove closed InternalFrame
    # Note: Invoked when an internal frame has been closed.
    #---------------------------------------------------------------------------
    def internalFrameClosed( self, e ) :
        frames = self.app.frames
        for item in frames :
            if item[ 0 ] == self :
                if self.debug :
                    print '     Closed( "%s" )' % self.title
                frames.remove( item )
                break
        else :
            print '\ninternalFrameClosed() Error - frame not found!'

    #---------------------------------------------------------------------------
    # Name: internalFrameClosing()
    # Note: Invoked when an internal frame is in the process of being closed.
    #---------------------------------------------------------------------------
    def internalFrameClosing( self, e ) :
        if self.debug :
            print '    Closing( "%s" )' % self.title
        cellData = self.getCellData()
        if cellData.hasChanges() :
            for frame, fileName in self.app.frames :
                if frame == self :
                    if fileName :
                        #-------------------------------------------------------
                        # It's possible (although unlikely) that the file no
                        # longer exists.  If it does, get permission to replace
                        #-------------------------------------------------------
                        if os.path.isfile( fileName ) :
                            response = JOptionPane.showInternalConfirmDialog(
                                self.app.getDesktop(),
                               'Overwrite existing file: %s?' % fileName,
                               'Confirm Overwrite',
                                JOptionPane.YES_NO_OPTION,
                                JOptionPane.QUESTION_MESSAGE
                            )
                            if response == JOptionPane.NO_OPTION :
                                return
                        #-------------------------------------------------------
                        # For an imported instance, "Save" is actually an Export
                        #-------------------------------------------------------
                        ExportTask(
                            self.app,
                            None,
                            cellData,
                            fileName,
                            cleanup = 1
                        ).execute()
                    else :
                        JOptionPane.showInternalMessageDialog(
                            self.app.getDesktop(),
                            'Attempt to "Close" local frame',
                            'Unexpected error',
                            JOptionPane.ERROR_MESSAGE,
                            None
                        )
                    break

    #---------------------------------------------------------------------------
    # Name: internalFrameDeactivated()
    # Note: Invoked when an internal frame is de-activated.
    #---------------------------------------------------------------------------
    def internalFrameDeactivated( self, e ) :
        self.app.setActiveFrame( None )
        self.app.ChangesMI.setEnabled( 0 )
        if self.debug :
            print 'Deactivated( "%s" )' % self.title

    #---------------------------------------------------------------------------
    # Name: internalFrameDeiconified()
    # Note: Invoked when an internal frame is de-iconified.
    #---------------------------------------------------------------------------
    def internalFrameDeiconified( self, e ) :
        if self.debug :
            print 'Deiconified( "%s" )' % self.title

    #---------------------------------------------------------------------------
    # Name: internalFrameIconified()
    # Note: Invoked when an internal frame is iconified.
    #---------------------------------------------------------------------------
    def internalFrameIconified( self, e ) :
        if self.debug :
            print '  Iconified( "%s" )' % self.title

    #---------------------------------------------------------------------------
    # Name: internalFrameOpened()
    # Note: Invoked when a internal frame has been opened.
    #---------------------------------------------------------------------------
    def internalFrameOpened( self, e ) :
        if self.debug :
            print '     Opened( "%s" )' % self.title
        self.requestFocusInWindow()

#-------------------------------------------------------------------------------
# Name: AboutTask
# Role: Background processing of potentially long running task to process the
#       script docstring (i.e., __doc__) to create the HTML version of it.
# Note: This class is only executed once.
#-------------------------------------------------------------------------------
class AboutTask( SwingWorker ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor - save a reference to the associated menu item
    #---------------------------------------------------------------------------
    def __init__( self, menuItem ) :
        self.menuItem = menuItem

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Convert script docstring to HTML
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        text    = __doc__[ 1: ] % globals()
        message = text.replace( ' ', '&nbsp;' )
        message = message.replace( '<', '&lt;' )
        message = message.replace( '>', '&gt;' )
        message = message.replace( '\n', '<br>' )
        self.result = '<html>' + message

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Enable the associated menuItem
    #---------------------------------------------------------------------------
    def done( self ) :
        self.menuItem.setEnabled( 1 )

    #---------------------------------------------------------------------------
    # Name: getResult()
    # Role: Return the HTML form of the application docstring
    #---------------------------------------------------------------------------
    def getResult( self ) :
        return self.result

#-------------------------------------------------------------------------------
# Name: SaveTask
# Role: Execute a potentially long running AdminConfig.save() call so the GUI
#       doesn't appear to be "hung".
# Note: Instances of SwingWorker are not reusuable; new ones must be created.
#-------------------------------------------------------------------------------
class SaveTask( SwingWorker ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    # Note: The associated menu item is disabled so multiple threads can't be
    #       running at the same time for the same activeFrame.
    #---------------------------------------------------------------------------
    def __init__( self, app, menuItem, cellData ) :
        self.app      = app
        self.menuItem = menuItem
        self.cellData = cellData
        self.msgText  = None
        menuItem.setEnabled( 0 )

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Call AdminConfig.save()
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        try :
            AdminConfig.save()
            original = self.cellData.clearOriginals()
        except :
            self.msgText = 'Error: %s\nvalue: %s' % sys.exc_info()[ :2 ]

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Display any error message in an internal dialog box, if any was
    #       encountered
    # Note: The specified menuItem is enabled only if more changes exist
    #---------------------------------------------------------------------------
    def done( self ) :
        if self.msgText :
            JOptionPane.showInternalMessageDialog(
                self.app.getDesktop(),
                self.msgText,
                'SaveTask() Failed',
                JOptionPane.ERROR_MESSAGE,
                None
            )
            self.menuItem.setEnabled(
                self.celldata.hasChanges()
            )
        else :
            JOptionPane.showInternalMessageDialog(
                self.app.getDesktop(),
                'AdminConfig.save() - successful',
                'Save complete',
                JOptionPane.INFORMATION_MESSAGE,
                None
            )

#-------------------------------------------------------------------------------
# Name: DiscardTask
# Role: Execute a potentially long running AdminConfig.reset() call so the GUI
#       doesn't appear to be "hung".
# Note: Instances of SwingWorker are not reusuable; new ones must be created.
#-------------------------------------------------------------------------------
class DiscardTask( SwingWorker ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    # Note: The associated menu item is disabled so multiple threads can't be
    #       running at the same time for the same activeFrame.
    #---------------------------------------------------------------------------
    def __init__( self, app, menuItem, cellData, fileName ) :
        self.app      = app
        self.cellData = cellData
        self.fileName = fileName
        self.menuItem = menuItem
        self.msgText  = None
        menuItem.setEnabled( 0 )

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Restore all port number changes and call AdminConfig.reset() if
    #       cellData specifies the local configuration (i.e., fileName == None)
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        try :
            original = self.cellData.getOriginal()
            tables = []
            for index in original.keys() :
                table, row = index
                table.getModel().resetPortValue(
                    row,
                    original[ index ]
                )
                if table not in tables :
                    tables.append( table )
            self.cellData.clearOriginals()
            for table in tables :
                table.repaint()
            #-------------------------------------------------------------------
            # AdminConfig.reset() only applies to frame 0 (local data)
            #-------------------------------------------------------------------
            if not self.fileName :
                AdminConfig.reset()
        except :
            self.msgText = 'Error: %s\nvalue: %s' % sys.exc_info()[ :2 ]

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Display an error message, if an error was encountered
    # Note: The specified menuItem is enabled iff changes remain to be saved
    #---------------------------------------------------------------------------
    def done( self ) :
        if self.msgText :
            JOptionPane.showInternalMessageDialog(
                self.app.getDesktop(),
                self.msgText,
                'DiscardTask() Failed',
                JOptionPane.ERROR_MESSAGE,
                None
            )
        self.menuItem.setEnabled(
            self.cellData.hasChanges()
        )


#-------------------------------------------------------------------------------
# Name: ExportTask
# Role: Traverse the inner frame details, exporting the information to the
#       specified output file.
# Note: Instances of SwingWorker are not reusuable; new ones must be created.
#-------------------------------------------------------------------------------
class ExportTask( SwingWorker ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    #---------------------------------------------------------------------------
    def __init__( self, app, menuItem, cellData, fileName, cleanup = 0 ) :
        self.app      = app
        self.menuItem = menuItem
        self.cellData = cellData
        self.fileName = fileName
        self.cleanup  = cleanup
        self.msgText  = None
        if menuItem :
            self.menuItem.setEnabled( 0 )

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Use XML transformation while processing the cellData to create the
    #       specified (nicely formatted) XML output file.
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        try :
            fos = FileOutputStream( self.fileName )
            streamResult = StreamResult(
                OutputStreamWriter( fos, 'ISO-8859-1' )
            )

            #-------------------------------------------------------------------
            # Start by creating our transformer instance
            #-------------------------------------------------------------------
            trans = SAXTransformerFactory.newInstance()
            trans.setAttribute( 'indent-number', 4 )

            #-------------------------------------------------------------------
            # Use the transformer hander to produce XML output
            #-------------------------------------------------------------------
            tHand = trans.newTransformerHandler()
            serializer = tHand.getTransformer()

            serializer.setOutputProperty(
                OutputKeys.ENCODING, 'ISO-8859-1'
            )
            serializer.setOutputProperty(
                OutputKeys.DOCTYPE_SYSTEM, 'WASports.dtd'
            )
            serializer.setOutputProperty(
                OutputKeys.INDENT, 'yes'
            )
            tHand.setResult( streamResult )

            tHand.startDocument()

            #-------------------------------------------------------------------
            # Create main WASports tag with the required version attribute
            #-------------------------------------------------------------------
            atts = AttributesImpl()
            atts.addAttribute(
                '', '', 'version', 'CDATA', __version__
            )
            tHand.startElement( '', '', 'WASports', atts )
            atts.clear()

            #-------------------------------------------------------------------
            # cell tag
            #-------------------------------------------------------------------
            tHand.startElement( '', '', 'cell', atts )
            data = self.cellData
            root = data.tree.getModel().getRoot()
            cellName = root.toString()
            self.addTagAndText( tHand, 'name', cellName )
            info = data.getInfoDict( cellName )
            self.addTagAndText(
                tHand, 'WAShome', info[ 'WAShome' ]
            )
            self.addTagAndText(
                tHand, 'WASversion', info[ 'WASversion' ]
            )
            self.addTagAndText(
                tHand, 'profile', info[ 'profile' ]
            )

            #-------------------------------------------------------------------
            # one or more node tags
            #-------------------------------------------------------------------
            nodes = root.children()
            while nodes.hasMoreElements() :
                node = nodes.nextElement()
                nodeName = node.toString()
                info = data.getInfoDict( nodeName )
                tHand.startElement( '', '', 'node', atts )
                self.addTagAndText( tHand, 'name', nodeName )
                self.addTagAndText(
                    tHand, 'WAShome', info[ 'WAShome' ]
                )
                self.addTagAndText(
                    tHand, 'WASversion', info[ 'WASversion' ]
                )
                self.addTagAndText(
                    tHand, 'profile', info[ 'profile' ]
                )
                self.addTagAndText(
                    tHand, 'hostname', info[ 'hostnames' ]
                )
                self.addTagAndText(
                    tHand, 'ipaddr', info[ 'ipaddr' ]
                )

                #---------------------------------------------------------------
                # one or more server tags
                #---------------------------------------------------------------
                servers = node.children()
                while servers.hasMoreElements() :
                    server = servers.nextElement()
                    serverName = server.toString()
                    tHand.startElement(
                        '', '', 'server', atts
                    )
                    self.addTagAndText(
                        tHand, 'name', serverName
                    )
                    table = data.getPortTable(
                        ( nodeName, serverName )
                    )
                    model = table.getModel()
                    #-----------------------------------------------------------
                    # many (named) endpoint tags
                    #-----------------------------------------------------------
                    for row in range( model.getRowCount() ) :
                        tHand.startElement( '', '', 'endpoint', atts )
                        name = model.getValueAt( row, 1 )
                        self.addTagAndText(
                            tHand, 'name', name
                        )
                        port = str(
                            model.getValueAt( row, 0 )
                        )
                        self.addTagAndText(
                            tHand, 'port', port
                        )
                        tHand.endElement(
                            '', '', 'endpoint'
                        )
                    tHand.endElement( '', '', 'server' )

                tHand.endElement( '', '', 'node' )

            tHand.endElement( '', '', 'cell' )

            tHand.endElement( '', '', 'WASports' )

            tHand.endDocument()
        except :
            self.msgText = 'Error: %s\nvalue: %s' % sys.exc_info()[ :2 ]

    #---------------------------------------------------------------------------
    # Name: addTagAndText()
    # Role: Make XML tag creation easier
    # Note: Simple utility method to create a simple XML tag with a string value
    #---------------------------------------------------------------------------
    def addTagAndText( self, handler, tagName, text ) :
        handler.startElement(
            '', '', tagName, AttributesImpl()
        )
        handler.characters(
            String( text ).toCharArray(), 0, len( text )
        )
        handler.endElement( '', '', tagName )

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Enable the Export Menu Item once this thread has completed
    #---------------------------------------------------------------------------
    def done( self ) :
        if self.msgText :
            JOptionPane.showInternalMessageDialog(
                self.app.getDesktop(),
                self.msgText,
                'ExportTask() Failed',
                JOptionPane.ERROR_MESSAGE,
                None
            )
            if self.menuItem :
                self.menuItem.setEnabled(
                    self.cellData.hasChanges()
                )
        else :
            JOptionPane.showInternalMessageDialog(
                self.app.getDesktop(),
                'Export successful',
                'ExportTask() complete',
                JOptionPane.INFORMATION_MESSAGE,
                None
            )
            #-------------------------------------------------------------------
            # Handle an Export that is the result of a Save request differently
            #-------------------------------------------------------------------
            if self.cleanup :
                self.cellData.clearOriginals()
            if self.menuItem :
                self.menuItem.setEnabled( not self.cleanup )

#-------------------------------------------------------------------------------
# Name: ImportTask
# Role: Validate and parse the specified XML file and use its contents to create
#       another InternalFrame.
# Note: Instances of SwingWorker are not reusuable; new ones must be created.
#-------------------------------------------------------------------------------
class ImportTask( SwingWorker ) :

    #---------------------------------------------------------------------------
    # Name: SAXhandler
    # Role: Implementation of SAX handler the methods of which are called by
    #       the SAX parser
    #---------------------------------------------------------------------------
    class SAXhandler( DefaultHandler ) :

        #-----------------------------------------------------------------------
        # Name: __init__()
        # Role: Constructor used to initialze instance attributes
        # Note: The self.names dictionary values are contrived configIds
        #-----------------------------------------------------------------------
        def __init__( self, app ) :
            self.app      = app
            self.chars    = ''
#           self.result   = cellInfo( debug = 1 )
            self.result   = cellInfo()
            self.string   = ''
            self.infoDict = {}
            self.errors   = []
            self.cellName = None
            self.nodeName = None
            self.serverName = None
            self.portData = []
            self.tree     = None
            self.names    = None
            self.node     = None

        #-----------------------------------------------------------------------
        # Name: startElement()
        # Role: Called by SAX parser to handle XML start tag
        # Note: Use of self.chars is deferred until here, n.b., characters()
        #-----------------------------------------------------------------------
        def startElement(
            self, uri, localName, tagName, attributes
        ) :
            if not self.errors :
                self.setString( self.chars )
                self.chars = ''

                #---------------------------------------------------------------
                # For the 'WASports' tag, verify the version attribute value
                #---------------------------------------------------------------
                if tagName == 'WASports' :
                    attr = [
                        (
                            attributes.getQName( i ),
                            attributes.getValue( i )
                        )
                        for i in range(
                            attributes.getLength()
                        )
                    ]
                    attrDict = {}
                    for name, value in attr :
                        attrDict[ name ] = value
                    #-----------------------------------------------------------
                    # Note: If "version" is missing ver == None
                    #-----------------------------------------------------------
                    ver = attrDict.get( 'version' )
                    if ver != __version__ :
                        self.errors.append(
                            (
                                'Version mismatch, expected ' +
                                '"%s" actual "%s"'
                            )
                            % ( __version__, ver )
                        )

                #---------------------------------------------------------------
                # When the cell tag is encountered, start initializing the
                # infoDict with the values required at the cell level
                #---------------------------------------------------------------
                elif tagName == 'cell' :
                    self.infoDict = {}
                #---------------------------------------------------------------
                # When the 1st 'node' tag is found, infoDict should contain all
                # of the cell level information
                # Note: the index for the names dictionary is a pseudo configId
                #---------------------------------------------------------------
                elif tagName == 'node' :
                    if not self.cellName :
                        self.cellName = self.infoDict[ 'name' ]
                        self.infoDict[
                            'cellName'
                        ] = self.cellName
                        self.result.setCellName(
                            self.cellName
                        )
                        self.result.addInfoData(
                            self.cellName,
                            CELLINFO,
                            self.infoDict
                        )
                        self.tree = JTree(
                            DefaultMutableTreeNode(
                                self.cellName
                            )
                        )
                        TSM = TreeSelectionModel
                        self.tree.getSelectionModel(
                        ).setSelectionMode(
                            TSM.SINGLE_TREE_SELECTION
                        )
                        self.result.setTree( self.tree )
                        configId = '/cell:%s/' % self.cellName
                        self.names = {
                            self.cellName : configId
                        }
                #---------------------------------------------------------------
                # When the 1st 'server' tag is found within a node, the infoDict
                # contains the node specific information that needs to be added
                #---------------------------------------------------------------
                elif tagName == 'server' :
                    if not self.nodeName :
                        self.nodeName = self.infoDict[
                            'name'
                        ]
                        self.infoDict[
                            'nodeName'
                        ] = self.nodeName
                        self.infoDict[
                            'hostnames'
                        ] = self.infoDict[ 'hostname' ]
                        self.result.addInfoData(
                            self.nodeName,
                            NODEINFO,
                            self.infoDict
                        )
                        node = DefaultMutableTreeNode(
                            self.nodeName
                        )
                        self.node = node
                        model  = self.tree.getModel()
                        root   = model.getRoot()
                        nodes  = root.getChildCount()
                        model.insertNodeInto( node, root, nodes )
                        configId = '/cell:%s/node:%s/' % (
                            self.cellName,
                            self.nodeName
                        )
                        self.names[ self.nodeName ] = configId
                #---------------------------------------------------------------
                # When the 1st 'endpoint' tag is found (within a server), 
                # some special handling needs to occur
                #---------------------------------------------------------------
                elif tagName == 'endpoint' :
                    if not self.serverName :
                        self.serverName = self.infoDict[
                            'name'
                        ]
                        self.infoDict[
                            'serverName'
                        ] = self.serverName
                        leaf = DefaultMutableTreeNode(
                            self.nodeName
                        )
                        configId = '/cell:%s/node:%s/server:%s' % (
                            self.cellName,
                            self.nodeName,
                            self.serverName
                        )
                        self.names[
                            ( self.nodeName, self.serverName )
                        ] = configId
                        leaf   = DefaultMutableTreeNode(
                            self.serverName
                        )
                        model  = self.tree.getModel()
                        root   = model.getRoot()
                        node   = self.node
                        servers = node.getChildCount()
                        model.insertNodeInto( leaf, node, servers )

        #-----------------------------------------------------------------------
        # Name: endElement()
        # Role: Called by SAX parser to handle XML end tag
        # Note: Use of self.chars is deferred until here, n.b., characters()
        #-----------------------------------------------------------------------
        def endElement( self, uri, localName, tagName ) :
            if not self.errors :
                self.setString( self.chars )
                self.chars = ''

                #---------------------------------------------------------------
                # Add the endpoint info the the current portData array
                #---------------------------------------------------------------
                if tagName == 'endpoint' :
                    self.portData.append(
                        [
                            self.infoDict[ 'port' ],
                            self.infoDict[ 'name' ]
                        ]
                    )
                elif tagName == 'node' :
                    self.nodeName = self.serverName = None
                elif tagName == 'server' :
                    #-----------------------------------------------------------
                    # Create the table to be displayed for this "remote" server
                    #-----------------------------------------------------------
                    LSM = ListSelectionModel
                    table = JTable(
                        PortTableModel( self.portData ),
                        autoResizeMode = JTable.AUTO_RESIZE_OFF,
                        selectionMode = LSM.SINGLE_SELECTION
                    )
                    table.getTableHeader().setReorderingAllowed(
                        0
                    )
                    table.getModel().setContext(
                        table,            # table instance reference
                        self.nodeName,    # nodeName for this server
                        self.serverName,  # serverName
                        {},               # empty for non-local data
                        self.app          # Application reference
                    )
                    setColumnWidths( table )
                    self.result.addPortTable(
                        ( self.nodeName, self.serverName ),
                        table
                    )
                    #-----------------------------------------------------------
                    # empty attributes for the next section
                    #-----------------------------------------------------------
                    self.serverName = None
                    self.portData = []
                elif tagName in [
                    'WAShome',
                    'WASversion',
                    'profile',
                    'hostname',
                    'ipaddr',
                    'name',
                    'port'
                ] :
                    self.infoDict[ tagName ] = self.getString()
                elif tagName in [ 'WASports', 'cell' ] :
                    #-----------------------------------------------------------
                    # These tags are valid, but require no special processing
                    #-----------------------------------------------------------
                    pass
                else :
                    self.errors.append(
                        'Unrecognized tag: %s' % tagName
                    )

        #-----------------------------------------------------------------------
        # Name: characters()
        # Role: Called by SAX parser to handle character text
        # Note: The SAX parser may make multiple calls to this routine to
        #       process character data.  That is why the use of self.chars
        #       is deferred until one of the *Element() methods is called
        #-----------------------------------------------------------------------
        def characters( self, ch, start, length ) :
            value = str( String( ch, start, length ) ).strip()
            if value :
                self.chars += value

        #-----------------------------------------------------------------------
        # Name: warning()
        # Role: Called by SAX parser when a warning condition is encountered
        #-----------------------------------------------------------------------
        def warning( self, e ) :
            if not self.errors :
                self.errors.append(
                    'Warning: %s' % e.getMessage()
                )

        #-----------------------------------------------------------------------
        # Name: error()
        # Role: Called by SAX parser when a error condition is encountered
        #-----------------------------------------------------------------------
        def error( self, e ) :
            if not self.errors :
                self.errors.append(
                    'Error: %s' % e.getMessage()
                )

        #-----------------------------------------------------------------------
        # Name: fatalError()
        # Role: Called by SAX parser when a fatal error condition is encountered
        #-----------------------------------------------------------------------
        def fatalError( self, e ) :
            if not self.errors :
                self.errors.append(
                    'Fatal Error: %s' % e.getMessage()
                )

        #-----------------------------------------------------------------------
        # Name: getString()
        # Role: Getter for local string value
        #-----------------------------------------------------------------------
        def getString( self ) :
            return self.string

        #-----------------------------------------------------------------------
        # Name: getString()
        # Role: setter for local string value
        #-----------------------------------------------------------------------
        def setString( self, value ) :
            if value :
                self.string = value
            else :
                self.string = ''

        #-----------------------------------------------------------------------
        # Name: getResults()
        # Role: Getter for result (instance of cellInfo)
        #-----------------------------------------------------------------------
        def getResults( self ) :
            return self.result

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: ImportTask Constructor
    #---------------------------------------------------------------------------
    def __init__( self, app, menuItem, fileName ) :
        self.app      = app
        self.menuItem = menuItem
        self.fileName = fileName
        self.handler  = ImportTask.SAXhandler( app )
        menuItem.setEnabled( 0 )
        self.msgText  = ''

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Setup the SAX parser to process the specifed XML input file
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        try :
            FIS     = FileInputStream( File( self.fileName ) )
            ISR     = InputStreamReader( FIS, ENCODING )
            src     = InputSource( ISR, encoding = ENCODING )
            factory = SAXParserFactory.newInstance()
            factory.setValidating( 1 )
            parser  = factory.newSAXParser()
            parser.parse( src, self.handler )
            FIS.close()
        except :
            msgText = 'Error: %s\nvalue: %s'
            self.msgText = msgText % sys.exc_info()[ :2 ]

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Enable the Import Menu Item once this thread has completed
    #---------------------------------------------------------------------------
    def done( self ) :
        localFrame = self.app.localFrame
        desktop    = self.app.frame.getContentPane()
        errors     = self.handler.errors
        #-----------------------------------------------------------------------
        # If XML parsing or validation errors occurred, inform the user
        #-----------------------------------------------------------------------
        if self.msgText or errors :
            if self.msgText :
                msg = self.msgText + '\n'
            else :
                msg = ''
            for error in self.handler.errors :
                msg += ( '\n' + error )
            if msg.startswith( '\n' ) :
                msg = msg[ 1: ]

            JOptionPane.showInternalMessageDialog(
                desktop,
                msg,
                'Import failed',
                JOptionPane.ERROR_MESSAGE,
                None
            )
        else :
            #-------------------------------------------------------------------
            # Create a new internal frame, and add it to the desktop
            #-------------------------------------------------------------------
            cellData = self.handler.getResults()
            tree = cellData.getTree()
            root = tree.getModel().getRoot()
            name = root.toString()
            if localFrame :
                size   = localFrame.getSize()
                w, h   = size.width, size.height
                count  = len( self.app.frames )
                num    = ( count - 1 ) % 8
                loc    = Point(
                    num * 27 + 32,
                    num * 27 + 32
                )
            else :
                print '\nWarning: no localFrame'
                size  = self.app.frame.getSize()
                w, h  = size.width >> 1, size.height >> 1
                count = 0
                loc   = Point( 32, 32 )

            #-------------------------------------------------------------------
            # XML parsing was successful.  Create a new internal frame
            #-------------------------------------------------------------------
            internal  = InternalFrame(
                title    = '%d : %s' % ( count, name ),
                size     = Dimension( w , h ),
                location = loc,
                cellData = cellData,
                app      = self.app,
                closable = 1
#               debug    = 1
            )
            self.app.frames.append(
                ( internal, self.fileName )
            )
            desktop.add( internal, None, 0 )
            internal.setSelected( 1 )
            node = tree.getModel().getRoot()
            tree.expandPath( TreePath( node.getPath() ) )

        self.menuItem.setEnabled( 1 )

#-------------------------------------------------------------------------------
# Name: PortLookupTask
# Role: Background processing of potentially long running WebSphere Application
#       Server (WSAS) scripting object calls to query the WSAS configuation to
#       determine the port numbers configured for a specific application server.
# Note: Instances of SwingWorker are not reusuable; new ones must be created.
#-------------------------------------------------------------------------------
class PortLookupTask( SwingWorker ) :

    #---------------------------------------------------------------------------
    # Thread lock used to synchronize calls to this class
    #---------------------------------------------------------------------------
    lock = threading.Lock()

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: constructor
    # Note: This class retrieves the port information for the specific Server
    #       and updates the data dictionary once the lookup is complete.
    #---------------------------------------------------------------------------
    def __init__(
        self,
        app,
        nodeName,
        serverName,
        data
    ) :
        self.app      = app
        self.nodeName = nodeName
        self.servName = serverName
        self.data     = data
        self.msgText  = None
        SwingWorker.__init__( self )

    #---------------------------------------------------------------------------
    # Name: doInBackground()
    # Role: Call the AdminConfig scripting object in the background
    #---------------------------------------------------------------------------
    def doInBackground( self ) :
        self.lock.acquire()
        try :
            pDict, eDict = self.getPorts( self.nodeName, self.servName )
            ports = pDict.keys()            # Note: Port #s are numeric strings
            #-------------------------------------------------------------------
            # Convert the port/endPointName dictionary to an ordered array
            # Note: The dictionary keys are numeric port number strings, so we
            #       need to sort them as integers
            #-------------------------------------------------------------------
            ports.sort( lambda x,y: cmp( int( x ), int( y ) ) )
            result = []
            for port in ports :
                result.append( [ port, pDict[ port ] ] )

            table = JTable(
                PortTableModel( result ),
                autoResizeMode = JTable.AUTO_RESIZE_OFF,
                selectionMode = ListSelectionModel.SINGLE_SELECTION
            )
            table.getTableHeader().setReorderingAllowed( 0 )
            table.getModel().setContext(
                table,            # Give model a reference to table instance
                self.nodeName,    # Identify the nodeName for this server
                self.servName,    # Identify the serverName
                eDict,            # Dict[ endPointName ] -> configId
                self.app          # Application reference
            )
            setColumnWidths( table )
            self.data.addPortTable( ( self.nodeName, self.servName ), table )
        except :
            self.msgText = 'Error: %s\nvalue: %s' % sys.exc_info()[ :2 ]
        self.lock.release()

    #---------------------------------------------------------------------------
    # Name: done()
    # Role: Called when the background processing completes
    #---------------------------------------------------------------------------
    def done( self ) :
        if self.msgText :
            JOptionPane.showInternalMessageDialog(
                self.app.getDesktop(),
                self.msgText,
                'PortLookupTask() Failed',
                JOptionPane.ERROR_MESSAGE,
                None
            )

    #---------------------------------------------------------------------------
    # Name: getPorts()
    # Role: Return a dictionary, indexed by port number, of the named EndPoints
    #       for the specified server.
    #---------------------------------------------------------------------------
    def getPorts( self, nodeName, serverName ) :
        #-----------------------------------------------------------------------
        # Use the nodeName to find it's configId
        #-----------------------------------------------------------------------
        scope = firstNamedConfigType( 'Node', nodeName  )

        #-----------------------------------------------------------------------
        # Locate the named (and optionally scoped) 'ServerEntry'
        #-----------------------------------------------------------------------
        serverEntry = firstNamedConfigType(
            'ServerEntry',
            serverName,
            scope,
            'serverName'
        )
        portDict = {}
        epIdDict = {}
        if serverEntry :
            #-------------------------------------------------------------------
            # for each NamedEndPoint on this server...
            #-------------------------------------------------------------------
            nEPs = AdminConfig.list( 'NamedEndPoint', serverEntry ).splitlines()
            for namedEndPoint in nEPs :
                Name = AdminConfig.showAttribute( namedEndPoint, 'endPointName' )
                epId = AdminConfig.showAttribute( namedEndPoint, 'endPoint' )
                port = AdminConfig.showAttribute( epId, 'port' )
                portDict[ port ] = Name
                epIdDict[ Name ] = epId
        #-----------------------------------------------------------------------
        # Return either an empty dictionary or one indexed by Port number
        # containing the associated end point names.
        #-----------------------------------------------------------------------
        return portDict, epIdDict

#-------------------------------------------------------------------------------
# Name: PortTableModel
# Role: Define the Table Model for the server ports
#-------------------------------------------------------------------------------
class PortTableModel( DefaultTableModel ) :

    headings = 'Port#,EndPoint Name'.split( ',' )

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    #---------------------------------------------------------------------------
    def __init__( self, data ) :
        self.table      = None
        self.nodeName   = None
        self.serverName = None
        self.epIdDict   = None
        self.app        = None
        for row in range( len( data ) ) :
            data[ row ][ 0 ] = int( data[ row ][ 0 ] )
        DefaultTableModel.__init__( self, data, self.headings )

    #---------------------------------------------------------------------------
    # Name: getColumnClass()
    # Role: Used to identify the data type for each column
    # Note: Since the port numbers need to be sorted as an Integer, and the End
    #       Point Names need to be sorted as Strings, we need to return the true
    #       class type for each column.
    #---------------------------------------------------------------------------
    def getColumnClass( self, col ) :
        if col == 0 :
            return Integer
        else :
            return String

    #---------------------------------------------------------------------------
    # Name: isCellEditable()
    # Role: Returns true (1) if the specified column is editable
    #---------------------------------------------------------------------------
    def isCellEditable( self, row, col ) :
        return col == 0

    #---------------------------------------------------------------------------
    # Name: resetPortValue()
    # Role: Used to restore the original port number value
    #---------------------------------------------------------------------------
    def resetPortValue( self, row, value ) :
        DefaultTableModel.setValueAt( self, value, row, 0 )
        self.fireTableCellUpdated( row, 0 )

    #---------------------------------------------------------------------------
    # Name: setValueAt()
    # Role: Used to validate and change a cell value
    # Note: Only column 0 (i.e., port#) is editable!
    # Note: This depends upon the order of menu items
    #---------------------------------------------------------------------------
    def setValueAt( self, value, row, col ) :
        prev = self.getValueAt( row, col )
        if 0 <= value <= 65535 :
            #-------------------------------------------------------------------
            # Note: We only keep the original (since last "save") port number
            #-------------------------------------------------------------------
            name = self.getValueAt( row, 1 )
            epId = self.epIdDict.get( name )
            if epId :
                AdminConfig.modify( epId, [ [ 'port', value ] ] )
            self.app.ChangesMI.setEnabled( 1 )
            DefaultTableModel.setValueAt( self, value, row, col )
            activeFrame = self.app.getActiveFrame()
            if activeFrame :
                activeFrame.getCellData().addOriginal( self.table, row, prev )
        else :
            DefaultTableModel.setValueAt(
                self,
                prev,
                row,
                col
            )
        self.fireTableCellUpdated( row, col )

    #---------------------------------------------------------------------------
    # Name: getContext()
    # Role: Return the current table context associated with this model
    #---------------------------------------------------------------------------
    def getContext( self ) :
        return self.table, self.nodeName, self.serverName

    #---------------------------------------------------------------------------
    # Name: setContext()
    # Role: Used to identify the table (instance) associated with this model
    #---------------------------------------------------------------------------
    def setContext(
        self, table, nodeName, serverName, epIdDict, app
    ) :
        self.table      = table
        self.nodeName   = nodeName
        self.serverName = serverName
        self.epIdDict   = epIdDict
        self.app        = app

#-------------------------------------------------------------------------------
# Name: WASports_11
# Role: Display multiple port tables and associated End Point Names using Swing
#-------------------------------------------------------------------------------
class WASports_11( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Application constructor
    # Note: See InternalFrame listener methods
    #---------------------------------------------------------------------------
    def __init__( self ) :
        self.activeFrame = None
        self.localFrame  = None
        self.frames      = []
        self.desktop     = None
        self.ensureDTD()

    #---------------------------------------------------------------------------
    # Name: getActiveFrame()
    # Role: Return a reference to the active (inner) frame, or None
    #---------------------------------------------------------------------------
    def getActiveFrame( self ) :
        return self.activeFrame

    #---------------------------------------------------------------------------
    # Name: setActiveFrame()
    # Role: Saves a reference to the active (inner) frame, or None
    #---------------------------------------------------------------------------
    def setActiveFrame( self, frame ) :
        self.activeFrame = frame

    #---------------------------------------------------------------------------
    # Name: getDesktop()
    # Role: Return the application desktop reference
    #---------------------------------------------------------------------------
    def getDesktop( self ) :
        return self.desktop

    #---------------------------------------------------------------------------
    # Name: setDesktop()
    # Role: Update (save) the application desktop reference
    #---------------------------------------------------------------------------
    def setDesktop( self, desktop ) :
        self.desktop = desktop

    #---------------------------------------------------------------------------
    # Name: getName()
    # Role: Return the name attribute value from the specified configId
    # Note: This "hides" java.awt.Component.getName()
    #---------------------------------------------------------------------------
    def getName( self, configId ) :
        return AdminConfig.showAttribute( configId, 'name' )

    #---------------------------------------------------------------------------
    # Name: getLocalCellInfo()
    # Role: Return cellInfo() instance containing local cell details
    #---------------------------------------------------------------------------
    def getLocalCellInfo( self ) :

        #-----------------------------------------------------------------------
        # Retrieve the name of the local cell
        #-----------------------------------------------------------------------
        cell = AdminConfig.list( 'Cell' )
        cellName = self.getName( cell )

        #-----------------------------------------------------------------------
        # Create the cellInfo object instance to be returned
        #-----------------------------------------------------------------------
        result = cellInfo()
        result.setCellName( cellName )
        infoDict = {
            'cellName'   : cellName,
            'WAShome'    : WAShome( cell ),
            'WASversion' : WASversion( cell ),
            'profile'    : WASprofileName( cell )
        }
        #-----------------------------------------------------------------------
        # Add the cell level information to result
        #-----------------------------------------------------------------------
        result.addInfoData( cellName, CELLINFO, infoDict )

        #-----------------------------------------------------------------------
        # Use the cellName as the tree root value
        #-----------------------------------------------------------------------
        root = DefaultMutableTreeNode( cellName )

        #-----------------------------------------------------------------------
        # Build an item name to start the names (configId) dictionary
        #-----------------------------------------------------------------------
        names = { cellName : cell }

        #-----------------------------------------------------------------------
        # Process each node in the cell
        #-----------------------------------------------------------------------
        for node in AdminConfig.list( 'Node' ).splitlines() :
            #-------------------------------------------------------------------
            # here = tree node for the current WAS "Node" with value of nodeName
            #-------------------------------------------------------------------
            nodeName = self.getName( node )
            here = DefaultMutableTreeNode(
                nodeName
            )

            #-------------------------------------------------------------------
            # Pick 1st server in this node & obtain hostname & ipaddr details
            #-------------------------------------------------------------------
            server     = AdminConfig.list( 'Server', node ).splitlines()[ 0 ]
            serverName = self.getName( server )
            hostnames  = getHostnames( nodeName, serverName )
            ipaddr     = getIPaddresses( hostnames )

            #-------------------------------------------------------------------
            # infoDict is the dictionary of current node information
            #-------------------------------------------------------------------
            infoDict = {
                'cellName'   : cellName,
                'nodeName'   : nodeName,
                'WAShome'    : WAShome( node ),
                'WASversion' : WASversion( node ),
                'profile'    : WASprofileName( node ),
                'hostnames'  : ', '.join( hostnames ),
                'ipaddr'     : ', '.join( ipaddr )
            }
            #-------------------------------------------------------------------
            # Add the node level information to result
            #-------------------------------------------------------------------
            result.addInfoData( nodeName, NODEINFO, infoDict )

            #-------------------------------------------------------------------
            # Add the node (configId) to the names dictionary
            #-------------------------------------------------------------------
            names[ nodeName ] = node

            #-------------------------------------------------------------------
            # Process all servers in the current node
            #-------------------------------------------------------------------
            servers = AdminConfig.list( 'Server', node )
            for server in servers.splitlines() :
                #---------------------------------------------------------------
                # Each server will be a leaf node in cell hierarchy tree
                #---------------------------------------------------------------
                serverName = self.getName( server )
                leaf = DefaultMutableTreeNode( serverName )
                #---------------------------------------------------------------
                # Add this server to the names dictionary
                # Note: Server names are not guaranteed to be unique in the cell
                #       so a tuple of ( nodeName, sererName ) is used, instead.
                #---------------------------------------------------------------
                names[ ( nodeName, serverName ) ] = server
                #---------------------------------------------------------------
                # Each server is a leaf node in cell hierarchy tree
                #---------------------------------------------------------------
                here.add( leaf )
                #---------------------------------------------------------------
                # Start a separate thread to lookup the ports used by the server
                # Note: This thread updates the cellInfo instance (result)
                #---------------------------------------------------------------
                PortLookupTask(
                    self,
                    nodeName,
                    serverName,
                    result
                ).execute()
            #-------------------------------------------------------------------
            # Add this node sub-tree to the cell hierarchy tree
            #-------------------------------------------------------------------
            root.add( here )

        #-----------------------------------------------------------------------
        # Add names dictionary, and the cell hierarchy tree to the result object
        #-----------------------------------------------------------------------
        result.setNames( names )
        tree = JTree( root )
        tree.getSelectionModel().setSelectionMode(
            TreeSelectionModel.SINGLE_TREE_SELECTION
        )
        result.setTree( tree )

        return result

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
        # Build the "File" -> "Changes" (nested) menu
        #-----------------------------------------------------------------------
        self.ChangesMI = JMenu( 'Changes', enabled = 0 )
        self.ChangesMI.add(
            JMenuItem(
                'Save',
                actionPerformed = self.save
            )
        )
        self.ChangesMI.add(
            JMenuItem(
                'Discard',
                actionPerformed = self.discard
            )
        )

        #-----------------------------------------------------------------------
        # "File" entry
        #-----------------------------------------------------------------------
        FileMI = JMenu( 'File' )
        FileMI.add( self.ChangesMI )

        FileMI.add( JSeparator() )
        FileMI.add(
            JMenuItem(
                'Import',
                actionPerformed = self.Import
            )
        )
        FileMI.add(
            JMenuItem(
                'Export',
                actionPerformed = self.Export
            )
        )
        FileMI.add( JSeparator() )

        FileMI.add(
            JMenuItem(
                'Exit',
                actionPerformed = self.Exit
            )
        )
        menu.add( FileMI )

        #-----------------------------------------------------------------------
        # "Help" entry
        #-----------------------------------------------------------------------
        HelpMI = JMenu( 'Help' )
        AboutMI = JMenuItem(
            'About',
            enabled = 0,
            actionPerformed = self.about
        )
        HelpMI.add( AboutMI )
        #-----------------------------------------------------------------------
        # Convert script docstring to HTML on a separate thread
        #-----------------------------------------------------------------------
        self.aboutTask = AboutTask( AboutMI )
        self.aboutTask.execute()

        HelpMI.add(
            JMenuItem(
                'Notice',
                actionPerformed = self.notice
            )
        )
        menu.add( HelpMI )

        return menu

    #---------------------------------------------------------------------------
    # Name: about()
    # Role: Help -> About menu item event handler
    #---------------------------------------------------------------------------
    def about( self, e ) :
        JOptionPane.showInternalMessageDialog(
            self.frame.getContentPane(),
            JLabel(
                self.aboutTask.getResult(),
                font = MONOFONT
            ),
            'About',
            JOptionPane.PLAIN_MESSAGE
        )

    #---------------------------------------------------------------------------
    # Name: notice()
    # Role: Help -> Notice menu item event handler
    #---------------------------------------------------------------------------
    def notice( self, e ) :
        JOptionPane.showInternalMessageDialog(
            self.frame.getContentPane(),
            Disclaimer,
            'Notice',
            JOptionPane.INFORMATION_MESSAGE
        )

    #---------------------------------------------------------------------------
    # Name: Export()
    # Role: Export cellData information to user specified XML file
    #---------------------------------------------------------------------------
    def Export( self, event ) :
        title = 'Export (Save) cell details'
        fc = JFileChooser(
            currentDirectory = File( '.' ),
            dialogTitle = title,
            fileFilter  = XMLfiles()
        )
        if fc.showOpenDialog( self.frame ) == JFileChooser.APPROVE_OPTION :
            f = fc.getSelectedFile()
            fileName = fc.getSelectedFile().getAbsolutePath()
            fileName = abspath( normpath( fileName ) )
            if not fileName.endswith( '.xml' ) :
                fileName += '.xml'
            if os.path.isfile( fileName ) :
                response = JOptionPane.showInternalConfirmDialog(
                    self.frame.getContentPane(),
                   'Overwrite existing file (%s)?' % os.path.basename( fileName ),
                   'Confirm Overwrite',
                    JOptionPane.OK_CANCEL_OPTION,
                    JOptionPane.QUESTION_MESSAGE
                )
                if response == JOptionPane.CANCEL_OPTION :
                    return

            activeFrame = self.getActiveFrame()
            if activeFrame :
                ExportTask(
                    self,
                    event.getSource(),
                    activeFrame.getCellData(),
                    fileName
                ).execute()

    #---------------------------------------------------------------------------
    # Name: Import()
    # Role: "Load" the contents of another cell from a user specified XML file
    #       and display it in a new inner frame.
    #---------------------------------------------------------------------------
    def Import( self, event ) :
        title = 'Import (Load) cell details'
        fc = JFileChooser(
            currentDirectory = File( '.' ),
            dialogTitle = title,
            fileFilter  = XMLfiles()
        )
        if fc.showOpenDialog( self.frame ) == JFileChooser.APPROVE_OPTION :
            f = fc.getSelectedFile()
            fileName = fc.getSelectedFile().getAbsolutePath()
            fileName = abspath( normpath( fileName ) )
            if not fileName.endswith( '.xml' ) :
                fileName += '.xml'
            if not os.path.isfile( fileName ) :
                JOptionPane.showInternalMessageDialog(
                    self.frame.getContentPane(),
                    'File not found: "%s"' % fileName,
                    'Information',
                    JOptionPane.INFORMATION_MESSAGE
                )
                return
            #-------------------------------------------------------------------
            # Don't allow multiple imports of same file
            #-------------------------------------------------------------------
            for frame, fName in self.frames :
                msg = (
                          '<html>The specified file has ' + 
                          'already been imported.<br>'    +
                          'Press "OK" to activate that frame.'
                      )
                if fName == fileName :
                    if JOptionPane.OK_OPTION == JOptionPane.showInternalConfirmDialog(
                        self.frame.getContentPane(),
                        msg,
                        'File already imported',
                        JOptionPane.OK_CANCEL_OPTION,
                        JOptionPane.WARNING_MESSAGE
                    ) :
                        frame.setSelected( 1 )
                        if frame.isIcon() :
                            frame.setIcon( 0 )
                    break
            else :
                ImportTask(
                    self,
                    event.getSource(),
                    fileName
                ).execute()

    #---------------------------------------------------------------------------
    # Name: save()
    # Role: File -> Changes -> Save : event handler
    # Note: Save action uses AdminConfig.save() for local data, Export otherwise
    #---------------------------------------------------------------------------
    def save( self, e ) :
        activeFrame = self.getActiveFrame()
        if activeFrame :
            for frame, fileName in self.frames :
                if frame == activeFrame :
                    if fileName :
                        #-------------------------------------------------------
                        # It's possible (although unlikely) that the file no
                        # longer exists.  If it does, get permission to replace
                        #-------------------------------------------------------
                        if os.path.isfile( fileName ) :
                            response = JOptionPane.showInternalConfirmDialog(
                                self.frame.getContentPane(),
                               'Overwrite existing file: %s?' % fileName,
                               'Confirm Overwrite',
                                JOptionPane.OK_CANCEL_OPTION,
                                JOptionPane.QUESTION_MESSAGE
                            )
                            if response == JOptionPane.CANCEL_OPTION :
                                return
                        #-------------------------------------------------------
                        # For an imported instance, "Save" is actually an Export
                        #-------------------------------------------------------
                        ExportTask(
                            self,
                            self.ChangesMI,
                            activeFrame.getCellData(),
                            fileName,
                            cleanup = 1
                        ).execute()
                    else :
                        SaveTask(
                            self,
                            self.ChangesMI,
                            activeFrame.getCellData()
                        ).execute()
                    break
            else :
                print '\nsave() error - activeFrame not found!'
        else :
            print '\nsave() error - no frame active.'

    #---------------------------------------------------------------------------
    # Name: discard()
    # Role: File -> Changes -> Discard : event handler
    # Note: A separate (SwingWorker) thread is used so the GUI isn't blocked by
    #       the AdminConfig.reset() call
    #---------------------------------------------------------------------------
    def discard( self, e ) :
        activeFrame = self.getActiveFrame()
        if activeFrame :
            for frame, fileName in self.frames :
                if frame == activeFrame :
                    DiscardTask(
                        self,
                        self.ChangesMI,
                        activeFrame.getCellData(),
                        fileName
                    ).execute()
                    break
            else :
                print '\ndiscard() error - activeFrame not found!'
        else :
            print '\ndiscard() error - no frame active.'

    #---------------------------------------------------------------------------
    # Name: Exit()
    # Role: File -> Exit menu item event handler: Exit application
    #---------------------------------------------------------------------------
    def Exit( self, e ) :
        msg = (
            '<html>Please save, or discard any changes<br/>'
            'before exiting the application.'
        )
        for frame, fileName in self.frames :
            if frame.getCellData().hasChanges() :
                JOptionPane.showInternalMessageDialog(
                    self.getDesktop(),
                    msg,
                    'Unsaved changes exist',
                    JOptionPane.WARNING_MESSAGE
                )
                break
        else :
            appCleanup( self.frame )


    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Called by Swing Event Dispatcher thread
    #---------------------------------------------------------------------------
    def run( self ) :

        #-----------------------------------------------------------------------
        # Starting width, height & location of the application frame
        #-----------------------------------------------------------------------
        screenSize = Toolkit.getDefaultToolkit().getScreenSize()
        w = screenSize.width  >> 1          # Use 1/2 screen width
        h = screenSize.height >> 1          # and 1/2 screen height
        x = ( screenSize.width  - w ) >> 1  # Top left corner of frame
        y = ( screenSize.height - h ) >> 1

        #-----------------------------------------------------------------------
        # Center the application frame in the window
        #-----------------------------------------------------------------------
        frame = self.frame = JFrame(
            'WASports_11',
            bounds = ( x, y, w, h ),
            defaultCloseOperation = JFrame.DISPOSE_ON_CLOSE,
            windowListener = windowAdapter( self )
        )

        #-----------------------------------------------------------------------
        # Add our menu bar to the frame, keeping a reference to the object
        #-----------------------------------------------------------------------
        frame.setJMenuBar( self.MenuBar() )

        #-----------------------------------------------------------------------
        # Internal frames require us to use a JDesktopPane()
        #-----------------------------------------------------------------------
        desktop = JDesktopPane()

        #-----------------------------------------------------------------------
        # Use local cell environment to populate cellInfo instance
        #-----------------------------------------------------------------------
        localCell = self.getLocalCellInfo()
        cellName  = localCell.getCellName()

        #-----------------------------------------------------------------------
        # Create our initial internal frame, and add it to the desktop
        #-----------------------------------------------------------------------
        self.localFrame = InternalFrame(
            title    = '0 : %s' % cellName,
            size     = Dimension( w >> 1, h >> 1 ),
            location = Point( 5, 5 ),
            cellData = localCell,
            app      = self
#           debug    = 1
        )
        self.frames.append( ( self.localFrame, None ) )
        desktop.add( self.localFrame )
        self.setDesktop( desktop )
        frame.setContentPane( desktop )
        frame.setVisible( 1 )
        self.localFrame.setSelected( 1 )

    #---------------------------------------------------------------------------
    # Name: ensureDTD()
    # Role: Ensure that WASports.dtd exists in the current working directory
    #---------------------------------------------------------------------------
    def ensureDTD( self ) :
        filename = 'WASports.dtd'
        if not exists( filename ) :
            fh = open( filename, 'w' )
            fh.write( DTD[ 1: ] )
            fh.close()
            print '\nWarning - DTD file created:', os.sep.join(
                [ os.getcwd(), filename ]
            )

#-------------------------------------------------------------------------------
# Name: windowAdapter()
# Role: WindowAdapter used to handle Application "Close" event
#-------------------------------------------------------------------------------
class windowAdapter( WindowAdapter ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor
    # Note: Save a reference to the application so the windowClosed() event
    #       handler can check for unsaved changes
    #---------------------------------------------------------------------------
    def __init__( self, app ) :
        self.app = app

    #---------------------------------------------------------------------------
    # Name: windowClosed()
    # Role: Called when the WindowClosed() event occurs
    # Note: Occasionally, a java.lang.InterruptedException is seen, in spite of
    #       calling appCleanup().
    #---------------------------------------------------------------------------
    def windowClosed( self, e ) :
        msg = (
            '<html>Please save, or discard any changes<br/>'
            'before exiting the application.'
        )
        for frame, fileName in self.app.frames :
            if frame.getCellData().hasChanges() :
                JOptionPane.showInternalMessageDialog(
                    self.app.getDesktop(),
                    msg,
                    'Unsaved changes exist',
                    JOptionPane.WARNING_MESSAGE
                )
                break
        else :
            frame = e.getWindow()
            appCleanup( frame )
        frame.setVisible( 1 )     # User chose cancel or close

#-------------------------------------------------------------------------------
# Name: XMLfiles
# Role: Define a FileFilter type of class for finding directories & XML files
#-------------------------------------------------------------------------------
class XMLfiles( FileFilter ) :

    #---------------------------------------------------------------------------
    # Name: accept()
    # Role: Return true (1) if the specified "file" is either a directory, or
    #       has an extension of ".xml"
    #---------------------------------------------------------------------------
    def accept( self, aFile ) :
        name = aFile.getAbsolutePath()
        return os.path.isdir( name ) or (
            os.path.isfile( name ) and
            name.lower().endswith( '.xml' )
        )

    #---------------------------------------------------------------------------
    # Name: getDescription()
    # Role: Description string for this file filter
    #---------------------------------------------------------------------------
    def getDescription( self ) :
        return 'XML files'

#-------------------------------------------------------------------------------
# Role: main entry point - verify that the script was executed, not imported.
#-------------------------------------------------------------------------------
if __name__ == '__main__' :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( WASports_11() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f WASports_11.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
