# -----------------------------------------------
# PSS SINCAL
# Recorded  : 12.11.2021 14:42:20
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

eImportExcel_UpdateData      = 1
eImportExcel_UseShortnames   = 2
eImportExcel_RepairErrors    = 4
eImportExcel_Test            = 8

iOptions = 0
iOptions = iOptions + eImportExcel_UpdateData
iOptions = iOptions + eImportExcel_Shortname
iOptions = iOptions + eImportExcel_RepairErrors

SincalDoc.ImportExcel( r"R:\2. Моделирование - группа\3 СОТРУДНИКИ\другой Ильнур\небольшая схема_files\Копия ИМпорт.xlsx", r"R:\2. Моделирование - группа\3 СОТРУДНИКИ\другой Ильнур\небольшая схема_files\EleEng_Def.xml", iOptions )

SincalDoc = None
