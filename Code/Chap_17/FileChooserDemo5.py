#-------------------------------------------------------------------------------
#    Name: FileChooserDemo5.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample wsadmin Jython script demonstrating the use of the
#          JFileChooser class
#    Note: This defaults the starting folder as: C:\IBM\WebSphere which may
#          require customization
#    Note: This shows how to remove the "All files" filter
#   Usage: wsadmin -f FileChooserDemo5.py
#            or
#          jython FileChooserDemo5.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import BorderLayout
from   java.awt    import EventQueue

from   java.io     import File

from   javax.swing import JButton
from   javax.swing import JLabel
from   javax.swing import JFileChooser
from   javax.swing import JFrame

from   javax.swing.filechooser import FileSystemView
from   javax.swing.filechooser import FileNameExtensionFilter

#-------------------------------------------------------------------------------
# Name: RestrictedFileSystemView()
# Role: Class used to limit / restrict the portion of the FileSystem to which
#       the user has access through the JFileChooser
# Note: Based upon work by Rob Camick (http://tips4java.wordpress.com/)
#-------------------------------------------------------------------------------
class RestrictedFileSystemView( FileSystemView ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Class constructor
    # Note: FileSystemView.roots is read/only, so we use Roots, instead
    #---------------------------------------------------------------------------
    def __init__( self, root ) :
        FileSystemView.__init__( self )
        self.root  = root
        self.Roots = [ root ]

    #---------------------------------------------------------------------------
    # Name: createNewFolder()
    # Role: Method used to create a new folder in the current directory
    #---------------------------------------------------------------------------
    def createNewFolder( self, containingDir ) :
        folder = File( containingDir, 'New Folder' )
        folder.mkdir()
        return folder

    #---------------------------------------------------------------------------
    # Name: getDefaultDirectory()
    # Role: Return the default directory in our limited file system view
    #---------------------------------------------------------------------------
    def getDefaultDirectory( self ) :
        return self.root

    #---------------------------------------------------------------------------
    # Name: getHomeDirectory()
    # Role: Return the Home directory in our limited file system view
    #---------------------------------------------------------------------------
    def getHomeDirectory( self ) :
        return self.root

    #---------------------------------------------------------------------------
    # Name: getHomeDirectory()
    # Role: Return the Root Partitions in our limited file system view
    #---------------------------------------------------------------------------
    def getRoots( self ) :
        return self.Roots

#-------------------------------------------------------------------------------
# Name: FileChooserDemo5()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class FileChooserDemo5( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'FileChooserDemo5',
            size = ( 150, 100 ),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add(
            JButton(
                'File Open',
                actionPerformed = self.showFC
            )
        )
        self.label = JLabel( '', JLabel.CENTER )
        frame.add( self.label, BorderLayout.SOUTH )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: showFC()
    # Role: Demonstrate a JFileChooser using a RestrictedFileSystemView as well
    #       as a FileNameExtensionFilter
    #---------------------------------------------------------------------------
    def showFC( self, event ) :
        fc = JFileChooser(
            RestrictedFileSystemView(
                File( r'C:\IBM\WebSphere' )
            )
        )
        fc.addChoosableFileFilter(
            FileNameExtensionFilter(
                'XML files',
                [ 'xml' ]
            )
        )
        fc.addChoosableFileFilter(
            FileNameExtensionFilter(
                'Image files',
                'bmp,jpg,jpeg,gif,png'.split( ',' )
            )
        )
        fc.addChoosableFileFilter(
            FileNameExtensionFilter(
                'Text files',
                [ 'txt' ]
            )
        )
        fc.removeChoosableFileFilter(
            fc.getAcceptAllFileFilter()
        )
        result = fc.showOpenDialog( None )
        if result == JFileChooser.APPROVE_OPTION :
            message = 'result = "%s"' % fc.getSelectedFile()
        else :
            message = 'Request canceled by user'
        self.label.setText( message )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( FileChooserDemo5() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
