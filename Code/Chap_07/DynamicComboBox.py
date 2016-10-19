#-------------------------------------------------------------------------------
#    Name: DynamicComboBox.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython Swing script with a modifiable JComboBox
#    Note: Changes do no persist.
#   Usage: wsadmin -f DynamicComboBox.py
#            or
#          jython DynamicComboBox.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys
from   java.awt       import BorderLayout
from   java.awt       import Component
from   java.awt       import EventQueue
from   java.awt.event import ActionListener
from   javax.swing    import JButton
from   javax.swing    import JComboBox
from   javax.swing    import JFrame
from   javax.swing    import JLabel
from   javax.swing    import JPanel

#-------------------------------------------------------------------------------
# Name: DynamicComboBox()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class DynamicComboBox( java.lang.Runnable, ActionListener ) :

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        self.frame = frame = JFrame(
            'DynamicComboBox',
            size = ( 310, 137 ),
            layout = BorderLayout(),
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        panel = JPanel()
        panel.add( JLabel( 'Pick one:' ) )
        self.choices = 'The,quick,brown,fox,jumped'.split( ',' )
        self.choices.extend( 'over,the,lazy,spam'.split( ',' ) )
        self.ComboBox = ComboBox = JComboBox(
            self.choices,
            editable = 1
        )
        ComboBox.addActionListener( self )
        panel.add( ComboBox )
        frame.add( panel, BorderLayout.NORTH )
        panel = JPanel()
        self.RemoveButton = JButton(
            'Remove',
            actionPerformed = self.remove
        )
        panel.add( self.RemoveButton )
        frame.add( panel, BorderLayout.CENTER )
        panel = JPanel( alignmentX = Component.CENTER_ALIGNMENT )
        self.msg = panel.add( JLabel( 'Make a selection' ) )
        frame.add( panel, BorderLayout.SOUTH )
        frame.setVisible( 1 )

    #---------------------------------------------------------------------------
    # Name: actionPerformed()
    # Role: Event handler associated withe the JComboBox
    #---------------------------------------------------------------------------
    def actionPerformed( self, event ) :
        cb = self.ComboBox
        item = cb.getSelectedItem().strip()
        items = [
            cb.getItemAt( i )
            for i in range( cb.getItemCount() )
        ]
        if item :
            if item not in items :
                cb.addItem( item )
                self.RemoveButton.setEnabled( 1 )
            msg = 'Selection: "%s"' % item
            self.msg.setText( msg )
        else :
            cb.setSelectedIndex( 0 )

    #---------------------------------------------------------------------------
    # Name: remove()
    # Role: Event handler associated withe the "Remove" button
    #---------------------------------------------------------------------------
    def remove( self, event ) :
        cb = self.ComboBox
        index = cb.getSelectedIndex()
        item = cb.getSelectedItem()
        try :
            cb.removeItem( item )
            self.msg.setText( 'Item removed: "%s"' % item )
        except :
            self.msg.setText( 'Remove request failed' )
        self.RemoveButton.setEnabled( cb.getItemCount() > 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( DynamicComboBox() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
