#-------------------------------------------------------------------------------
#    Name: columnInfo3.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple wsadmin Jython script to determine column width information
#          from the AdminTask.generateSecConfigReport() command
#    Note: This script requires a WebSphere Application Server environment.
#   Usage: wsadmin -f columnInfo3.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 13/01/06  rag  0.3   Chg - which rows have column 3 with more than 75 chars?
#                            and what is the distribution of # of rows needed
#                            to display the data in column 3?
# 13/01/06  rag  0.2   Add - code to find longest substring (i.e., between '>')
# 13/01/06  rag  0.1   New - Initial attempt
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Name: columnInfo3()
# Role: Simple function to determine column width details
# Note: No Swing classes are used
#-------------------------------------------------------------------------------
def columnInfo3() :
    widths  = [ 0 ] * 6
    report = AdminTask.generateSecConfigReport()
    for line in report.splitlines()[ 2: ] :
        field = line.split( ';' )[ 2 ].strip()
        LEN = len( field )
        if LEN >= 75 :
            print '%3d:' % LEN, field
        width = int( LEN / 25 )
        widths[ width ] += 1

    print '-' * 50
    here = 25
    for width in widths :
        print '< %3d : %3d' % ( here, width )
        here += 25

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        columnInfo3()
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f columnInfo3.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
