#-------------------------------------------------------------------------------
#    Name: MethodTable1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: wsadmin Jython script to display wsadmin scripting object help text
#          with splitpanes to separate the general object description from the
#          method details.  This iteration adds code to highlight the user
#          specified text.
#    Note: This requires a WebSphere Application Server environment.
#   Usage: wsadmin -f MethodTable1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/11/03  rag  0.0  New - ...
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# Command: MethodTable
# Purpose: Sample wsadmin Jython script seeing what is needed to display the
#          method portion of the Help.help() text in a scrollable JTable.
#   Usage: wsadmin -f MethodTable.py
# Example: ./wsadmin.sh -f MethodTable.py
#-------------------------------------------------------------------------------

import java
import re
import sys

from   java.awt    import EventQueue
from   java.awt    import Font
from   java.awt    import Toolkit

from   javax.swing import JFrame
from   javax.swing import JTable
from   javax.swing import JScrollPane

#-------------------------------------------------------------------------------
# Name: MethodTable1()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class MethodTable1( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: center()
    # Role: Position the frame in the center of the screen
    # Note: The frame isn't allowed to be wider than 1/2 the screen width, or
    #       more than 1/2 the screen height.  It is resized, if necessary.
    #---------------------------------------------------------------------------
    def center( self, frame ) :
        screenSize = Toolkit.getDefaultToolkit().getScreenSize()
        frameSize  = frame.getSize()
        frameSize.width  = min( frameSize.width , screenSize.width  >> 1 )
        frameSize.height = min( frameSize.height, screenSize.height >> 1 )
        if frameSize != frame.getSize() :
            frame.setSize( frameSize )
        frame.setLocation(
            ( screenSize.width  - frameSize.width  ) >> 1,
            ( screenSize.height - frameSize.height ) >> 1
        )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'MethodTable1',
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )

        #-----------------------------------------------------------------------
        # Get the text to be processed
        #-----------------------------------------------------------------------
        helpText = Help.help().expandtabs()

        #-----------------------------------------------------------------------
        # Verify our help text parsing routine
        #-----------------------------------------------------------------------
        headings = [ 'Method', 'Description / Abstract' ]

        #-----------------------------------------------------------------------
        # Let's try to highlight every instance of "help" in the table
        #-----------------------------------------------------------------------
        data = self.parseMethodHelp( helpText )
                
        #-----------------------------------------------------------------------
        # Create the JTable using the massaged data and column headings
        #-----------------------------------------------------------------------
        table = JTable(
            data,
            headings,
            font = Font( 'Courier' , Font.PLAIN, 12 )
        )
        frame.add( JScrollPane( table ), 'Center' )

        frame.pack()
        self.center( frame )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: parseMethodHelp()
    # Role: Parse specified help text and return an array with each row having
    #       2 columns (i.e., method name, and descriptive text)
    # Note: The parsing algorithm depends upon the text being "well formed"
    #       i.e., returned from one of the wsadmin Help.<scriptingObject>() calls
    #---------------------------------------------------------------------------
    def parseMethodHelp( self, helpText ) :

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
        mo   = methRE.search( helpText )
        name = None
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
        return result

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( MethodTable1() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f MethodTable1.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
