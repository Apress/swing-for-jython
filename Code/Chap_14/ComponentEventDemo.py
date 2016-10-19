#-------------------------------------------------------------------------------
# Original Java version is available at:
# http://docs.oracle.com/javase/tutorial/uiswing/examples/events/ComponentEventDemoProject/src/events/ComponentEventDemo.java
#-------------------------------------------------------------------------------
#
# Copyright (c) 1995, 2008, Oracle and/or its affiliates. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  - Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
#  - Neither the name of Oracle or the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#    Name: ComponentEventDemo.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample Jython Swing script to monitor / display component events
#    Note: This a conversion of the ComponentEventDemo.java application from the
#          Java Swing tutorial.
#   Usage: wsadmin -f ComponentEventDemo.py
#            or
#          jython ComponentEventDemo.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/28  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import java
import sys

from   java.awt       import BorderLayout
from   java.awt       import Dimension
from   java.awt       import EventQueue
from   java.awt       import Font

from   java.awt.event import ComponentEvent
from   java.awt.event import ComponentListener

from   javax.swing    import JButton
from   javax.swing    import JCheckBox
from   javax.swing    import JFrame
from   javax.swing    import JPanel
from   javax.swing    import JScrollPane
from   javax.swing    import JTextArea

#-------------------------------------------------------------------------------
# Name: listener()
# Role: Component listener descendant to monitor events
#-------------------------------------------------------------------------------
class listener( ComponentListener ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor used to save a reference to the textarea to be updated
    #       when Component events occur
    #---------------------------------------------------------------------------
    def __init__( self, textarea ) :
        self.textarea = textarea
        self.event = {
            ComponentEvent.COMPONENT_HIDDEN  : 'Hidden' ,
            ComponentEvent.COMPONENT_MOVED   : 'Moved'  ,
            ComponentEvent.COMPONENT_RESIZED : 'Resized',
            ComponentEvent.COMPONENT_SHOWN   : 'Shown'
        }
        self.counter = 0

    #---------------------------------------------------------------------------
    # Name: displayMessage()
    # Role: Update the specified textArea with the given message
    #---------------------------------------------------------------------------
    def displayMessage( self, ce ) :
        #-----------------------------------------------------------------------
        # The original Java expression: ce.getComponent().getClass().getName()
        # fails with: TypeError: getName(): expected 1 args; got 0
        # we work-around this using the following statement syntax
        #-----------------------------------------------------------------------
        name = str(
            ce.getComponent().getClass()
        ).split( '.' )[ -1 ]
        self.textarea.append(
            '%3d: %9s --- %s\n' % (
                self.counter,
                name,
                self.event[ ce.getID() ]
            )
        )
        self.counter += 1
        self.textarea.setCaretPosition(
            self.textarea.getDocument().getLength()
        )

    #---------------------------------------------------------------------------
    # Name: componentHidden()
    # Role: Update the textArea with a "hidden" message
    #---------------------------------------------------------------------------
    def componentHidden( self, ce ) :
        self.displayMessage( ce )

    #---------------------------------------------------------------------------
    # Name: componentMoved()
    # Role: Update the textArea with a "moved" message
    #---------------------------------------------------------------------------
    def componentMoved( self, ce ) :
        self.displayMessage( ce )

    #---------------------------------------------------------------------------
    # Name: componentResized()
    # Role: Update the textArea with a "resized" message
    #---------------------------------------------------------------------------
    def componentResized( self, ce ) :
        self.displayMessage( ce )

    #---------------------------------------------------------------------------
    # Name: componentShown()
    # Role: Update the textArea with a "shown" message
    #---------------------------------------------------------------------------
    def componentShown( self, ce ) :
        self.displayMessage( ce )

#-------------------------------------------------------------------------------
# Name: ComponentEventDemo()
# Role: Used to demonstrate how to create, and display a JFrame instance
# Note: This class should be instantiated on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
class ComponentEventDemo( java.lang.Runnable ) :

    #---------------------------------------------------------------------------
    # Name: clear()
    # Role: Empty the instance textarea
    #---------------------------------------------------------------------------
    def clear( self, event ) :
        self.display.setText( '' )

    #---------------------------------------------------------------------------
    # Name: showHide()
    # Role: Make the button visible, or hidden
    #---------------------------------------------------------------------------
    def showHide( self, event ) :
        self.button.setVisible( event.getItem().isSelected() )

    #---------------------------------------------------------------------------
    # Name: run()
    # Role: Instantiate the user class
    # Note: Invoked by the Swing Event Dispatch Thread
    #---------------------------------------------------------------------------
    def run( self ) :
        frame = JFrame(
            'ComponentEventDemo',
            locationRelativeTo = None,
            defaultCloseOperation = JFrame.EXIT_ON_CLOSE
        )
        cp = frame.getContentPane()
        cp.setLayout( BorderLayout() )
        self.display = JTextArea(
            editable = 0,
            font = Font( 'Courier', Font.PLAIN, 12 )
        )
        myListener = listener( self.display )
        frame.addComponentListener( myListener )
        scrollPane = JScrollPane(
            self.display,
            preferredSize = Dimension( 350, 210 )
        )
        cp.add( scrollPane, BorderLayout.CENTER )
        panel = JPanel(
            BorderLayout(),
            componentListener = myListener
        )
        self.button = JButton(
            'Clear',
            actionPerformed = self.clear,
            componentListener = myListener
        )
        panel.add(
            self.button,
            BorderLayout.CENTER
        )
        visible = JCheckBox(
            'Button visible',
            selected = 1,
            itemStateChanged = self.showHide,
            componentListener = myListener
        )
        panel.add( visible, BorderLayout.PAGE_END )
        cp.add( panel, BorderLayout.PAGE_END )
        frame.pack()
        frame.setVisible( 1 )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and instantiate
#        the user application class on the Swing Event Dispatch Thread
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    EventQueue.invokeLater( ComponentEventDemo() )
    if 'AdminConfig' in dir() :
        raw_input( '\nPress <Enter> to terminate the application:\n' )
else :
    print '\nError: This script should be executed, not imported.\n'
    which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
    print 'Usage: %s %s.py' % ( which, __name__ )
    sys.exit()
