'''.NET Common Language Runtime (CLR) '''
import clr
import sys
import time
from robot.api import logger
import os
import re
from robot.libraries.BuiltIn import BuiltIn

from System import *
from System.Collections import *
'''Path to  CANoe DLL Files'''
sys.path.append(r'C:\Program Files (x86)\Vector CANoe 8.5\Exec32')

'''Add Reference to .NET DLL file'''
clr.AddReference('Vector.CANoe.Interop')
'''Import Namespace from DLL file'''
import CANoe


class  CANoeLib(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        logger.console(__name__+" constructor is called")
        self.name = "interactCANoe"
        self.mRelativeConfigPath = r'..\..\..\..\..\CAN_Simulation\SIM\MIB2p_Audi_MLBevo2\MIB2p_Audi_MLBevo2.cfg'
        self.mAbsoluteConfigPath = r'C:\CAN_Simulation\SIM\MIB2p_Audi_MLBevo2\MIB2p_Audi_MLBevo2.cfg'
        self.mCANoeApp = None
        self.mCANoeEnv = None
        self.mCANoeMeasurement = None
        self.mCANoeBus = None
        os.system("taskkill /im CANoe32.exe /f 2>nul >nul")

    def open_can(self):
        if self.mCANoeApp is None:
            self.mCANoeApp = CANoe.Application()
            self.mCANoeMeasurement = CANoe.Measurement(self.mCANoeApp.Measurement)
            self.mCANoeEnv = CANoe.Environment(self.mCANoeApp.Environment)
            self.mCANoeBus = CANoe.Bus(self.mCANoeApp.get_Bus("CAN"))


    def load_configuration(self, AbsoluteConfigPath = 'none'):

        if AbsoluteConfigPath!= 'none':
           self.mAbsoluteConfigPath = AbsoluteConfigPath

        logger.console("Load Configuration...")

        if self.mCANoeMeasurement.Running == True:
            self.mCANoeMeasurement.Stop
            print('Configugration stoped')

        if self.mCANoeApp != 0:
            print(self.mAbsoluteConfigPath)
            try:

                if os.path.isfile(self.mAbsoluteConfigPath):
                    logger.console("Opening CANoe...")
                    self.mAbsoluteConfigPath = re.sub('/', '\\\\', self.mAbsoluteConfigPath)
                    logger.console("absConfigPath: %s" % self.mAbsoluteConfigPath)
                    self.mCANoeApp.Open(self.mAbsoluteConfigPath, True, True)
            except:
                print('I don\'t care')

        myConfiguration = CANoe.Configuration(self.mCANoeApp.Configuration)
        ocresult = CANoe.OpenConfigurationResult(myConfiguration.OpenConfigurationResult)
        logger.console("Configuration result %s" %ocresult.result)

    def start_measurement(self):

        if (self.mCANoeApp is None) or (self.mCANoeMeasurement is None):
            raise Exception("Cant start the measurement, because CANoe was not initialized")

        if self.mCANoeMeasurement.Running is False:
            self.mCANoeMeasurement.Start()

    def stop_measurement(self):
        if (self.mCANoeApp is None) or (self.mCANoeMeasurement is None):
            return

        if self.mCANoeMeasurement.Running is True:
            self.mCANoeMeasurement.Stop()
        else:
            return

    def close_can(self):
        if not (self.mCANoeApp is None):
            os.system("taskkill /im CANoe32.exe /f 2>nul >nul")
        self.mCANoeApp = None
        self.mCANoeEnv = None
        self.mCANoeMeasurement = None
        self.mCANoeBus = None

    def set_canoe_environment_variable(self, variableName, variableValue):

        myEnvironmentVariable = CANoe.EnvironmentVariable(self.mCANoeEnv.GetVariable(variableName))
        myEnvironmentVariable.Value = variableValue

        time.sleep(1)
        logger.console("Set environment variable name: %s:%s" % (variableName, myEnvironmentVariable.Value))
        return myEnvironmentVariable.Value

    def get_canoe_environment_variable(self, variableName):

        myEnvironmentVariable = CANoe.EnvironmentVariable(self.mCANoeEnv.GetVariable(variableName))
        logger.console("Get environment variable name: %s:%s" %(variableName, myEnvironmentVariable.Value))
        #logger.console(dir(myEnvironmentVariable))
        return myEnvironmentVariable.Value

    def set_canoe_can_message(self, canMessage):
        # mCANoeEngineStatus = CANoe.Signal(CANoeBus.GetSignal(1, "EngineData", "EngineStatus"))
        # mCANoeEngineSpeed = CANoe.Signal(CANoeBus.GetSignal(1, "EngineData", "EngineSpeed"))
        # mCANoeEngineTemp = CANoe.Signal(CANoeBus.GetSignal(1, "EngineData", "EngineTemp"))

        myCanMessage = canMessage
        print("set message " % myCanMessage)

    def get_canoe_can_message(self):
        print("get message")


if __name__ == "__main__":
    obj = CANoeLib()
    obj.open_can()
    obj.load_configuration(obj.mAbsoluteConfigPath)
    obj.start_measurement()
    time.sleep(60)
    obj.start_measurement()
    time.sleep(10)
    obj.close_can()
