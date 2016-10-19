#-------------------------------------------------------------------------------
#    Name: steps.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: wsadmin Jython script to display information about the AdminTask
#          commands that have any "Steps" listed in the help text.
#    Note: This requires a WebSphere Application Server environment.
#          This is not a Swing application and was written to better understand
#          which AdminTask commands have "Steps" help text.
#   Usage: wsadmin -f steps.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/11/03  rag  0.0  New - ...
#-------------------------------------------------------------------------------

import re

#-------------------------------------------------------------------------------
# Name: steps
# Role: Process the help text for every AdminTask command, and display the names
#       of the commands that have steps (and how many steps each command has).
#
#       Additionally, metrics are displayed about AdminTask commands help text.
#-------------------------------------------------------------------------------
def steps() :
    empty = hasNone = hasSteps = numCmds = 0
    for line in AdminTask.help( '-commands' ).splitlines() :
        mo = re.match( '(\w+) -.*$', line )
        if mo :
            numCmds += 1
            cmd = mo.group( 1 )
            text = AdminTask.help( cmd ).strip()
            if text.endswith( 'Steps:' ) :
                empty += 1
            elif text.endswith( 'None' ) :
                hasNone += 1
            else :
                offset = text.rfind( 'Steps:' )
                steps  = text[ offset + 6: ]
                names  = []
                for step in steps.splitlines() :
                    mo = re.search( ' *(\w+) -.*$', step )
                    if mo :
                        names.append( mo.group( 1 ) )

                hasSteps += 1
                print '%3d (%d) : %s' % ( hasSteps, len( names ), cmd )

    print '\n   Commands:', numCmds
    print 'Empty steps: %4d %5.2f%%' % ( empty, empty * 100.0 / numCmds )
    print 'None  steps: %4d %5.2f%%' % ( hasNone, hasNone * 100.0 / numCmds )
    print 'Some  steps: %4d %5.2f%%' % ( hasSteps, hasSteps * 100.0 / numCmds )

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported and call the
#        steps() routine to process the AdminTask help text.
#-------------------------------------------------------------------------------
if __name__ == '__main__' :
    if 'AdminConfig' in dir() :
        steps()
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f steps.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
