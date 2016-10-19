//------------------------------------------------------------------------------
//    Name: Welcome3.java
//    From: Swing for Jython
//      By: Robert A. (Bob) Gibson [rag]
// ISBN-13: 978-1-4824-0818-2 (paperback)
// ISBN-13: 978-1-4824-0817-5 (electronic)
// website: http://www.apress.com/978148420818
//    Role: Demonstrate one advantage provided by Java compiler
//    Note: A Java compiler (Java Development Kit) is required
//   Usage: javac Welcome3.java
//          java  Welcome3
// History:
//   date    who  ver   Comment
// --------  ---  ---  ----------
// 14/10/21  rag  0.0  New - ...
//------------------------------------------------------------------------------
import javax.swing.JFrame;

public class Welcome3 {
    public static void main( String args[] ) {
        JFrame win = new JFrame( "Welcome to Java Swing" );
        win.setDefaultCloseOperation( JFrame.EXIT_ON_CLOSE );
        win.setSize( 400, 100 );
        win.show();
    }
}