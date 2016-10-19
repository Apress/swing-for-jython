#-------------------------------------------------------------------------------
#    Name: 03_WFD.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Construct & displaying a JWindow, a JFrame & a JDialog only using
#          constructor keyword arguments.  This technique takes advantage of
#          Jython idioms.
#    Note: Using Jython it is best to close the command prompt to exit
#   Usage: C:\IBM\WebSphere\AppServer\bin\wsadmin -f 03_WFD.py
#            or
#          C:\jython2.5.3\bin\jython 03_WFD.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/20  rag  0.0  New
#-------------------------------------------------------------------------------
import javax.swing as swing

w = swing.JWindow( bounds = ( 200, 200, 200, 200 ), visible = 1 )
f = swing.JFrame( 'JFrame',
                   bounds = ( 450, 200, 200, 200 ), visible = 1 )
d = swing.JDialog( bounds = ( 700, 200, 200, 200 ), visible = 1 )

if 'AdminConfig' in dir() :
    #---------------------------------------------------------------------------
    # If executed using wsadmin, pressing <Enter> will terminate the script
    # C:\IBM\WebSphere\AppServer\bin\wsadmin -f 03_WFD.py
    #---------------------------------------------------------------------------
    raw_input( '\nPress <Enter> to terminate the application:' )