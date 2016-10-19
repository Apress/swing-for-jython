#-------------------------------------------------------------------------------
#    Name: columnInfo4.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple wsadmin Jython script to determine column width information
#          from the AdminTask.generateSecConfigReport() command
#    Note: This script requires a WebSphere Application Server environment.
#   Usage: wsadmin -f columnInfo4.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 13/01/07  rag  0.4   Add - 2 pass processing of report help text
# 13/01/06  rag  0.3   Chg - which rows have column 3 with more than 75 chars?
#                            and what is the distribution of # of rows needed
#                            to display the data in column 3?
# 13/01/06  rag  0.2   Add - code to find longest substring (i.e., between '>')
# 13/01/06  rag  0.1   New - Initial attempt
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Name: columnInfo4()
# Role: Simple function to determine column width details
# Note: No Swing classes are used
#-------------------------------------------------------------------------------
def columnInfo4():
    text = AdminTask.generateSecConfigReport().splitlines()[ 1: ]
    widths = [ 0 ] * 5
    #---------------------------------------------------------------------------
    # Pass 1. Determine maximum width of every column
    #---------------------------------------------------------------------------
    for line in text :
        fields = line.strip().split( ';' )
        for f in range( len( fields ) ) :
            field = fields[ f ].strip()
            widths[ f ] = max( widths[ f ], len( field ) )
    print 'Widths:', widths
    #---------------------------------------------------------------------------
    # Pass 2. Display each line, left aligned in maximum width columns
    # Note: Each column is followed by a single space (i.e., ' ')
    #---------------------------------------------------------------------------
    for line in text :
        fields = line.strip().split( ';' )
        for f in range( len( fields ) ) :
            field = fields[ f ].strip()
            w = widths[ f ]
            if w :
                print '%*s;' % ( -w, field ),
        print

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        columnInfo4()
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f columnInfo4.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
