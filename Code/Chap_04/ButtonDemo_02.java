//------------------------------------------------------------------------------
//   Name: ButtonDemo_02.java
//   From: Swing for Jython
//     By: Robert A. (Bob) Gibson [rag]
//ISBN-13: 978-1-4824-0818-2 (paperback)
//ISBN-13: 978-1-4824-0817-5 (electronic)
//website: http://www.apress.com/978148420818
//   Role: Demonstrate how a button press event handler can be done in Java
//   Note: A Java Development Kit environment is required to compile this code
//  Usage: javac ButtonDemo_02.java
//         java  ButtonDemo_02
//History:
//  date    who  ver   Comment
//--------  ---  ---  ----------
//14/10/21  rag  0.0  New - ...
//-----------------------------------------------------------------------------
import java.awt.event.*;
import javax.swing.*;

public class ButtonDemo_02 {
    public static void main( String[] args ) {
        javax.swing.SwingUtilities.invokeLater( new Runnable() {
            public void run() {
                JFrame frame = new JFrame( "ButtonDemo" );
                frame.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE );
                JButton button = new JButton( "Press me" );
                button.addActionListener( new ActionListener() {
                    public void actionPerformed( ActionEvent ae ) {
                        System.out.println( "button pressed" );
                    };
                } );
                frame.add( button );
                frame.pack();
                frame.setVisible( true );
            }
        });
    }
}