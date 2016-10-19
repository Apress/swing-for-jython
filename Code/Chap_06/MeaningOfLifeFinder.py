#-------------------------------------------------------------------------------
#    Name: MeaningOfLifeFinder.py
#    From: Swing for Jython
#      By: Robert A. (Bob) Gibson [rag]
# ISBN-13: 978-1-4824-0818-2 (paperback)
# ISBN-13: 978-1-4824-0817-5 (electronic)
# website: http://www.apress.com/978148420818
#    Role: Trivial Jython Swing code snippet translated from SwingWorker Java Doc
#          http://docs.oracle.com/javase/7/docs/api/javax/swing/SwingWorker.html
#    Note: This is an incomplete, and syntactically invalid example.
#   Usage: wsadmin -f MeaningOfLifeFinder.py
#            or
#          jython MeaningOfLifeFinder.py
# History:
#   date    who  ver   Comment
# --------  ---  ---  ----------
# 14/10/24  rag  0.0  New - ...
#-------------------------------------------------------------------------------

class MeaningOfLifeFinder( SwingWorker ) :        
    def __init__( self, labelField = None ) :     
        self.label = labelField                   
    def doInBackground( self ) :                  
        try :                                     
            self.result = findTheMeaningOfLife()  
        except :                                  
            self.result = 'Exception encountered.'
    def done( self ) :                            
        self.label.setText( self.result )         
...                                               
label = frame.add( JLabel() )                     
MeaningOfLifeFinder( label ).execute()            
