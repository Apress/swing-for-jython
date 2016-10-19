#-------------------------------------------------------------------------------
#    Name: classes.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Recursively display class name hierarchy
#    Note: Originally published at http://ibm.co/SwingEra1
#    Note: The output of this is much better in the wsadmin environment than it
#          is using Jython.  However, it servers its purpose well in this simple
#          form, so changes needed to make the Jython output more readable are
#          left as an exercise for the reader.
#   Usage: from classes import classes
#          from javax.swing import JFrame
#          classes( JFrame)
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/21  rag  0.0  New - ...
#-------------------------------------------------------------------------------
def classes( Class, pad = '' ) :
    print pad + str( Class )
    for base in Class.__bases__ :
        classes( base, pad + '| ' )
