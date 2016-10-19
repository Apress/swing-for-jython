#-------------------------------------------------------------------------------
#    Name: xmlSAX.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Simple Jython script demonstrating the use of XML SAX parsing
#    Note: This script does not require WebSphere
#   Usage: wsadmin -f xmlSAX.py <filename>
#            or
#          jython xmlSAX.py <filename>
# History:
#   date    who  ver   Comment
# --------  ---  ---   ----------
# 14/04/19  rag  0.0   New - ...
#-------------------------------------------------------------------------------
import sys

from java.io             import File
from java.io             import FileInputStream
from java.io             import InputStreamReader

from java.lang           import String

from javax.xml.parsers   import SAXParserFactory

from org.xml.sax         import InputSource

from org.xml.sax.helpers import DefaultHandler

# ENCODING = 'UTF-8'
ENCODING = 'ISO-8859-1'

#-------------------------------------------------------------------------------
# Name: SAXhandler
# Role: Implementation of SAX handler the methods of which are called by the
#       SAX parser
#-------------------------------------------------------------------------------
class SAXhandler( DefaultHandler ) :

    #---------------------------------------------------------------------------
    # Name: __init__()
    # Role: Constructor used to initialize instance attributes
    #---------------------------------------------------------------------------
    def __init__( self ) :
        self.chars  = ''
        self.prefix = ''
        self.width  = 0

    #---------------------------------------------------------------------------
    # Name: indent()
    # Role: Called to increase the indentation
    #---------------------------------------------------------------------------
    def indent( self ) :
        self.width += 2
        self.prefix = '%*s' % ( self.width, '' )

    #---------------------------------------------------------------------------
    # Name: dedent()
    # Role: Called to decrease the indentation
    #---------------------------------------------------------------------------
    def dedent( self ) :
        self.width -= 2
        self.prefix = '%*s' % ( self.width, '' )

    #---------------------------------------------------------------------------
    # Name: startElement()
    # Role: Called by SAX parser to handle XML start tag
    # Note: Use of self.chars is deferred until here for the reason noted in the
    #       characters() comment block, below.
    #---------------------------------------------------------------------------
    def startElement( self, uri, localName, name, attributes ) :
        if self.chars :
            print '%s"%s"' % ( self.prefix, self.chars )
            self.chars = ''

        attr = [
            (
                attributes.getQName( i ),
                attributes.getValue( i )
            )
            for i in range( attributes.getLength() )
        ]
        if attr :
            print '%s<%s %s>' % (
                self.prefix,
                name,
                ', '.join(
                    [
                        '%s="%s"' % ( n, v ) for n, v in attr
                    ]
                )
            )
        else :
            print '%s<%s>' % ( self.prefix, name )
        self.indent()

    #---------------------------------------------------------------------------
    # Name: endElement()
    # Role: Called by SAX parser to handle XML end tag
    # Note: Use of self.chars is deferred until here for the reason noted in the
    #       characters() comment block, below.
    #---------------------------------------------------------------------------
    def endElement( self, uri, localName, name ) :
        if self.chars :
            print '%s"%s"' % ( self.prefix, self.chars )
            self.chars = ''

        self.dedent()
        print '%s</%s>' % ( self.prefix, name )

    #---------------------------------------------------------------------------
    # Name: characters()
    # Role: Called by SAX parser to handle character text
    # Note: The SAX parser may make multiple calls to this routine to process
    #       character data.  That is why the use of self.chars is deferred until
    #       one of the *Element() methods is called
    #---------------------------------------------------------------------------
    def characters( self, ch, start, length ) :
        value = str( String( ch, start, length ) ).strip()
        if value :
            self.chars += value

    #---------------------------------------------------------------------------
    # Name: warning()
    # Role: Called by SAX parser when a warning condition is encountered
    #---------------------------------------------------------------------------
    def warning( self, e ) :
         print 'Warning:', e.getMessage()

    #---------------------------------------------------------------------------
    # Name: error()
    # Role: Called by SAX parser when a error condition is encountered
    #---------------------------------------------------------------------------
    def error( self, e ) :
         print 'Error:', e.getMessage()

    #---------------------------------------------------------------------------
    # Name: fatalError()
    # Role: Called by SAX parser when a fatal error condition is encountered
    #---------------------------------------------------------------------------
    def fatalError( self, e ) :
         print 'Fatal error:', e.getMessage()

#-------------------------------------------------------------------------------
# Name: readFileSAX()
# Role: Instantiate the object classes required to demonstrate the SAX parsing
#-------------------------------------------------------------------------------
def readFileSAX( filename ) :
    try :
        FIS     = FileInputStream( File( filename ) )
        ISR     = InputStreamReader( FIS, ENCODING )
        src     = InputSource( ISR, encoding = ENCODING )
        factory = SAXParserFactory.newInstance()
        factory.setValidating( 1 )
        parser  = factory.newSAXParser()
        parser.parse( src, SAXhandler() )
    except :
        print '\nError: %s\nvalue: %s' % sys.exc_info()[ :2 ]
    

#-------------------------------------------------------------------------------
# Name: anonymous
# Role: Verify that the script was executed, not imported, and that 1 parameter
#       was provided.
#-------------------------------------------------------------------------------
which  = [ 'wsadmin -f', 'jython' ][ 'JYTHON_JAR' in dir( sys ) ]
jython = ( which[ 0 ] == 'j' )  # 0 in wsadmin 1 in jython environment
if __name__ == '__main__' :
    argc = len( sys.argv )
    if argc == jython + 1 :
        readFileSAX( sys.argv[ jython ] )
    else :
        print '\nError - unexpected number of parameters:', argc
        print '\nUsage: %s xmlSAX.py <filename>' % which
else :
    print '\nError: This script should be executed, not imported.\n'
    print 'Usage: %s %s.py <filename>' % ( which, __name__ )
    sys.exit()
