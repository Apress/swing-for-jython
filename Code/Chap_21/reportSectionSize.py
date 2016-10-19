#-------------------------------------------------------------------------------
#    Name: reportSectionSize.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: wsadmin Jython script used to process the AdminTask
#          generateSecConfigReport and determine information about the sections
#    Note: This script does not use any Swing components.
#   Usage: wsadmin -f reportSectionSize.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/11/04  rag  0.0  New - ...
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Name: processReport
#  Role: Process the results returned by the AdminTask.generateSecConfigReport()
#        method to determine the number of sections and the maximum & minimum
#        section size (i.e., the number of records within a section).
#-------------------------------------------------------------------------------
def processReport() :
    numSections, minSize, maxSize, size = 0, sys.maxint, 0, 0
    for line in AdminTask.generateSecConfigReport().splitlines()[ 2: ] :
        if line.startswith( '_' ) :
            if size :
                minSize = min( minSize, size )
                maxSize = max( maxSize, size )
            size = 0
            numSections += 1
        else :
            size += 1
    if size :
        minSize = min( minSize, size )
        maxSize = max( maxSize, size )
    print '# sections:', numSections
    print '  Min size:', minSize
    print '  Max size:', maxSize

#-------------------------------------------------------------------------------
#  Name: anonymous
#  Role: Verify that the script was executed, and not imported
#-------------------------------------------------------------------------------
if __name__ in [ '__main__', 'main' ] :
    if 'AdminConfig' in dir() :
        processReport()
    else :
        print '\nError: This script requires a WebSphere environment.'
        print 'Usage: wsadmin -f reportSectionSize.py'
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: wsadmin -f %s.py' % __name__
    sys.exit()
