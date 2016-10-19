#-------------------------------------------------------------------------------
#    Name: columnInfo5.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple wsadmin Jython script to determine column width information
#          from the AdminTask.generateSecConfigReport() command
#    Note: This script requires a WebSphere Application Server environment.
#   Usage: wsadmin -f columnInfo5.py
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 13/01/08  rag  0.5   Add - Font Metrics to determine column text widths
# 13/01/07  rag  0.4   Add - 2 pass processing of report help text
# 13/01/06  rag  0.3   Chg - which rows have column 3 with more than 75 chars?
#                            and what is the distribution of # of rows needed
#                            to display the data in column 3?
# 13/01/06  rag  0.2   Add - code to find longest substring (i.e., between '>')
# 13/01/06  rag  0.1   New - Initial attempt
#-------------------------------------------------------------------------------

from java.awt    import Font
from javax.swing import JLabel

#-------------------------------------------------------------------------------
# Name: columnInfo5()
# Role: Use Font Metrics to determine actual width requirements of the text in
#       each column
#-------------------------------------------------------------------------------
def columnInfo5():
    #---------------------------------------------------------------------------
    # Variables used to determine pixel width
    #---------------------------------------------------------------------------
    plainFont  = Font( 'Dialog', Font.PLAIN, 12 )
    boldFont   = Font( 'Dialog', Font.BOLD , 12 )
    fmPlain    = JLabel().getFontMetrics( plainFont )
    fmBold     = JLabel().getFontMetrics( boldFont  )
    delimiters = [ '|', '/', ':', ',', '.', ' ' ]

    text = AdminTask.generateSecConfigReport().splitlines()[ 1: ]
    widths = [ 0 ] * 5
    pixels = [ 0 ] * 5
    #---------------------------------------------------------------------------
    # Pass 1. Determine maximum width of every column
    #---------------------------------------------------------------------------
    for line in text :
        fields = line.strip().split( ';' )
        fm = [ fmPlain, fmBold ][ fields[ 0 ].startswith( '_' ) ]
        for f in range( len( fields ) ) :
            field = fields[ f ].strip()
            widths[ f ] = max( widths[ f ], len( field ) )
            pixels[ f ] = max( pixels[ f ], fm.stringWidth( field ) )
    if not widths[ -1 ] :
        widths.pop()
        pixels.pop()
    print 'Pass 1:'
    print '  Widths:', ', '.join( [ '%3d' % w for w in widths ] )
    print '  Pixels:', ', '.join( [ '%3d' % p for p in pixels ] )
    #---------------------------------------------------------------------------
    # Pass 2. Process each table row, determining the
    #   - Section # (0..X)
    #   - # lines
    #   - preferred width in characters (Widths) and pixels (Pixels)
    #---------------------------------------------------------------------------
    Widths = [ 0 ] * 4
    Pixels = [ 0 ] * 4
    N = len( widths ) - 1
    for line in text :
        fields = line.strip().split( ';' )
        fm = [ fmPlain, fmBold ][ fields[ 0 ].startswith( '_' ) ]
        for f in range( N, -1, -1 ) :
            field = fields[ f ].strip()
            if f == 3 :
                links = field.split( '>' )
                lines = len( links ) + 1
                for L in range( len( links ) ) :
                    tail = [ ' >', '' ][ L == len( links ) - 1 ]
#                   temp = links[ L ].replace( 'United States Federal Information Processing Standard (FIPS)', 'FIPS' )
#                   value = '%s%s%s' % ( ' ' * L, temp, tail )
                    value = '%s%s%s' % ( ' ' * L, links[ L ], tail )
                    Widths[ f ] = max( Widths[ f ], fm.stringWidth( value ) )
                    Pixels[ f ] = max( Pixels[ f ], fm.stringWidth( value ) )
            else :
                w = int( widths[ f ] / lines )
                p = int( pixels[ f ] / lines )
                for d in delimiters :
                    if field.count( d ) > 0 :
                        parts = field.split( d )
                        value = ''
                        for part in parts :
                            if fm.stringWidth( value + d + part ) > p :
                                Pixels[ f ] = max( Pixels[ f ], fm.stringWidth( value + d ) )
                                value = part
                            else :
                                value += d + part
                        Pixels[ f ] = max( Pixels[ f ], fm.stringWidth( value ) )
                        break
#               else :
#                   print line
#                   L = len( field )
#                   if L > w :
#                       print '%3d %d %3d "%s"' % ( w, lines, L, field )
    print 'Pass 2:'
#   print '  Widths:', ', '.join( [ '%3d' % w for w in Widths ] )
    print '  Pixels:', ', '.join( [ '%3d' % p for p in Pixels ] )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        columnInfo5()
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f columnInfo4.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
