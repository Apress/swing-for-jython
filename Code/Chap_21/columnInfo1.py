#-------------------------------------------------------------------------------
#    Name: columnInfo1.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple wsadmin Jython script to determine column width information
#          from the AdminTask.generateSecConfigReport() command
#    Note: This script requires a WebSphere Application Server environment.
#   Usage: wsadmin -f columnInfo1.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 13/01/06  rag  0.1   New - Initial attempt
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Name: columnInfo1()
# Role: Simple function to determine column width details
# Note: No Swing classes are used
#-------------------------------------------------------------------------------
def columnInfo1() :
    widths  = [ 0 ] * 5
    arrows  = [ 0 ] * 5
    report = AdminTask.generateSecConfigReport()
    for line in report.splitlines()[ 2: ] :
        col = 0
        for cell in line.split( ';' ) :
            widths[ col ] = max(
                len( cell.strip() ),
                widths[ col ]
            )
            arrows[ col ] = max(
                cell.count( '>' ),
                arrows[ col ]
            )
            col += 1
    print ' widths:', widths
    print ' arrows:', arrows

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        columnInfo1()
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f columnInfo1.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
