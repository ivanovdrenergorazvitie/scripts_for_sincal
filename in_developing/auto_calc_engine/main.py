import win32com.client
import sys
import os
import textwrap

# Constants
siSimulationOK = 1101
siSimulationLoadDB_Failed = 1502

siSimulationData_LF   = 0x0001
siSimulationData_SC   = 0x0002
siSimulationData_HAR  = 0x0004
siSimulationData_MOT  = 0x0008
siSimulationData_DIM  = 0x0010
siSimulationData_MF   = 0x0020
siSimulationData_PROT = 0x0040
siSimulationData_DI   = 0x0080
siSimulationData_OPT  = 0x0100
siSimulationData_DYN  = 0x0200
siSimulationData_USYM = 0x0400
siSimulationData_REL  = 0x0800
siSimulationData_ECO  = 0x1000
siSimulationData_LA   = 0x2000
siSimulationData_AFH  = 0x4000

siSimulationData_PSTA = 0x00080000 # Pipe network steady state
siSimulationData_PDYN = 0x00100000 # Pipe network dynamics
siSimulationData_PGST = 0x00200000 # Pipe network geostationary (profile, op-series, ...)

# Simulation COM objects
SimulationSrv = None # Server for external simulation
Simulation = None    # Simulation object

strTest = "-lf"

strNetwDB = r"R:\2. Моделирование - группа\3 СОТРУДНИКИ\Денис\DEN232_files\database.db" # write the route to the .sin file
strProtDB = r"R:\2. Моделирование - группа\3 СОТРУДНИКИ\Максим\Protection.mdb" # write the route to the std prot db file
strModels = r"\\sr-nt-001\SINCAL15\Models" # write the route to the directory with models
strNetwDB = os.path.expandvars(strNetwDB) # transform the route


def WriteMessages(Simulation):
    """
    Simulation = Sincal.Simulation COM object
    """
    MessageTypes = {
        0: "",
        1: "STATUS",
        2: "INFO",
        3: "WARNING",
        4: "ERROR"
    }

    Messages = Simulation.Messages
    if Messages == None:
        return

    iMessages = Messages.Count
    print("\nSimulation Messages {}:".format(iMessages))

    wrapper = textwrap.TextWrapper(width=80, subsequent_indent=" " * 16)

    for iMsg in range(1, iMessages + 1):
        Message = Messages.Item(iMsg)
        strType = MessageTypes[Message.Type]
        lErrorNo = Message.MessageId
        strText = Message.Text
        strMsg = "{:>8} {:4d} - {}".format(strType, lErrorNo, strText)
        print(wrapper.fill(strMsg))

        Message = None
    Messages = None
    return

def CleanupAndQuit():
    global Simulation, SimulateSrv

    Simulation = None
    SimulateSrv = None

    sys.exit()

#  Write results from virtual tables in simulation
def WriteResults(Simulation, strRowObj, Attributes):
    """
    Simulation = Sincal.Simulation COM object
    strRowObj  = "LFNodeResult"
    Attributes = [("Node_ID","Node_ID"),("U","U [kV]"),("U_Un","U/Un [%]"),..]
    """
    Rows = Simulation.DB_EL().GetRowObj(strRowObj)

    if Rows == None:
        print("Error: Getting recordset for {} failed!".format(strRowObj))
        return
    if Rows.Open() != 0:
        print("Error: Unable to open recordset for {}!".format(strRowObj))
        return 0

    # Write table header
    strHdr = ""
    for i, item in enumerate(Attributes):
        if i == 0: strHdr = "{:10}".format(item[1])
        else:      strHdr += "  {:>10}".format(item[1])
    print("\n{}:".format(strRowObj))
    print("  " + strHdr + "\n  " + "-" * len(strHdr))

    # Write data
    hr = Rows.MoveFirst()
    while hr == 0:
        strRow = ""
        for i, item in enumerate(Attributes):
            if i == 0: strRow = "  {:<10}".format(Rows.Item(item[0]))
            else:      strRow += "  {:10.3f}".format(Rows.Item(item[0]))
        print(strRow)
        hr = Rows.MoveNext()

    Rows.Close()
    Rows = None
    return

try:
    SimulationSrv = win32com.client.Dispatch("Sincal.SimulationSrv")
    print("srv")
except:
    try:
        SimulationSrv = win32com.client.Dispatch("Sincal.Simulation")
        print("sim")
    except:
        SimulationSrv = None
        print("none")
if SimulationSrv != None:
    Simulation = SimulationSrv.GetSimulation()
else:
    print("Error: Creating Sincal.SimulationSrv failed!")
    sys.exit()

if strTest == "-lf":

    print("\n--- Load Flow ---")

    strCalc = "LF"

    # Setting databases & data to be loaded
    if strNetwDB != "": Simulation.DataSourceEx("NET", "JET", strNetwDB, "Admin", "")
    if strProtDB != "": Simulation.DataSourceEx("PROT", "JET", strProtDB, "Admin", "")
    if strModels != "": Simulation.MacroPath(strModels, "")
    # Set batch mode for virtual DB
    Simulation.BatchMode(1)
    Simulation.Language("EN")

    # Specify data to be considered in simulation
    Simulation.SetInputState(siSimulationData_LF | siSimulationData_SC)

    # Load data from DB
    Simulation.LoadDB(strCalc)
    print(Simulation.StatusID)
    if Simulation.StatusID == siSimulationLoadDB_Failed:
        print("Error: Load database {} failed!".format(strNetwDB))
        WriteMessages(Simulation)
        CleanupAndQuit()

    # Perform specified calculation
    Simulation.Start(strCalc)
    if Simulation.StatusID != siSimulationOK:
        WriteMessages(Simulation)
        CleanupAndQuit()

    # Write results of load flow
    strTable = "LFNodeResult"
    Attributes = [("Node_ID","Node_ID"),("U","U [kV]"),("U_Un","U/Un [%]"),("phi","phiU [°]"),("P","P [MW]"),("Q","Q [Mvar]")]
    WriteResults(Simulation,strTable,Attributes)


# Close COM instances and quit
CleanupAndQuit()
