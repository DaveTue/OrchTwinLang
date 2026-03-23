import fmpy 
import os


#https://github.com/CATIA-Systems/FMPy/blob/main/fmpy/fmi2.py
# seems that only supports FMU version 2

# possible implementation
class FMU:
    
    def __init__(self,modelName = 'plant', directory = os.getcwd(),
                 inputNames = [], outputNames = [], parameterNames = []):
        """
        Initializes the FMUController without a loaded model.
        """
        self.modelName = modelName #The name of the Simulink Model original
        self.directory = directory #directory of the model 
        self.modelpointer = self.directory + '\\' +self.modelName + '.fmu'
        # self.model = None
        # self.simulation = None
        self.start_time = None
        self.step_size = None
        self.end_time = None
        
        self.inputNames = []
        self.outputNames = []
        self.paramsNames = []
        self.inputRef ={}
        self.outputRef ={}
        self.paramRef ={}
        self.timeRef = {}
        if inputNames != [] and outputNames != [] and parameterNames != []:
            self.variablesDef(inputNames=inputNames, outputNames=outputNames,paramNames=parameterNames)
        
        self.exe_model = 'None'
        self.instance = 'None'
        self.initFlag = False

    def get_info(self,infoType = 'all', printInfo = True)->object:
        
        if infoType== "all":
            model_description = fmpy.read_model_description(self.modelpointer)
        elif infoType == "Variables":
            model_description = fmpy.read_model_description(self.modelpointer).modelVariables
        elif infoType == "Name":
            model_description = fmpy.read_model_description(self.modelpointer).modelName    
        elif infoType == 'star_time':
            model_info = fmpy.read_model_description(self.modelpointer)
            model_description = model_info.defaultExperiment.startTime
        elif infoType == 'end_time':
            model_info = fmpy.read_model_description(self.modelpointer)
            model_description = model_info.defaultExperiment.stopTime
        elif infoType == 'step_size':
            model_info = fmpy.read_model_description(self.modelpointer)
            model_description = model_info.defaultExperiment.stepSize
        else:
            print("the only information available is All, Variables or Name")
            return 0
            
        if printInfo == True:
            print(fmpy.dump(self.modelpointer))
        
        return model_description
    
    def variablesDef(self, inputNames = [],  outputNames = [],  paramNames = [])->tuple:
        """_summary_

        Args:
            inputNames (list, optional): _description_. Defaults to [].
            outputNames (list, optional): _description_. Defaults to [].
            paramNames (list, optional): _description_. Defaults to [].
        """
        if inputNames != []:
            self.inputNames = inputNames
        if outputNames != []:
            self.outputNames = outputNames
        if paramNames != []:
            self.paramsNames = paramNames
        
        # vrs_inputs = {}
        # vrs_outputs ={}
        # vrs_param = {}
        model_description = fmpy.read_model_description(self.modelpointer).modelVariables
        for variable in model_description:
            if variable.name in self.inputNames: 
                self.inputRef[variable.name] = variable.valueReference
            if variable.name in self.outputNames: 
                self.outputRef[variable.name] = variable.valueReference
            if variable.name in self.paramsNames: 
                self.paramRef[variable.name] = variable.valueReference
            if variable.name  == 'time':
                self.timeRef['time'] = variable.valueReference

        return (self.inputRef, self.outputRef,self.paramRef,self.timeRef) 
        
    def load_model(self, model_name = 'name', instanceName = 'instance1'):
        """
        Loads the FMU model and initializes the simulation model.
        this method does not initialize the model

        :param model_name: Path to the FMU file.
        """
        
        unzipdir = fmpy.extract(self.modelpointer)
        model_des = self.get_info(infoType = 'all', printInfo = False)
        
        #set original values for simulation, configuration can change them
        self.start_time = self.get_info(infoType = 'star_time', printInfo = False)
        self.end_time = self.get_info(infoType = 'end_time', printInfo = False)
        self.step_size = self.get_info(infoType = 'step_size', printInfo = False)
        
        self.exe_model = fmpy.fmi2.FMU2Slave(guid=model_des.guid,
                unzipDirectory=unzipdir,
                modelIdentifier=model_des.coSimulation.modelIdentifier,
                instanceName=instanceName) 
        
    def initialize_model(self,ini_val={})-> None:
        
        if self.exe_model is None:
            print("No model initialize. Please load the model first.")
            return 0
        else:
            self.exe_model.instantiate()
            self.instance = self.exe_model.component
            self.exe_model.enterInitializationMode()
            self.exe_model.exitInitializationMode()
            self.initFlag = True
        
    def advance(self, inputs_val = {}, printFlag = False)->dict:
        """Advances the FMU simulation by one step.

        Args:
            time_step (float, optional): _description_. Defaults to 1.
        """
        
        outputDict = {name:0 for name in self.outputNames }

        if self.instance is None:
            print("No instance initialized. Please load and initialize the model first.")
            return 0

        try:
            # Get the current simulation time
            current_time = self.exe_model.getReal([self.timeRef['time']])
            # print(current_time)
            # time = current_time[0] + self.step_size
            time = current_time[0] 
            # self.exe_model.setReal([self.timeRef['time']], [time])
            self.exe_model.doStep(currentCommunicationPoint=time, communicationStepSize=self.step_size)
            if printFlag == True:
                print(f"Model advanced to time {time}")
            for output in self.outputNames:
                outputDict[output] = self.get_output(output)
            return outputDict
        except Exception as e:
            print(f"Failed to advance the model: {e}")

    def set_input(self, var_name: str, var_val, printFlag =False):
        """
        Sets a value for an input variable in the FMU.

        :param var_name: Name of the input variable.
        :param var_val: Value to set for the variable.
        """
        if self.instance is None:
            print("No instance initialized. Please load and initialize the model first.")
            return 0

        try:
            self.exe_model.setReal([self.inputRef[var_name]], [var_val])
            if printFlag == True:
                print(f"Input '{var_name}' set to {var_val}.")
        except Exception as e:
            print(f"Failed to set input '{var_name}': {e}")

    def set_parameter(self, name: str, value, printFlag = False):
        """
        Sets a parameter value in the FMU.

        :param name: Name of the parameter.
        :param value: Value to set for the parameter.
        """
        if self.instance is None:
            print("No instance initialized. Please load and initialize the model first.")
            return 0

        try:
            self.exe_model.setReal([self.paramRef[name]], [value])
            if printFlag == True:
                print(f"Parameter '{name}' set to {value}.")
        except Exception as e:
            print(f"Failed to set parameter '{name}': {e}")

    def get_param(self, var_name, printFlag = False)->any:
        """_summary_

        Args:
            var_name (_type_): _description_

        Returns:
            any: _description_
        """
        if self.instance is None:
            print("No instance initialized. Please load and initialize the model first.")
            return 0

        try:
            value = self.exe_model.getReal([self.paramRef[var_name]])
            if printFlag == True:
                print(f"Parameter '{var_name}' has value {value[0]}.")
            return value[0]
        except Exception as e:
            print(f"Failed to get parameter '{var_name}': {e}")    
    
    def get_output(self, var_name: str,printFlag = 'False'):
        """
        Retrieves the value of a variable from the FMU.

        :param var_name: Name of the variable to retrieve.
        :return: Value of the variable.
        """
        if self.instance is None:
            print("No instance initialized. Please load and initialize the model first.")
            return 0

        try:
            value = self.exe_model.getReal([self.outputRef[var_name]])
            if printFlag == True:
                print(f"Output '{var_name}' has value {value[0]}.")
            return value[0]
        except Exception as e:
            print(f"Failed to get output '{var_name}': {e}")
            return None

    def set_config(self, configIdName = 't_ini', configIdVal = 0 , startConfig =  False)-> bool:
        """_summary_
            this method re-configure a simulation, but it only supports
            time configuration IdNames such as t_ini, t_period and t_step
        Args:
            configIdName (str, optional): _description_. Defaults to 't_ini'.
            configIdVal (int, optional): _description_. Defaults to 0.
        """
        if startConfig == False:
            pass

        
        if configIdName == 't_ini':
            self.exe_model.setupExperiment(startTime=configIdVal)
            self.start_time = configIdVal
            print ("Start time in FMU " + self.modelName + " is: " + str(self.start_time))
            return True
        elif configIdName == 't_period':
            startTime = self.start_time
            self.end_time = int(startTime) + configIdVal
            
            self.exe_model.setupExperiment(stopTime=self.end_time )
            
            # stopTime = self.eng.get_param(self.modelName_exe,'StopTime')
            print ("Stop time in FMU " + self.modelName + " is: " + str(self.end_time))
            return True
        elif configIdName == 't_step':
            self.step_size = configIdVal
            # self.eng.set_param(self.modelName_exe,'FixedStep', str(configIdVal))
            # t_step = self.eng.get_param(self.modelName_exe,'FixedStep')
            print ("Step time in FMU " + self.modelName + " is: " + str(self.step_size))
            return True
        else:
            print('only three possible time configurations: t_ini, t_peior and t_step, please change')
            return False
     
    def get_variable(self, var_name, printFlag = False)->any:
        """_summary_

        Args:
            var_name (_type_): _description_

        Returns:
            any: _description_
        """
        if self.instance is None:
            print("No instance initialized. Please load and initialize the model first.")
            return 0
        variables = self.inputRef
        variables.update(self.outputRef)
        variables.update(self.paramRef)
        variables.update(self.timeRef)
        try:
            
            value = self.exe_model.getReal([variables[var_name]])
            if printFlag == True:
                print(f"Variable '{var_name}' has value {value[0]}.")
            return value[0]
        except Exception as e:
            print(f"Failed to get variable '{var_name}': {e}")    
        
    def simulate (self, sim_inputs = {}) -> any:
        """_summary_

        Args:
            sim_inputs (dict, optional): _description_. Defaults to {}.

        Returns:
            _type_: _description_
        """
        if self.instance is None:
            print("No instance initialized. Please load and initialize the model first.")
            return 0
        outputVals ={name:0 for name in self.outputNames}
        inputVals = {name:0 for name in self.inputNames}
        paramVals = {name: self.get_variable(var_name=name) for name in self.paramsNames}
        
        for name, val in sim_inputs.items():
            self.set_input(var_name=name, var_val=val)
            inputVals[name] = val
        time  =  self.start_time
        # self.end_time =  end_time
        while time <= self.end_time:
            sim_time = self.get_variable(var_name='time')
            self.advance()
            time += self.step_size
            
        for output in self.outputNames:
            outputVals[output] = self.get_output(output)
        print('The simulation is carried out with the following parameters')
        print('  Initial time = ' + str(self.start_time) + '\n' '  Time step = ' + str(self.step_size) + '\n' + '  End time = ' + str(self.end_time))
        print('Parameters values:')
        for param, val in paramVals.items():
            print("  " + param + '=' + str(val))
        print('Following input values:')
        for input, val in inputVals.items():
            print("  "+input + '=' + str(val))
        print('The final result of the simulation is:')
        for output, val in outputVals.items():
            print("  " + output + '=' + str(val))
        
        return (outputVals)

    def pause(self):
        print('Dont neet to pause FMu model')
    
    def resume(self):
        print('Dont need to resume FMU model')
    
    def stop(self):
        print("dont Need to stop FMU model")
    
    def terminate(self):
        """
        this methos destroyed and liberate the instance
        """
        self.exe_model.terminate()
        self.exe_model.freeInstance()
        self.initFlag = False