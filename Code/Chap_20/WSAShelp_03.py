#-------------------------------------------------------------------------------
#    Name: WSAShelp_03.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: wsadmin Jython script to display wsadmin scripting object help text
#          with splitpanes to separate the general object description from the
#          method details.
#    Note: This requires a WebSphere Application Server environment.
#   Usage: wsadmin -f WSAShelp_03.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 12/12/11  rag  0.03  Add - Separate the scripting object help from method help
# 12/12/10  rag  0.02  New - Add a tabbed pane
# 12/12/10  rag  0.01  New - Initial application
#-------------------------------------------------------------------------------

import java
import re
import sys

from   java.awt    import Dimension
from   java.awt    import EventQueue
from   java.awt    import Font
from   java.awt    import Toolkit

from   javax.swing import JFrame
from   javax.swing import JScrollPane
from   javax.swing import JSplitPane
from   javax.swing import JTabbedPane
from   javax.swing import JTextArea

#-------------------------------------------------------------------------------
# Name: WSAShelp_03()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class WSAShelp_03( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        screenSize = Toolkit.getDefaultToolkit().getScreenSize()
        frameSize  = Dimension(        # Initial frame size
            screenSize.width  >> 2,    # 1/4 screen width
            screenSize.height >> 2     # 1/4 screen height
        )
        frame = JFrame(
            'WSAShelp_03',
            size = frameSize,
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        #-----------------------------------------------------------------------
        # Reposition the frame to be in the center of the screen
        # Note: This is done based upon initial frameSize, not packed() size...
        #-----------------------------------------------------------------------
        frame.setLocation(
            ( screenSize.width  - frameSize.width  ) >> 1,
            ( screenSize.height - frameSize.height ) >> 1
        )

        #-----------------------------------------------------------------------
        # RegExp used to locate the method name portion of the help text
        #-----------------------------------------------------------------------
        methRE = re.compile( r'^(\w+)(?:\s+.*)$', re.MULTILINE )
        monoFont = Font( 'Courier' , Font.PLAIN, 12 )

        #-----------------------------------------------------------------------
        # Create & Populate the JTabbedPane
        #-----------------------------------------------------------------------
        objs = [
            ( 'Help'        , Help         ),
            ( 'AdminApp'    , AdminApp     ),
            ( 'AdminConfig' , AdminConfig  ),
            ( 'AdminControl', AdminControl ),
            ( 'AdminTask'   , AdminTask    )
        ]
        tabs = JTabbedPane()
        for name, obj in objs :
            #-------------------------------------------------------------------
            # Use a single ScrollPane for the AdminTask help
            #-------------------------------------------------------------------
            if name.endswith( 'Task' ) :
                tabs.addTab(
                    name,
                    JScrollPane(
                        JTextArea(
                            obj.help().expandtabs(),
                            20,
                            90,
                            editable = 0,
                            font = monoFont
                        )
                    )
                )
            else :
                #---------------------------------------------------------------
                # Use a RegExp to identify where the 1st method starts.
                #---------------------------------------------------------------
                text = obj.help().expandtabs()
                mo   = re.search( methRE, text ) # Match Object
                desc = text[ :mo.start( 1 ) ].strip()
                meth = text[ mo.start( 1 ): ].strip()
                #---------------------------------------------------------------
                # The description section is before the 1st method
                #---------------------------------------------------------------
                top  = JScrollPane(
                    JTextArea(
                        desc,
                        10,
                        90,
                        editable = 0,
                        font = monoFont
                    )
                )
                #---------------------------------------------------------------
                # The method section starts at the 1st method
                #---------------------------------------------------------------
                bot  = JScrollPane(
                    JTextArea(
                        meth,
                        10,
                        90,
                        editable = 0,
                        font = monoFont
                    )
                )
                #---------------------------------------------------------------
                # For the other scripting objects, use a vertically split pane
                # with the top containing the description section, and the
                # bottom containing the method details.
                #---------------------------------------------------------------
                tabs.addTab(
                    name,
                    JSplitPane(
                        JSplitPane.VERTICAL_SPLIT,
                        top,
                        bot,
                        oneTouchExpandable = 1
                    )
                )

        #-----------------------------------------------------------------------
        # Add the tabbed pane to the frame & show the result
        #-----------------------------------------------------------------------
        frame.add( tabs )
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        EventQueue.invokeLater( WSAShelp_03() )
        raw_input( '\nPress <Enter> to terminate the application:\n' )
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f WSAShelp_03.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
