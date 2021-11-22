# -----------------------------------------------
# PSS SINCAL
# Recorded  : 11.11.2021 12:51:23
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

eExportNetworkState_FullTopology     = 1
eExportNetworkState_ReducedTopology  = 2
eExportNetworkState_Selection        = 4
eExportNetworkState_SwitchState      = 1
eExportNetworkState_OperatingState   = 2
eExportNetworkState_ElementData      = 4

iIdentification = eExportNetworkState_FullTopology
iOptions = 0
iOptions = iOptions + eExportNetworkState_SwitchState
iOptions = iOptions + eExportNetworkState_OperatingState
iOptions = iOptions + eExportNetworkState_ElementData

SincalDoc.ExportNetworkState( r"R:\2. Моделирование - группа\3 СОТРУДНИКИ\другой Ильнур\cc.xml", r"R:\2. Моделирование - группа\3 СОТРУДНИКИ\другой Ильнур\ar.xml", iIdentification, iOptions )

SincalDoc = None
