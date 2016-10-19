#-------------------------------------------------------------------------------
#    Name: Welcome1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: A simple, and straightforward script showing how to create a frame
#    Note: If executed using wsadmin, the frame is displayed, and the user
#          needs to press <Enter> at the command prompt to terminate the
#          Application.
#          Using the close icon ('X' in top right corner) does not terminate
#          the script, so closing the command prompt window is suggested.
#   Usage: wsadmin -f Welcome1.py
#            or
#          jython Welcome1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------
from javax.swing import JFrame
win = JFrame( 'Welcome to Jython Swing' )
win.size = ( 400, 100 )
win.show()
if 'AdminConfig' in dir() :
    raw_input( '\nPress <Enter> to terminate the application: ' )