# -----------------------------------------------
# PSS SINCAL
# Recorded  : 11.11.2021 9:00:56
# -----------------------------------------------
import win32com.client
import sys
import os

SincalApp = win32com.client.Dispatch( "SIASincal.Application" )
if SincalApp == None:
    # TODO: Add your error handler code here
    os._exit( 0 )

while ( not SincalApp.IsReady() ):
    pass

SincalDoc = SincalApp.GetActiveDocument()
if SincalDoc == None:
    # TODO: Add your error handler code here
    os._exit( 0 )

SincalDoc.StartCalculation( "LF" )
iSimState = SincalDoc.GetCalculationState()
if iSimState != 0:
    # TODO: Add your error handler code here
    os._exit( 0 )

SincalDoc = None
