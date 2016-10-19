#-------------------------------------------------------------------------------
#    Name: getLinks.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Sample Jython script demonstrating the use of some Java HTML related
#          related classes.
#    Note: If no URL is provided http://www.ibm.com is used
#          This script, as written, has some issues in Jython 2.5.3
#   Usage: wsadmin -f getLinks.py [URL]
#            or
#          jython getLinks.py [URL]
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/29  rag  0.0  New - ...
#-------------------------------------------------------------------------------
import sys

from java.net              import URI

from java.io               import InputStreamReader
from java.io               import BufferedReader

from javax.swing.text.html import HTML
from javax.swing.text.html import HTMLEditorKit

from javax.swing.text.html.parser import ParserDelegator

#-------------------------------------------------------------------------------
# Name: getLinks()
# Role: Demonstrate one way to access, retrieve & process remote HTML
#-------------------------------------------------------------------------------
def getLinks( page ) :
    url  = URI( page ).toURL()
    conn = url.openConnection()
    isr  = InputStreamReader( conn.getInputStream() )
    br   = BufferedReader( isr )

    kit  = HTMLEditorKit()
    doc  = kit.createDefaultDocument()
    parser = ParserDelegator()
    callback = doc.getReader( 0 )
    parser.parse( br, callback, 1 )

    iterator = doc.getIterator( HTML.Tag.A )
    while iterator.isValid() :
        try :
            attr   = iterator.getAttributes()
            src    = attr.getAttribute( HTML.Attribute.HREF )
            start  = iterator.getStartOffset()
            fini   = iterator.getEndOffset()
            length = fini - start
            text   = doc.getText( start, length )
            print '%40s -> %s' % ( text, src )
        except :
            pass
        iterator.next()

#-------------------------------------------------------------------------------
# Name: anonymous
# Role: Verify that the script was executed, and not imported
# Note: If no URL is provided, use http://www.ibm.com as a default 
#-------------------------------------------------------------------------------
which = which = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
Usage = '''
Usage: %s getLinks.py [URL]
       No URL provided.  Using %s as a default.
'''
default = 'http://www.IBM.com'
if __name__ in [ '__main__', 'main' ] :
    argc = len( sys.argv )
    if 'AdminConfig' in dir() :
        if argc :
            webpage = sys.argv[ 0 ]
        else :
            webpage = default
            print Usage % ( which, webpage )
    else :
        if argc > 1 :
            webpage = sys.argv[ 1 ]
        else :
            webpage = default
            print Usage % ( which, webpage )
    getLinks( webpage )
else :
    print '\nError: This script should be executed, not imported.'
    print '\nUsage: %s -f %s.py [URL]' % ( which, __name__ )
    sys.exit()

sys.exit()