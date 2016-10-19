#-------------------------------------------------------------------------------
#    Name: ConfirmDialogDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script demonstrating various JOptionPane
#          showConfirmDialog boxes.
#    Note: This script is not referenced in the text
#   Usage: wsadmin -f ConfirmDialogDemo.py
#            or
#          jython ConfirmDialogDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt    import BorderLayout
from   java.awt    import EventQueue
from   java.awt    import FlowLayout
from   java.awt    import GridLayout

from   javax.swing import BorderFactory
from   javax.swing import BoxLayout
from   javax.swing import JButton
from   javax.swing import JCheckBox
from   javax.swing import JComboBox
from   javax.swing import JLabel
from   javax.swing import JFrame
from   javax.swing import JOptionPane
from   javax.swing import JPanel
from   javax.swing import JTextField

#-------------------------------------------------------------------------------
# Name: ConfirmDialogDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class ConfirmDialogDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = self.frame = JFrame(
            'ConfirmDialogDemo',
            size = ( 300, 300 ),
            layout = BorderLayout(),
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        frame.add( self.makePane() )
        self.label = JLabel(
            '',
            JLabel.CENTER
        )
        frame.add(
            self.label,
            BorderLayout.SOUTH
        )
        frame.setVisible( 1 )
 
    #---------------------------------------------------------------------------
    # Name: makePane()
    # Role: Instantiate, populate, and return the primary application panel
    #---------------------------------------------------------------------------
    def makePane( self ) :
        #-----------------------------------------------------------------------
        # Panel Header
        #-----------------------------------------------------------------------
        panel = JPanel( FlowLayout() )
        panel.add(
            JLabel(
                '<html><h2>ConfirmDialog options:</h2>',
                JLabel.CENTER
            )
        )

        #-----------------------------------------------------------------------
        # ConfirmDialog argument values
        #-----------------------------------------------------------------------
        choices = JPanel(
            border = BorderFactory.createEmptyBorder(
                20,          # top
                20,          # left
                 5,          # bottom
                20           # right
            ),
        )
        choices.setLayout(
            BoxLayout(
                choices,
                BoxLayout.PAGE_AXIS
            )
        )

        #-----------------------------------------------------------------------
        # Required: Message to be displayed
        #-----------------------------------------------------------------------
        picks = JPanel( GridLayout( 0, 2 ) )
        picks.add(
            JLabel(
                '<html><font color="red">Message:</font>',
                JLabel.RIGHT
            )
        )
        self.message = picks.add( JTextField( 10 ) )

        #-----------------------------------------------------------------------
        # Optional: Dialog box title
        #-----------------------------------------------------------------------
        picks.add(
            JLabel(
                'Title:',
                JLabel.RIGHT
            )
        )
        self.title = picks.add( JTextField( 10 ) )

        #-----------------------------------------------------------------------
        # Optional: Option Type
        #-----------------------------------------------------------------------
        picks.add(
            JLabel(
                'optionType:',
                JLabel.RIGHT
            )
        )
        JOP = JOptionPane    # Make the next few lines shorter
        optionTypes = [
            ( 'Yes or No'         , JOP.YES_NO_OPTION        ),
            ( 'Yes, No, or Cancel', JOP.YES_NO_CANCEL_OPTION ),
            ( 'OK or Cancel'      , JOP.OK_CANCEL_OPTION     )
        ]
        optionList, self.optionDict = [], {}
        for name, value in optionTypes :
            optionList.append( name )
            self.optionDict[ name ] = value

        self.optType = picks.add( JComboBox( optionList ) )
        picks.add( self.optType )

        #-----------------------------------------------------------------------
        # Optional: Message Type
        #-----------------------------------------------------------------------
        picks.add(
            JLabel(
                'messageType:',
                JLabel.RIGHT
            )
        )
        messageTypes = [
            ( 'Unspecified'  , None ),
            ( 'Plain'        , JOptionPane.PLAIN_MESSAGE       ),
            ( 'Error'        , JOptionPane.ERROR_MESSAGE       ),
            ( 'Informational', JOptionPane.INFORMATION_MESSAGE ),
            ( 'Warning'      , JOptionPane.WARNING_MESSAGE     ),
            ( 'Question'     , JOptionPane.QUESTION_MESSAGE    ) 
        ]
        msgList, self.msgDict = [], {}
        for name, value in messageTypes :
            msgList.append( name )
            self.msgDict[ name ] = value
        self.msgType = picks.add( JComboBox( msgList ) )
        picks.add( self.msgType )

        choices.add( picks )
        panel.add( choices )
        panel.add(
            JButton(
                'Display Dialog Box',
                actionPerformed = self.showDialog
            )
        )
        return panel

    #---------------------------------------------------------------------------
    # Name: showDialog()
    # Role: ActionListener event handler used to display the user specified
    #       Dialog
    #---------------------------------------------------------------------------
    def showDialog( self, event ) :
        msg   = self.message.getText()
        title = self.title.getText()
        opt   = self.optionDict[ self.optType.getSelectedItem() ]
        kind  = self.msgDict[ self.msgType.getSelectedItem() ]
        if msg :
            if title :
                if kind :
                    result = JOptionPane.showConfirmDialog(
                        self.frame,
                        msg,
                        title,
                        opt,
                        kind
                    )
                else :
                    result = JOptionPane.showConfirmDialog(
                        self.frame,
                        msg,
                        title,
                        opt
                    )
            else :
                result = JOptionPane.showConfirmDialog(
                    self.frame,
                    msg,
                )
            self.statusUpdate( 'result = %d' % result )
        else :
            JOptionPane.showMessageDialog(
                self.frame,
                'A message value is required!',
                'Required value not specified',
                JOptionPane.ERROR_MESSAGE
            )
            self.statusUpdate( 'Enter a message, and try again.' )

    #---------------------------------------------------------------------------
    # Name: statusUpdate()
    # Role: Update the application status field
    #---------------------------------------------------------------------------
    def statusUpdate( self, statusMessage ) :
        self.label.setText( statusMessage )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( ConfirmDialogDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
