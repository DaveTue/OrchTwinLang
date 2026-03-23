#Component and Communication managers

import logging
import os
# import csv
from typing import List, Tuple
import queue
import collections
import random
import re

from src.API import MatlabAPI
from src.API import PythonAPI
from src.API import FMUAPI
from src.API import srcAPI
from src.API import sinkAPI
from src.API import localInterface_gen
from src.API.comm_protos.TCP import TCPServer as Server
from src.API.comm_protos.TCP import TCPClient as Client

import src.GlOb

# logging.basicConfig(filename='loggings\\Comm2.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Port:
    '''
    Class that reffers to the component Port in the DSL. It has two variants, inport and outport, to ease the implementation effort for extraction of data. 
    

    '''    
    def __init__(self, ID:str = "port_1", port:dict = {'name':"Port1", 'unit':"m", 'datatype':"str",'val':''}, direction:str = 'input') -> None:
    # def __init__(self, ID:str = "port_1", name:str = "Port1", unit:str = "m", datatype:str = "str",val:any = '') -> None:
        
        '''
        The attribute component is the parent component containing the port (e.g., model, sensor)
        '''
        
        self.type = ''
        self.ID =  ID
        self.direction = direction
        self.name = port['name']
        self.unit =  port['unit']
        self.datatype = port['datatype']
        try:
            self.components  = port['components']
        except:
            self.components = 1
        
        self.val = port['val']
        self.queueState = 'empty'
        self.connector = []
        self.exchReady = False
        
    def __str__(self) -> str:
        if self.components == 1: 
            text = f"{self.ID}:{self.name} as an {self.direction} with units = {self.unit} and datatype = {self.datatype}."
        else: 
            components_list = list(self.components.values())
            num_components = len(components_list)
            units = {components_list[i]:list(self.unit.values())[i] for i in range(len(components_list))}
            datatypes = {components_list[i]:list(self.datatype.values())[i] for i in range(len(components_list))}
            text = f"{self.ID}:{self.name} as an {self.direction} with {num_components} components:{components_list} units = {units} and complex datatype = {datatypes}."
        # if  num_components > 1:
            
        # else:
            
        return text
        
    def data_comp_count(self)->int:
        '''
        This method computes the number of elements the data, if the data has a primitive datatype the number of elements is one, 
        if the datatype is complex (e.i., list or dictionary) the computation define the number of elements
        '''
        size = 1
        complex = False
        datatype = self.datatype
        
        if datatype.find("list") != -1 or datatype.find("dict") != -1:
            complex = True
            
        if complex == True :
            size = datatype.count(",") + 1
        return size

class Inport(Port):
    def __init__(self, ID: str = "port_1", port: dict = { 'name': "Port1",'unit': "m",'datatype': "str",'val': '' }) -> None:
        super().__init__(ID, port)
        self.type = 'inp'
        self.direction = 'input'
        self.exchReady = True

class Outport(Port):
    def __init__(self, ID: str = "port_1", port: dict = { 'name': "Port1",'unit': "m",'datatype': "str",'val': '' }) -> None:
        super().__init__(ID, port)
        self.type = 'outp'
        self.direction = 'output'
    
    # def __init__(self, ID: str = "port_1", name: str = "Port1", unit: str = "m", datatype: str = "str",val:any = '') -> None:
    #     super().__init__(ID, name, unit, datatype,val)
        
class Component:
    
    EXEMODE = ['Live', 'Iteration', 'Initial']
    
    def __init__(self, name = "Name", ID = "Mod1") -> None:
        self.type = 'not assigned yet'
        self.name = name
        # self.ID = ID
        self.ID = ID
        self.uniqueNum = random.randint(0,1000)
        self.inputs = dict(dict())
        self.outputs = dict(dict())
        self.inports = dict()
        self.outports = dict()
        self.ports = []
        self.inputsNames = []
        self.outputsNames =[]
        self.exeMode = 'Live'
        
        # for id, input in self.inputs.items():
        #     self.inputsNames.append(input["name"])
        
    
    def __str__(self) -> str:
        text = f'Name:{self.name}\n'
        text = text + f'type:{self.type}\n'
        text2 = text
        for id, input in self.inputs.items():
            name = input['name']
            text2 = text2 + '\n' + f'input:{id}, name:{name}'
        for id, output in self.outputs.items():
            name = output['name']
            text2 = text2 + '\n' + f'output:{id}, name:{name}'

        return text2
    
    def Port_gen(self, type = 'input', port:dict = {} ):
        # def Port_gen(self, type = 'input', name: str = "Port1", 
        # unit: str = "m", datatype: str = "str", val:any = '' ):
        '''
        Generate a port object
        
        '''
        temp_dict = dict()
        temp_dict['name'] = port['name']
        try:
            components  = list(port['components'].keys())
            names = list(port['components'].values())
            # temp_dict['components'] = dict.fromkeys(components,names)
            temp_dict['components'] = {components[i]:names[i] for i in range(len(components))}
            temp_dict['value'] = dict.fromkeys(components,'')
        except:
            temp_dict['value'] = ''
            
        if type == 'input':
            input_num = len(self.inputs)
            ID_port = 'input' + str(input_num) + '_' + self.ID  
            self.inputs[ID_port] = temp_dict
            self.inports[ID_port] = Inport(ID = ID_port,port = port)
            # self.inports[ID_port] = Inport(ID = ID_port,name = name, unit = unit, datatype = datatype,val = val)
            self.ports.append(self.inports[ID_port])
            self.inputsNames.append(temp_dict['name'])
            return ID_port
        elif type == 'output':
            output_num = len(self.outputs)
            ID_port = 'output' + str(output_num) + '_' + self.ID  
            self.outputs[ID_port] = temp_dict
            self.outports[ID_port] = Outport(ID = ID_port,port = port)
            self.ports.append(self.outports[ID_port])
            self.outputsNames.append(temp_dict['name'])
            return ID_port
        else:
            print("There is only 2 types of ports: input or output; please repeat the generation with the correct type")
    
    def Port_update(self, type = 'input',  port_update = {'name': 'Temp','unit': 'm^3'} )-> str:
        """_summary_
            method can update two metadata of the object port: unit or datatype
            by detecting the name of the port (input or output)  extracting the ID
            and updating the object
        Returns:
            str: _description_ successful operation or error in the match of the name
        """
        if type == 'input':
            port_iterate = self.inports
        elif type == 'output':
            port_iterate = self.outports
        else:
            print('That type of port does not exits, only input or output type')
        updated_ports = []
        for port_ID, port_obj  in port_iterate.items():
            if port_obj.name == port_update['name']:
                if 'unit' in port_update.keys():
                    port_obj.unit = port_update['unit']
                if 'datatype' in port_update.keys():
                    port_obj.datatype = port_update['datatype']
                # just for now, this next 2 lines of code are for testing
                if 'value' in port_update.keys():
                    port_obj.val = port_update['value']
                ### if erase only the previous2 lines of code 
                print('port ' + str(port_ID) + ' has been updated')
                updated_ports.append(port_ID)
        message ="the updated ports are: \n"
        for portupdate in updated_ports:
            message = message + portupdate + '\n'
        print(message)
        return message         
    
    def input_update(self, inputs_names = [])-> dict:
        """_summary_
        method update the input of the simulation model (using interface) by the value contain in the port
        it does not update pass the values to the connector
        worked?
        Args:
            inputs (_type_): this variable can have the following possible values:
            empty -> means all inputs in the model will be updated. 
            single input name-> only that input will update its value
            multiple input names -> only the input names on that list will be updated 
            all -> means all inputs in the model will be updated. 
        """
        inputs_ID = []
        inputReturn = {}
        # prepare list
        if inputs_names == [] or inputs_names == 'all':
            inputs_names= []
            for name in self.inputs:
                inputs_ID.append(name)
        #if there is only an element of type str
        elif type(inputs_names) ==str:
            for inputID in self.inputs:
                if self.inputs[inputID]['name'] == inputs_names:
                    inputs_ID.append(inputID)
                    break
            # inputs_names = [inputs_names]
        else:
            for input_name in inputs_names:
                for inputID in self.inputs:
                    if self.inputs[inputID]['name'] == input_name:
                        inputs_ID.append(inputID)
                        break
        
        for input_ID in inputs_ID:
        #get data from connection to inport
            # self.inports[input_name].connector.push_dst()
            # get data from port to input
            if type(self.inports[input_ID].val) == dict:
                
                for name,val  in self.inports[input_name].val.items():
            
                    self.inputs[input_ID]['value'][name] = self.inports[inputs_ID].val[name] 
                    #missing how to pass this value to specific input in differnet engines
                    #example: how to pass a dictionary to matlab but also to other types of engines
            else:
                # print(self.inports[input_ID].val)
                # print(self.inputs[input_ID]['value'])
                self.inputs[input_ID]['value'] =  self.inports[input_ID].val 
                input_name = self.inputs[input_ID]['name'] 
                inputReturn[input_name] = self.inputs[input_ID]['value']
                # self.interfaceObj.set_input(input_name,self.inputs[input_ID]['value'])
        return inputReturn        
    
    def output_update(self, outputsDict = {})-> None:
        """_summary_
        method update the output of the simulation model (using interface) by the value contain in the simlation model to the 
        output value. It does not update pass the values to the connector

        Args:
            outputs_names (_type_): 
            this variable can have the following possible values:
            empty -> means all outputs in the model will be updated. 
            single output name-> only that output will update its value
            multiple output names -> only the output names on that list will be updated 
            all -> means all output in the model will be updated. 
        """
        outputs_ID = []
        outputs_IdVal ={}
        if outputsDict == {}:
            print('It cannot update an empy dictionary of outputs')
            return 0
        else:
            for name,val  in outputsDict.items():
                # outputs_names.append(name)
                for outputID in self.outputs:
                        if self.outputs[outputID]['name'] == name:
                            outputs_IdVal[outputID] = val
                            outputs_ID.append(outputID)
                            break
            
            
            
            for output_ID in outputs_ID:
                
                #get data from output to port
                if type(self.outports[output_ID].val) ==dict:
                    for name,val  in self.outports[output_ID].val.items():
                        # still missing howto extract the value from the engine intface when it is a complex value
                        self.outports[output_ID].val[name] = self.outputs[output_ID]['value'][name] 
                else:
                    # output_val = self.interfaceObj.get_output(self.outports[output_ID]['name'])
                    self.outputs[output_ID]['value'] =  outputs_IdVal[outputID] 
                    self.outports[output_ID].val = self.outputs[output_ID]['value']
            return 1        
    
    def inport_assigment(self, inputs_names = [])-> None:
        """_summary_
        pull data from the connectors to ALL the inports of the model
        """
        inputs_ID = []
        # prepare list
        if inputs_names == [] or inputs_names == 'all':
            inputs_names= []
            for name in self.inputs:
                inputs_ID.append(name)
        #if there is only an element of type str
        elif type(inputs_names) ==str:
            for inputID in self.inputs:
                if self.inputs[inputID]['name'] == inputs_names:
                    inputs_ID.append(inputID)
                    break
            # inputs_names = [inputs_names]
        else:
            for input_name in inputs_names:
                for inputID in self.inputs:
                    if self.inputs[inputID]['name'] == input_name:
                        inputs_ID.append(inputID)
                        break
        
        for input_ID in inputs_ID:
            self.inports[input_ID].connector.push_dst()
            
    
    def outport_assigment(self, outputs_names = [])-> None:
        """_summary_
        push data to the connectors from ALL the outports of the model
        """
        outputs_ID = []
        # prepare list
        if outputs_names == [] or outputs_names == 'all':
            outputs_names= []
            for name in self.outputs:
                outputs_ID.append(name)
        #if there is only an element of type str
        elif type(outputs_names) ==str:
            for outputID in self.outputs:
                if self.outputs[outputID]['name'] == outputs_names:
                    outputs_ID.append(outputID)
                    break
            # inputs_names = [inputs_names]
        else:
            for output_name in outputs_names:
                for outputID in self.outputs:
                    if self.outputs[outputID]['name'] == output_name:
                        outputs_ID.append(outputID)
                        break
        
        for output_ID in self.outputs:
        # for output_name in self.outputs:
            
            #get data from output to port
            # if type(self.outports[output_ID].val) ==dict:
            #     for name,val  in self.outports[output_ID].val.items():
            
            #         self.outports[output_ID].val[name] = self.outputs[output_ID]['value'][name] 
            # else:
            #     self.outports[output_ID].val = self.outputs[output_ID]['value'] 
            #get data from port to connector
            self.outports[output_ID].connector.pull_src()
    
class Model(Component):
    
    SIMENG = ["Simulink", "Matlab", "FMU", "Python"]
    
    def __init__(self, name="Name", ID="Mod1", SimE = "Simulink", simmod = "simulationModel", 
                 modelDir = os.getcwd(), interfaceObj = None,
                 outputs = [], inputs = [], parameters = []) -> None:
        super().__init__(name, ID)
        self.type = 'mod'
        if SimE not in Model.SIMENG:
            print("error in the supported Simulation engine:" + SimE + " not supported\n" )
            print("Currently supports:\n")
            for se in Model.SimEng:
                print(se)
        else:
            self.SimE = SimE
        self.ID="Mod" + str((random.randrange(20)))
        self.parameters = parameters
        
        self.parametersNames = []
        # for param in self.parameters:
        #     self.parametersNames.append(param['name'])
        self.paramConfig =[]
        if self.parameters != []:
            for parameter in self.parameters:
                self.parametersNames.append(parameter['name'])
                if parameter['val'] != '':
                    paramDict = {}
                    paramDict[parameter['name']] = parameter['val']
                    self.paramConfig.append(paramDict)
        self.inputsDict = []
        self.outputsDict = []
        self.outIDs = []
        self.inIDs = []
        self.dir = modelDir
        if outputs != None:
            if outputs == []:# or inputs == []:
                self.autoDef(name , modelDir,typ = 'output')
            else:
                self.manualDef(outputs= outputs, typ = 'output')
            if inputs == []:
                self.autoDef(name , modelDir, typ = 'input')
            else:
                self.manualDef(inputs = inputs, typ = 'input')
        
        if interfaceObj == None:
            self.interfaceObj = self.object_gen()
            
        else:
            self.interfaceObj = interfaceObj
       
    def object_gen(self)->object:
        """returns the interface object

        Returns:
            object: _description_
        """
        if self.SimE ==  "Simulink":
            return MatlabAPI.Simulink(self.name, self.dir)            
        elif self.SimE == "Python":
            return PythonAPI.Wrapping.load_from_csv(name=self.name, directory=self.dir)
        elif self.SimE == 'FMU':
            self.interfaceObj = FMUAPI.FMU(self.name,self.dir)
            # print(self.interfaceObj)
            inputNames = []
            outputNames = []
            if self.parameters!= [] : 
                paramNames = self.parametersNames
            else:
                paramNames = []
                print('Model ' + self.name + ' has no parameters defined, in case is wrong correct it')
            if self.inputsDict != {} :
                for input in self.inputsDict:
                    inputNames.append(input['name'])
            else:
                # inputNames = []
                print(print('Model ' + self.name + ' has no inputs  defined, this will generate errors'))
            if self.outputsDict != {}:
                for output in self.outputsDict:
                    outputNames.append(output['name'])
            else:
                # outputNames = []
                print(print('Model ' + self.name + ' has no outputs defined, this will generate errors'))
            
            refrences=self.interfaceObj.variablesDef(inputNames=inputNames, outputNames=outputNames, paramNames=paramNames)
            return self.interfaceObj    
        else:
            print(' Engine '+ self.SimE +' not currently supported')
            return None
                 
    def autoDef (self,name = "name", directory = os.getcwd(),typ = 'input' )-> str:
        """_summary_
            this method constructs the dictionary of names of inputs and outputs based on inspection of model
        Returns:
            str: _description_
        """
        if self.SimE ==  "Python":
            inputNames = self.interfaceObj.inputsNames
            outputNames = self.interfaceObj.outputsNames
            model_data = {'inports': inputNames, 'outports': outputNames, 'connections': [{}]}
        elif self.SimE == 'Simulink':
            #this only works for Simulink models at the moment
            model_inspect = localInterface_gen.model_inspection(model_name = name, directory = directory , folder_name = name)
            model_inspect.unzipped()
            model_data = model_inspect.extract()
        elif self.SimE == 'FMU':
            inputNames = self.interfaceObj.inputNames
            outputNames = self.interfaceObj.outputNames
            model_data = {'inports': inputNames, 'outports': outputNames, 'connections': [{}]}
        if typ == 'input':        
            for input in model_data['inports']:
                tempdict = {'name':"temporal", 'unit':'', 'datatype':'','val':''}
                tempdict['name'] = input
                self.inputsDict.append(tempdict)
                ID = super().Port_gen(type = 'input', port = tempdict)
                self.inIDs.append(ID)
            # print(self.inputsDict)
        if typ == 'output':
            for output in model_data['outports']:
                tempdict = {'name':"temporal", 'unit':'', 'datatype':'','val':''}
                tempdict['name'] = output
                self.outputsDict.append(tempdict)
                ID = super().Port_gen(type = 'output', port = tempdict)
                self.outIDs.append(ID)
        # print(self.inputsDict)
        # print(self.outputsDict)
        return ("dictionaries for inputs and oututs created automatically from model inspection, units and data format empty in dictionaries")
        
    def manualDef(self,inputs = [], outputs = [], typ = "input")-> str:
        """_summary_
        function generetes the inports,outputs, inputs and outports of the component class with a json value of the list of inputs and outputs
        Args:
            inputs (list, optional): _description_. Defaults to [].
            outpts (list, optional): _description_. Defaults to [].

        Returns:
            str: _description_
        """
        if inputs == []: 
            inputs = self.inputsDict
        else:
           self.inputsDict = inputs
        if outputs == []:
            outputs = self.outputsDict
        else: 
            self.outputsDict = outputs
        if typ == 'input':
            for input in inputs:
                ID_input = super().Port_gen(type = 'input',port = input)
                self.inIDs.append(ID_input)
        if typ == 'output':
            for output in outputs:
                ID_output = super().Port_gen(type = 'output',port = output)
                self.outIDs.append(ID_output)
        
    def __str__(self) -> str:
        return super().__str__()
    
    def input_update(self, inputs_names = [])-> dict:
        """_summary_
        method update the input of the simulation model (using interface) by the value contain in the port
        it does not update pass the values to the connector
        worked?
        Args:
            inputs (_type_): this variable can have the following possible values:
            empty -> means all inputs in the model will be updated. 
            single input name-> only that input will update its value
            multiple input names -> only the input names on that list will be updated 
            all -> means all inputs in the model will be updated. 
        """
        inputs_ID = []
        inputReturn = {}
        # prepare list
        if inputs_names == [] or inputs_names == 'all':
            inputs_names= []
            for name in self.inputs:
                inputs_ID.append(name)
        #if there is only an element of type str
        elif type(inputs_names) ==str:
            for inputID in self.inputs:
                if self.inputs[inputID]['name'] == inputs_names:
                    inputs_ID.append(inputID)
                    break
            # inputs_names = [inputs_names]
        else:
            for input_name in inputs_names:
                for inputID in self.inputs:
                    if self.inputs[inputID]['name'] == input_name:
                        inputs_ID.append(inputID)
                        break
        
        for input_ID in inputs_ID:
        #get data from connection to inport
            # self.inports[input_name].connector.push_dst()
            # get data from port to input
            if type(self.inports[input_ID].val) == dict:
                
                for name,val  in self.inports[input_name].val.items():
            
                    self.inputs[input_ID]['value'][name] = self.inports[inputs_ID].val[name] 
                    #missing how to pass this value to specific input in differnet engines
                    #example: how to pass a dictionary to matlab but also to other types of engines
            else:
                # print(self.inports[input_ID].val)
                # print(self.inputs[input_ID]['value'])
                self.inputs[input_ID]['value'] =  self.inports[input_ID].val 
                input_name = self.inputs[input_ID]['name'] 
                inputReturn[input_name] = self.inputs[input_ID]['value']
                #this line is the only difference with the method in Component class
                self.interfaceObj.set_input(input_name,self.inputs[input_ID]['value'])
        return inputReturn        
    
    def output_update(self, outputsDict = {})-> None:
        """_summary_
        method update the output of the simulation model (using interface) by the value contain in the simlation model to the 
        output value. It does not update pass the values to the connector

        Args:
            outputs_names (_type_): 
            this variable can have the following possible values:
            empty -> means all outputs in the model will be updated. 
            single output name-> only that output will update its value
            multiple output names -> only the output names on that list will be updated 
            all -> means all output in the model will be updated. 
        """
        outputs_ID = []
        outputs_IdVal ={}
        # print('this is the values intering the method:')
        # print(outputsDict)
        if outputsDict == {}:
            # print('It cannot update an empy dictionary of outputs')
            # return 0
            for outputName in self.outputsNames:
                # print('value extracted from sim eng:' + outputName)
                # print(self.interfaceObj.get_output(outputName))
                outputsDict[outputName] = self.interfaceObj.get_output(outputName)
        else:
            for name,val  in outputsDict.items():
                # outputs_names.append(name)
                # print('value extracted from sim eng:' + name)
                # print(self.interfaceObj.get_output(name))
                outputsDict[name] = self.interfaceObj.get_output(name)
                for outputID in self.outputs:
                    if self.outputs[outputID]['name'] == name:
                        outputs_IdVal[outputID] = outputsDict[name]
                        outputs_ID.append(outputID)
                        # print(outputID + str(outputs_IdVal[outputID]))
                        break
           
            for output_ID in outputs_ID:
                
                #get data from output to port
                if type(self.outports[output_ID].val) ==dict:
                    for name,val  in self.outports[output_ID].val.items():
                        # still missing howto extract the value from the engine intface when it is a complex value
                        self.outports[output_ID].val[name] = self.outputs[output_ID]['value'][name] 
                else:
                    # output_val = self.interfaceObj.get_output(self.outports[output_ID]['name'])
                    self.outputs[output_ID]['value'] =  outputs_IdVal[output_ID] 
                    self.outports[output_ID].val = self.outputs[output_ID]['value']
            return 1        
 
    def get_params(self)->list:
        
        if self.SimE ==  "Simulink":
            self.parameters = self.interfaceObj.get_params()
            # print(parameters)
    
    def initialize (self, ini_val={},desktop = True)-> str:
        """_summary_
        this function initialize the simulation engine and the model to start the simulation
        Returns:
            str: _state of the engine and model-> active or desactive_
        """
        # SimEng =   self.SimE 
        for inputN in self.inputsNames:
            if ini_val == {}:
                for portId, port in self.inports.items():
                    port.val = 0
            else:
                for portId, port in self.inports.items():
                    port.val = ini_val[port.name]
        if self.interfaceObj.initFlag == False:
            if self.SimE ==  "Simulink":
                # self.interfaceObj = MatlabAPI.Simulink(self.name, self.dir)
                self.interfaceObj.inputs= []
                self.interfaceObj.outputs = []
                for input in self.inputsDict:
                    self.interfaceObj.inputs.append(input['name'])  #populate the inputs list name with the names
                for output in self.outputsDict:
                    self.interfaceObj.outputs.append(output['name'])  #populate the otputs list name with the names  
        
                
                self.interfaceObj.connectToMatlab()
                if desktop == True: 
                    self.interfaceObj.eng.desktop(nargout=0)
                self.interfaceObj.load_model()
                
                self.interfaceObj.initialize_model()
                
            elif self.SimE == "Python":
                self.interfaceObj.initialize_model()
                print("already started the eng")
            
            elif self.SimE == 'FMU':
                # self.interfaceObj = FMUAPI.FMU(self.name,self.dir)
                self.interfaceObj.load_model()
                self.interfaceObj.initialize_model()
            print(f'*******Model {self.name} has been initialized**********')
            print(f'\n')
            #change the values of the parameters once the engine is running. 
            if self.paramConfig != []:
                for param in self.paramConfig:
                    self.setParam(param=param)
                    
        else:
             print(f"Engine {self.SimE} for model {self.name} has already been initialized")       
        print('*********************************************')
    
    def pause(self)->None:
        """
        This method pause a model object
        """
        self.interfaceObj.pause()
        
    def stop(self)-> None:
        """_summary_
        this function stop the model execution
        """
        self.interfaceObj.stop()
    
    def simulate (self,  ExeMode = 'Live', 
                 inputsFromConn = ["all"],outputsToConn = ["all"]) -> None:
        """_summary_
            this function executes a model following the step size define in seconds, and using the exeType to define weather
            the model will run in real-time or faster than real time
            inputsFromConn is  listwith names of the inputs obtain from the connector
            outputsToConn is  listwith names of the outputs  that will update the connector
            any input or output not on the list will obtain its value from the ports and not update the conector
            
        Args:
            inputsFromConn (list, optional): _description_. Defaults to ["all"].
            outputsToConn (list, optional): _description_. Defaults to ["all"].
        """
        # val = val + 1
                    
        if inputsFromConn == ["all"] and ExeMode == 'Live':
            inputsFromConn = self.inputsNames
        
        if outputsToConn == ["all"] and ExeMode == 'Live':
            outputsToConn = self.outputsNames
        
        # if len(inputsFromConn) != 0 and ExeMode == 'Live':
        if len(inputsFromConn) != 0 and ExeMode != 'Initial':
            self.inport_assigment (inputsFromConn)
            print('pulling data from connector')
        
        input_val = self.input_update(inputs_names = self.inputsNames)
        print(input_val)
        for name in input_val:
            self.interfaceObj.set_input(name,input_val[name])
        output_vals = self.interfaceObj.simulate(input_val)
        print(output_vals)
        self.output_update( outputsDict = output_vals)
    
        
        if len(outputsToConn) != 0:
            self.outport_assigment(outputsToConn)
    
    def runStep (self,  ExeMode = 'Live', 
                 inputsFromConn = ["all"],outputsToConn = ["all"]) -> None:
        """_summary_
            this function executes a model following the step size define in seconds, and using the exeType to define weather
            the model will run in real-time or faster than real time
            inputsFromConn is  listwith names of the inputs obtain from the connector
            outputsToConn is  listwith names of the outputs  that will update the connector
            any input or output not on the list will obtain its value from the ports and not update the conector
            
        Args:
            inputsFromConn (list, optional): _description_. Defaults to ["all"].
            outputsToConn (list, optional): _description_. Defaults to ["all"].
        """
        # val = val + 1
                    
        if inputsFromConn == ["all"] and ExeMode == 'Live':
            inputsFromConn = self.inputsNames
        
        if outputsToConn == ["all"] and ExeMode == 'Live':
            outputsToConn = self.outputsNames
        
        # if len(inputsFromConn) != 0 and ExeMode == 'Live':
        if len(inputsFromConn) != 0 and ExeMode != 'Initial':
            print(f'Trying to pull data from connector model {self.name}')
            self.inport_assigment (inputsFromConn)
            print('pulling data from connector')
        
        input_val = self.input_update(inputs_names = self.inputsNames)
        print(input_val)
        for name in input_val:
            self.interfaceObj.set_input(name,input_val[name])
        output_vals = self.interfaceObj.advance(input_val)
        print(output_vals)
        self.output_update( outputsDict = output_vals)
    
        
        if len(outputsToConn) != 0:
            self.outport_assigment(outputsToConn)
      
    def runProcessing(self, mode = "Live")->None :
        """_summary_

        Returns:
            _type_: _description_
        """
        if self.SimE != 'Python':
            print('SimEng Error: This function can only be used for python models with a type DataProc')
            return 0
        if self.interfaceObj.typ != 'DataProc':
            print('Type Error: This function can only be used for python models with a type DataProc ')
            return 0
        
        inputsFromConn = self.inputsNames
        outputsToConn = self.outputsNames
        
        if mode == 'Live':
            self.inport_assigment (inputsFromConn)
            print('pulling data from connector')
        
        input_val = self.input_update(inputs_names = self.inputsNames)
        print(input_val)
        for name in input_val:
            self.interfaceObj.set_input(name,input_val[name])
        output_vals = self.interfaceObj.execution()
        print(output_vals)
        self.output_update( outputsDict = output_vals)

        if mode == 'Live':
            self.outport_assigment(outputsToConn)
    
    def setParam(self,param = {"t_init":0})->None:
        """_summary_
            set the define parameters with the define values. 
        Returns:
            _type_: _description_
        """
        # for name, value in param.items():
        # print(param)
        name = list(param.keys())[0]
        # print(name)
        value = float(param[name])
        # print(value)
        if self.SimE ==  "Simulink":
            self.interfaceObj.set_parameter(name = name, value = value)
        elif self.SimE == 'FMU':
            self.interfaceObj.set_parameter(name = name, value = value) 
        elif self.SimE == 'Python':
            self.interfaceObj.set_parameter(name = name, value = value) 
   
    def setConfig(self,confParam = {"t_init":0})->None:
        """_summary_

        Args:
            confParam (dict, optional): _description_. Defaults to {"t_init":0}.
        """
        startedConfig = False
        for name,val in confParam.items():
            if startedConfig == False:
                startedConfig = self.interfaceObj.set_config(configIdName=name,configIdVal=val)
                print('flag for start config' + str(startedConfig))
            else:
                startedConfig = self.interfaceObj.set_config(configIdName=name,configIdVal=val, startConfig= startedConfig)
               
    def modelControl(ctrlAction = "pause")-> Tuple:
        """_summary_
             define the control value of a mode. Only one of the three control actions can be set: pause, resume, stop
        Args:
            ctrlAction (str, optional): _description_. Defaults to "pause".

        Returns:
            Tuple: _description_ the status of all control actions (e.g., ({"pause":true},{"stop":false},{"resume":false})
        """

class ConfigComp(Model):
    
    def __init__(self, name="Name", ID="Mod1", SimE= None, simmod="simulationModel", 
                 modelDir=os.getcwd(), ModelObj = None, interfaceObj = None,
                 outputs=[], inputs=[], parameters=[]):
        
        if ModelObj == None:
            self.interfaceObj = None
            raise ValueError (f'Error in defining configuration component {self.name}, the interface object comes from a model component ')
            # print(f'Error in defining configuration component {self.name}, the interface object comes from a model component ')
        else:
            self.ModelObj = ModelObj
        
        # self.interfaceObj = self.obj_extraction(ModelObj)
        if SimE == None and interfaceObj != None:
           self.SimE = interfaceObj.SimE 
        #    SimE = self.SimE
        
        super().__init__(name, ID, SimE, simmod, modelDir, interfaceObj, outputs, inputs, parameters)
        self.paramConfig =[]
        self.type = 'config'
        
        if SimE not in Model.SIMENG:
            print("error in the supported Simulation engine:" + SimE + " not supported\n" )
            print("Currently supports:\n")
            for se in Model.SimEng:
                print(se)
        else:
            self.SimE = SimE
        self.ID="Config" + str((random.randrange(20)))
        self.parameters = None
        self.parametersNames = None
        self.paramConfig =None
        self.inputsDict = []
        self.outputsDict = None
        self.outIDs = None
        self.inIDs = []
        self.dir = modelDir
        
        if inputs == []:
            self.autoDef()
        else:
            self.manualDef(inputs = inputs)
        
        # if ModelObj == None:
        #     self.interfaceObj = None
        #     raise ValueError (f'Error in defining configuration component {self.name}, the interface object comes from a model component ')
        #     # print(f'Error in defining configuration component {self.name}, the interface object comes from a model component ')
        # else:
        #     self.interfaceObj = self.obj_extraction(ModelObj)   
    
    def object_gen(self)-> object:
        """overwrite the original object generation to extract the interfaceObj 
        from the reference model

        Returns:
            object: _description_
        """
        obj = self.obj_extraction(self.ModelObj)
        return obj      
    
    def obj_extraction(self, interfaceObj = None)->object:
        """_summary_

        Args:
            interfaceObj (_type_, optional): _description_. Defaults to None.

        Returns:
            object: _description_
        """
        #check interface object type
        if type(interfaceObj) == Model:
            #extract interface object from model:
            obj = interfaceObj.interfaceObj
        else:
            print(f'Error the interface object input for {self.name} configuration component needs to be a type Model')
            return None
        return obj
    
    def input_update(self, inputs_names = [])-> dict:
        """_summary_
        method update the input of the simulation model (using interface) by the value contain in the port
        it does not update pass the values to the connector
        worked?
        Args:
            inputs (_type_): this variable can have the following possible values:
            empty -> means all inputs in the model will be updated. 
            single input name-> only that input will update its value
            multiple input names -> only the input names on that list will be updated 
            all -> means all inputs in the model will be updated. 
        """
        inputs_ID = []
        inputReturn = {}
        # prepare list
        if inputs_names == [] or inputs_names == 'all':
            inputs_names= []
            for name in self.inputs:
                inputs_ID.append(name)
        #if there is only an element of type str
        elif type(inputs_names) ==str:
            for inputID in self.inputs:
                if self.inputs[inputID]['name'] == inputs_names:
                    inputs_ID.append(inputID)
                    break
            # inputs_names = [inputs_names]
        else:
            for input_name in inputs_names:
                for inputID in self.inputs:
                    if self.inputs[inputID]['name'] == input_name:
                        inputs_ID.append(inputID)
                        break
        
        for input_ID in inputs_ID:
        #get data from connection to inport
            # self.inports[input_name].connector.push_dst()
            # get data from port to input
            if type(self.inports[input_ID].val) == dict:
                
                for name,val  in self.inports[input_name].val.items():
            
                    self.inputs[input_ID]['value'][name] = self.inports[inputs_ID].val[name] 
                    #missing how to pass this value to specific input in differnet engines
                    #example: how to pass a dictionary to matlab but also to other types of engines
            else:
                # print(self.inports[input_ID].val)
                # print(self.inputs[input_ID]['value'])
                self.inputs[input_ID]['value'] =  self.inports[input_ID].val 
                input_name = self.inputs[input_ID]['name'] 
                inputReturn[input_name] = self.inputs[input_ID]['value']
                # self.interfaceObj.set_input(input_name,self.inputs[input_ID]['value'])
        return inputReturn        
    
    def autoDef(self)->None:
        if type(self.interfaceObj) == 'FMU': 
            inputNames = self.interfaceObj.paramsNames
        elif type(self.interfaceObj) == 'Python':
            inputNames = self.interfaceObj.parametersNames
        else: 
            inputNames = self.interfaceObj.parameterNames
        
        for input in inputNames:
                tempdict = {'name':"temporal", 'unit':'', 'datatype':'','val':''}
                tempdict['name'] = input
                self.inputDIct.append(tempdict)
                ID = super().Port_gen(type = 'input', port = tempdict)
                self.inIDs.append(ID)
        print('Dont fortget to update the unit, and data type of the inputs since they are not defined in the sink')
    
    def manualDef(self, inputs = [])->None:
        """_summary_
        function generetes the outputs and outports of the component class with a json value of the list of outputs
        Args:
            outpts (list, optional): _description_. Defaults to [].

        Returns:
            str: _description_
        """
        if inputs == []:
            inputs = self.inputDIct
        else: 
            self.inputDIct = inputs
       
        for input in inputs:
            # print(output)
            ID_input = super().Port_gen(type = 'input',port = input)
            self.inIDs.append(ID_input)

    def setParam(self,ExeMode = 'Live', inputsFromConn = ["all"])->None:
        """_summary_
            set the define parameters with the define values. 
        Returns:
            _type_: _description_
        """
        if inputsFromConn == ["all"] and ExeMode == 'Live':
            inputsFromConn = self.inputsNames
        
        if len(inputsFromConn) != 0 and ExeMode != 'Initial':
            self.inport_assigment (inputsFromConn)
            print('pulling data from connector')
        
        input_val = self.input_update(inputs_names = self.inputsNames)
        print(input_val)
        for name in input_val:
            self.interfaceObj.set_parameter(name = name, value = float(input_val[name]))
        
        # name = list(param.keys())[0]
        # # print(name)
        # value = float(param[name])
        

   
class Source (Component):
   
    def __init__(self, name="tilt", ID="Mod1", 
                config = {"type" : "freq", "unit": "s", "occurrences_per_unit":10},
                interfaceType = 'TCP-IP', interfaceObj = None,
                # sending_port = 55000, receiving_ports = [55001],
                outputs = [{'name':"temperature", 'unit':'C', 'datatype':'float','val':''},
                           {'name':"sg", 'unit':'', 'datatype':'float','val':''}]) -> None:
        
        super().__init__(name, ID)
        self.inputs = None
        self.inports = None
        self.inputsNames = None
        
        self.interfaceType = interfaceType
        if interfaceObj == None:
            self.interfaceObj = self.object_gen()
            
        else:
            self.interfaceObj = interfaceObj

        self.client = None
        self.outIDs = []
        self.outputsDict = []
        # self.exeMode = 'Live'
        
        # self.send_ch = sending_port
        # self.recv_chs = receiving_ports
        
        self.config = config
        self.activationFlag = False
        
        if outputs != []:
            self.manualDef(outputs=outputs)
        elif self.interfaceObj != None:
            self.autoDef()
        else:
            print(' Need to define an interfacing object and define the output  name')
        
        consistency =self.checkconsistency()
        if consistency == False:
            print('Check message of consistency, since there are error(s) in the definition of the variables')
       
    def __str__(self) -> str:
        return super().__str__()
    
    def checkconsistency(self)->bool:
        sens_names = self.interfaceObj.outputsNames
        outputNames = self.outputsNames
        consistencyFlag = {name: True  for name in outputNames}
        consistent = True
        for output in outputNames:
            if output not in sens_names:
                consistencyFlag[output] = False
                consistent = False
        sensNamesmissing = []
        for name in sens_names:
            if name not in outputNames:
                sensNamesmissing.append(name)
        
        if consistent == False:
            print('The definition of the variables is not consistent')
            for name, flag in consistencyFlag.items():
                if flag == False:
                    print('Consistency error, output ' + name +  'is not defined in sensor interface')
        else:
            print('The variables defined are connsistent with the sensor component ' + self.name)
            
        if len(sensNamesmissing) >0 :
            for name in sensNamesmissing:
                print('These variable in the sensor' + self.name + ' is not being used: ' + name)
            
        return consistent
    
    def object_gen(self)->object:
        """generate a sensor object      

        Returns:
            object: sensor object
        """
        return srcAPI.Sensor.load_from_csv(name=self.name, directory='')
    
    def autoDef(self):
        outputnames = self.interfaceObj.outputNames
        for output in outputnames:
                tempdict = {'name':"temporal", 'unit':'', 'datatype':'','val':''}
                tempdict['name'] = output
                self.outputsDict.append(tempdict)
                ID = super().Port_gen(type = 'output', port = tempdict)
                self.outIDs.append(ID)
        print('Dont fortget to update the unit, and data type of the outputs since they are not defined in the sensor')
    
    def manualDef(self, outputs = []):
        """_summary_
        function generetes the outputs and outports of the component class with a json value of the list of outputs
        Args:
            outpts (list, optional): _description_. Defaults to [].

        Returns:
            str: _description_
        """
        if outputs == []:
            outputs = self.outputsDict
        else: 
            self.outputsDict = outputs
       
        for output in outputs:
            # print(output)
            ID_output = super().Port_gen(type = 'output',port = output)
            self.outIDs.append(ID_output)

    def controller(self, command = 'start', config = {"type" : "freq", "unit": "s", "occurrences_per_unit":1})->None:
        """this method activate the functionality of the sensor, 
        """
        if command == 'start':
            self.interfaceObj.start(self.client)
            print('Sensor ' + self.name + ' has been activated and functioning')
        elif command == 'stop':
            self.interfaceObj.stop(self.client)
        elif command == 'pause':
            self.interfaceObj.pause(self.client)
        elif command == 'resume':
            self.interfaceObj.resume(self.client)
        elif command == 'configuration':
            self.interfaceObj.set_config(self.client,config)
            
        else:
            print('Commmand:' + command + ' is not supported. Only: start, stop, pause, resume and config are supported')
            return 0
       
    def initialize(self):
        self.client = self.interfaceObj.initialize_comm()
        # self.interfaceObj.client = self.client
    
    def pull_data(self, outputName = ['all'], testMode = 'off')-> dict:
        """_summary_

        Returns:
            any: _description_
        """
        self.interfaceObj.client = self.client
        if outputName== ['all']:
            outputName = self.outputsNames
            outputsToConn = self.outputsNames
        outputDict = {name:0 for name in outputName}
        
        for name in outputName:
            outputDict[name] = self.interfaceObj.get_output(var_name = name, client = self.client)
        
        self.output_update( outputsDict = outputDict)
        if testMode == 'off':
            self.outport_assigment(outputsToConn)
        
        return outputDict

class Sink (Component):
    def __init__(self, name="monitor", ID="Sink1",              
                config = {"type" : "freq", "unit": "s", "occurrences_per_unit":1},
                interfaceType = 'TCP-IP', interfaceObj = None,
                inputs = [{'name':"temperature", 'unit':'C', 'datatype':'float','val':''},
                           {'name':"sg", 'unit':'', 'datatype':'float','val':''},
                           {'name':"real_temperature", 'unit':'C', 'datatype':'float','val':''},
                           {'name':"real_sg", 'unit':'', 'datatype':'float','val':''},
                           {'name':"simTime", 'unit':'s', 'datatype':'float','val':''}
                           ]) -> None:
        super().__init__(name, ID)
        self.outputs = None
        self.outports = None
        self.outputsNames = None
        
        self.interfaceType = interfaceType
        if interfaceObj == None:
            self.interfaceObj = self.object_gen()
            
        else:
            self.interfaceObj = interfaceObj

        self.client =None
        
        self.inIDs = []
        self.inputDIct = []
        
        self.config = config
        self.activationFlag = False
        
        if inputs != []:
            self.manualDef(inputs=inputs)
        elif self.interfaceObj != None:
            self.autoDef()
        else:
            print(' Need to define an interfacing object and define the output  name')
        
        consistency =self.checkconsistency()
        if consistency == False:
            print('Check message of consistency, since there are error(s) in the definition of the variables')
        
    def __str__(self) -> str:
        return super().__str__()
    
    def checkconsistency(self)->bool:
        sink_names = self.interfaceObj.inputsNames
        inputsNames = self.inputsNames
        consistencyFlag = {name: True  for name in inputsNames}
        consistent = True
        for output in inputsNames:
            if output not in sink_names:
                consistencyFlag[output] = False
                consistent = False
        sinkNamesmissing = []
        for name in sink_names:
            if name not in inputsNames:
                sinkNamesmissing.append(name)
        
        if consistent == False:
            print('The definition of the variables is not consistent')
            for name, flag in consistencyFlag.items():
                if flag == False:
                    print('Consistency error, input ' + name +  'is not defined in sink interface')
        else:
            print('The variables defined are connsistent with the sink component ' + self.name)
            
        if len(sinkNamesmissing) > 0 :
            for name in sinkNamesmissing:
                print('These variable in the sink '+ self.name +' is not being used: ' + name)
            
        return consistent
    
    def object_gen(self)->object:
        """generate a sink object      

        Returns:
            object: sink object
        """
        return sinkAPI.Sink.load_from_csv(name=self.name,directory='')
  
    def autoDef(self)->None:
        inputNames = self.interfaceObj.inputNames
        for input in inputNames:
                tempdict = {'name':"temporal", 'unit':'', 'datatype':'','val':''}
                tempdict['name'] = input
                self.inputDIct.append(tempdict)
                ID = super().Port_gen(type = 'input', port = tempdict)
                self.inIDs.append(ID)
        print('Dont fortget to update the unit, and data type of the inputs since they are not defined in the sink')
    
    def manualDef(self, inputs = [])->None:
        """_summary_
        function generetes the outputs and outports of the component class with a json value of the list of outputs
        Args:
            outpts (list, optional): _description_. Defaults to [].

        Returns:
            str: _description_
        """
        if inputs == []:
            inputs = self.inputDIct
        else: 
            self.inputDIct = inputs
       
        for input in inputs:
            # print(output)
            ID_input = super().Port_gen(type = 'input',port = input)
            self.inIDs.append(ID_input)

    def controller(self, command = 'start', config = {"type" : "freq", "unit": "s", "occurrences_per_unit":1})->None:
        """this method activate the functionality of the sensor, 
        """
        if command == 'start':
            self.interfaceObj.start(self.client)
            print('Sensor ' + self.name + ' has been activated and functioning')
        elif command == 'stop':
            self.interfaceObj.stop(self.client)
        elif command == 'pause':
            self.interfaceObj.pause(self.client)
        elif command == 'resume':
            self.interfaceObj.resume(self.client)
        elif command == 'configuration':
            self.interfaceObj.set_config(config,self.client)  
        else:
            print('Commmand:' + command + ' is not supported. Only: start, stop, pause, resume and config are supported')
            return 0
       
    def initialize(self):
        self.client = self.interfaceObj.initialize_comm()
    
    def push_data(self, inputName = ['all'], testMode = 'off')-> dict:
        """_summary_

        Returns:
            any: _description_
        """
        
        if inputName== ['all']:
            inputName = self.inputsNames
            inputsFromConn = self.inputsNames
        else:
            inputsFromConn = inputName
            
        inputDict = {name:0 for name in inputName}
        
        if testMode == 'off':
            self.inport_assigment (inputsFromConn)
            print('pulling data from connector')
        
        input_val = self.input_update(inputs_names = self.inputsNames)
        print(input_val)
        
        for name in inputName:
            inputDict[name] = self.interfaceObj.set_input(var_name = name, value = input_val[name],client = self.client)
        
        # self.output_update( outputsDict = outputDict)
        # if testMode == 'off':
        #     self.outport_assigment(outputsToConn)
        
        # return outputDict

    
class Duplicator(Component):
    '''
        this element cannot dupplicate complex data types (lists or dictionaries)
    '''
    def __init__(self, name="duplicator", ID="dup1",input:dict = {'name': 'input', 'unit' : 'K', 'datatype':'str'}, num_outputs:int = 2) -> None:
        
        super().__init__(name, ID)        
        self.name = name + str(self.uniqueNum)
        self.type = 'dup'
        
        if type(input) == list:
            input = input[0]
            print(f'Duplicator {self.name} can only take one input. Only taking the first input define')
            print('Input considered:')
            print(input)
        
        self.inID = super().Port_gen(type = 'input', port = input )
        if abs(int(num_outputs)) < 2:
            self.num_outputs = 2
        else:
            self.num_outputs = abs(int(num_outputs))
        self.outID = []
        
        
            
        self.dup_def(input)
    
    def dup_def(self, input):
        #names of each output must be unique
        idx = 0
        output = input
        name = input['name']
        outputNames = []
        for out in range(self.num_outputs):
            output['name'] = name + str(out)
            outputNames.append(output['name'])
            ID = super().Port_gen(type = 'output', port = output)
            self.outID.append(ID)
        print(f"For duplicator {self.name}, the names of the outputs are:")
        for o in outputNames:
            print(o)
            
                
    def behavior(self, inputsFromConn = ['all'],outputsToConn = ['all']):
        '''
        This method duplicates the input value  to all outputs
        '''
        
        #get the data from the connector
        if inputsFromConn == ["all"] :
            inputsFromConn = self.inputsNames
        
        if outputsToConn == ["all"]:
            outputsToConn = self.outputsNames
        
        # if len(inputsFromConn) != 0 and ExeMode == 'Live':
        if len(inputsFromConn) != 0:
            self.inport_assigment (inputsFromConn)
            print('pulling data from connector')
        # self.inport_assigment()
        #get the value from the ports into the inputs
        self.input_update()
        
        #UNIQUE CAPABILITY FOR THIS COMMUNICATION COMPONENT
        for output in self.outputs.items():
            output[1]['value'] = self.inputs[self.inID]['value']
            print(output)
            
        
        #OUTPUT UPDATE FOR THIS COMPONENT
        outputsDict = {}
        for iD,output in self.outputs.items():
            name = output['name']
        #    self.outputs[iD]['value'] = assignedVals[name]
            outputsDict[name] = output['value']
        # return assignedVals
        print(outputsDict)
        # copy the output values into the outport
        self.output_update(outputsDict)
        #send the data to the connector
        self.outport_assigment(outputsToConn)

    def __str__(self) -> str:
        text = "input =" + str(self.inputs.items()) + "\n"
        item_num = 0
        for o in self.outputs.items():
            item_num += 1
            text = text + "output_" + str(item_num) +"=" + str(o) + "\n"
            
        return text
            
    
class Aggreggator(Component):
    
    def __init__(self, name="aggreggator", ID="Agg1", output_name:str =  'output', inputs:any = [] ) -> None:
        super().__init__(name, ID)
        self.name = name + str(self.uniqueNum)
        self.type = 'agg'
        #the data type has to always be a dictionary in the output
        self.outID = ''
        # self.output_name = output_name
        self.inID= []
        self.inputs_dt = []
        self.inputs_unit = []
        if type(inputs) == list:
            self.var_names = [name['name'] for name in inputs]
        elif type(inputs) == dict:
            items = tuple(inputs.items())
            self.var_names = [name[1]['name'] for name in items]
        self.agg_def(output_name, inputs)
        
    def agg_def(self, output_name,inputs):
        
        if type(inputs) == list:
            #'name':'Conc_y', 'unit':'mol/l','datatype': 'str'
            for input in inputs:
                
                ID_in = super().Port_gen(type = 'input', port = input )
                # ID_in = super().Port_gen(type = 'input', name = input['name'], unit = input['unit'], datatype = input['datatype'] )
                self.inputs_dt.append(input['datatype'])
                self.inputs_unit.append(input['unit'])
                self.inID.append(ID_in)
        elif type(inputs) == dict:
            for input_name, input_value in inputs.items():

                ID_in = super().Port_gen(type = 'input', port =inputs[input_name] )
                # ID_in = super().Port_gen(type = 'input', name = inputs[input_name]['name'], unit = inputs[input_name]['unit'], datatype = inputs[input_name]['datatype'] )
                self.inputs_dt.append(inputs[input_name]['datatype'])
                self.inputs_unit.append(inputs[input_name]['unit'])
                self.inID.append(ID_in)
        else:
            print('Error, only acceptable types are dictionaries or list for defining all inputs')
        
        #generation of dictionary for a complex port.
        
        complex_components = self.Complex_data_agg(self.var_names)
        complex_datatype = self.Complex_data_agg(self.inputs_dt)
        complex_units = self.Complex_data_agg(self.inputs_unit)      
        complex_values = self.Complex_data_agg([])   
        # print(complex_values)    
        ouput_dict = {'name': output_name, 'components' : complex_components, 'unit':complex_units, 'datatype': complex_datatype, 'val':complex_values }
        
        self.outID = super().Port_gen(type = 'output', port = ouput_dict)
    
    def Complex_data_agg(self, data_list:List = []):
        comp_id = ['c' + str(i) for i in range(1,len(self.var_names)+1)]
        if data_list == []:
            complex_dict =dict.fromkeys(comp_id,'')
        else:
            complex_dict = {comp_id[i]:data_list[i] for i in range(len(comp_id))}
        
        return complex_dict
          
    def behavior(self):
        name_list = [name for  name,val in self.outputs[self.outID]['value'].items()]
        i = 0
        for input_ID in self.inID:
            name = name_list[i]
            self.outputs[self.outID]['value'][name] = self.inputs[input_ID]['value']
            i +=1
        # for in_name, val  in self.inputs.items():
        #     print(val)
        #     self.outputs[self.outID]['value'][val['name']] = val['value']
            

class Splitter(Component):
    def __init__(self, name="Splitter", ID="spl1", input:dict = {'name':"temp", 'components':{'c1':'Temp_air','c2':'Temp_beer'},'unit':{'c1':"K",'c2':'K'}, 'datatype':{'c1':"str",'c2':'float'},'val':{'c1':2,'c2':90}}) -> None:

        super().__init__(name, ID)
        self.name = name + str(self.uniqueNum)
        self.type = 'spl'
        #the data type has to always be a dictionary in the output
        self.inID= ''
        self.outID = []
        
        if type(input) == list:
            print(f'Input should be defined as dictionary e.g. ') 

        elif type(input) == dict:
            # items = tuple(input.items())
            # print(items)
            self.var_names = [input['components'].values()]
            self.inputs_dt = [input['datatype'].values()]
            self.inputs_unit = [input['unit'].values()]
        
        self.split_def(input)
         
    def split_def(self,input):
        
        self.inID = super().Port_gen(type = 'input', port = input)
        # input_data = input[self.inID]
        for comp,name in input['components'].items():
            unit = input['unit'][comp]
            datatype = input['datatype'][comp]
            val = input['val'][comp]
            #def a port simple: portdict = {'name':"temp", 'unit':"celcius", 'datatype':"float",'val':'125'}
            output = {'name':name,'unit': unit,  "datatype" :datatype,'val':val}
            outID = super().Port_gen(type = 'output', port = output)
            self.outID.append(outID)
                
    def behavior(self):
        name_list = [name for  name,val in self.inputs[self.inID]['value'].items()]
        i = 0
        for out_ID in self.outID:
            name = name_list[i]
            self.outputs[out_ID]['value'] =self.inputs[self.inID]['value'][name] 
            i +=1

class Switch(Component):
    #types of definitions of inputs and outputs 
    
    # input:dict = {'name': 'input', 'unit' : 'K', 'datatype':'str','val':''}
    # input1 = {'name':"temp", 'components':{'c1':'Temp_air','c2':'Temp_beer'},
    # 'unit':{'c1':"K",'c2':'K'}, 'datatype':{'c1':'str','c2':'str'},'val':{'c1':'','c2':''}}
    def __init__(self, name="Switch1", ID="swi0", 
                 output_def:str = {'name': 'input', 'unit' : 'K', 'datatype':'str','val':''},
                 inputs:list =[], 
                #  triggers:dict = {}, 
                 unit_trans_expr:dict = {}) -> None:
        super().__init__(name, ID)
        self.type = 'swi'
        self.name = name + str(self.uniqueNum)
        self.triggers = {}
        self.out_ID = ''
        self.in_IDs=[]
        self.switch_def(output_def=output_def,inputs = inputs)

    
    def switch_def(self,output_def: str = 'Temperature', inputs: dict = {}):
        '''
        Generate all the inputs, outputs, inports and outports and correlate the triggers with the inputs by ID
        also check that all the ports generated are consistent (have all the same number of components)
        '''
        ports = [output_def]
        for input in inputs:
            ports.append(input)
        inconsistencies = self.consistency_check(ports)
        if len(inconsistencies) == 0: 
            for input in inputs:
                ID_input = super().Port_gen(type = 'input',port = input)
                self.in_IDs.append(ID_input)
                #trasnform dictionary of triggers with inputs from name to IDs
                # input_trigger = triggers[input['name']]
                # self.triggers[ID_input] = input_trigger                        
            self.out_ID = super().Port_gen(type = 'output', port = output_def)
        else:
            text = 'Ports not defines inconsistencies in ports:\n'
            for inconsistency in inconsistencies:
                text = text + inconsistency + '\n'
            print(text)
    
    def add_triggers(self, triggers:dict = {}):
        for id,input in self.inports.items():
            
            in_name = input.name
            input_trigger = triggers[in_name]
            self.triggers[id] = input_trigger
            
    
    def consistency_check(self,ports:list=[]):    
        '''
        check weather the output definition has the same number of components as the inputs 
        and return all the inconsistencies
        '''
        
        inconsistency =[] 
        if 'components'  in list(ports[0].keys()):
            num_components = len(ports[0]['components'])
        else:
            num_components = 1
        
           
        for port in ports:
            if 'components' in list(port.keys()):
                comp_num = len(port['components'])
            else:
                comp_num = 1
            if num_components != comp_num:
                    inconsistency.append(port['name'])
        return inconsistency           
    
    def behavior(self):
        '''
        pass the value to the output of the corresponding input depending on the trigger
        it prioritise the triggers by input ID (i.e., lowest ID input number the higher the priority) in case
        both triggers are True
        '''
        trig_val = [False]*len(self.in_IDs)  
        index = 0
        for in_ID in self.in_IDs:
            
            #evaluate the event
            trig_active = self.triggers[in_ID].evaluation()
            if index == 0:
                output_value = self.inputs[in_ID]['value']
            
            index += 1
            
            if trig_active:
                output_value = self.inputs[in_ID]['value']
                
                break
        
        self.outputs[self.out_ID]['value'] = output_value
        
class Operation(Component):
    def __init__(self, name="Operator", ID="Op1",function: callable = []) -> None:
        super().__init__(name, ID)
        self.type ='op'
        
        
    def behavior(self):
        pass
        # still need some definition of behavior, what can you do.. based on the areas of execution?

class Transformation(Component):
   
    def __init__(self, name="Transformator", ID="Tr1",
                    outputs:list = [{'name': 'input', 'unit' : 'K', 'datatype':'str','val':''}],
                 inputs:list =[dict],
                 expressions: str = 'T=(T-32)*5/9', variables: dict = {}, dst_fmt:str = 'float') -> None:
        super().__init__(name, ID)
        self.name = name + str(self.uniqueNum)
        self.type ='tr'
        self.in_IDs =[]
        self.out_ID =[]
        self.expressions = expressions.split('\n')
        # self.var = {}
        self.dst_fmt = dst_fmt
        self.result = {'dummy' : 0}
        self.transformator_def(outputs = outputs, inputs = inputs)
        self.consistency_check()
        
    def transformator_def (self, outputs = [dict], inputs = [dict])-> None:
        """_summary_
            generate the definition and create of all ports, inputs and outputs and makes sure to create the necesary variables 
            dictionaries for the evaluation
        Args:
            output (str, optional): _description_. Defaults to 'outName'.
            inputs (dict, optional): _description_. Defaults to {}.
        """
                
        for input in inputs:
            ID_input = super().Port_gen(type = 'input',port = input)
            if input['val'] == '':
                input['val'] = 0
            # self.var[input['name']] = self.src_fmt(input['val'])
            self.in_IDs.append(ID_input)
                #trasnform dictionary of triggers with inputs from name to IDs
                # input_trigger = triggers[input['name']]
                # self.triggers[ID_input] = input_trigger                        
        for output in outputs:
            ID_output = super().Port_gen(type = 'output', port = output)
            self.out_ID.append(ID_output)
        
    def consistency_check(self)-> bool:
        """_summary_
            check weather the names in the inputs and output correspond to the variable names of
            the expressions. 
        Args:
            output (dict, optional): _description_. Defaults to {}.
            inputs (list, optional): _description_. Defaults to [dict].
            expression (str, optional): _description_. Defaults to ''.

        Returns:
            bool: _description_
        """
        intOutputs = []
        varNames = []
        outputsCorrect = True
        inputsCorrect = True
        outNames = []
        inNames = []
        for Id, output in self.outputs.items():
            outNames.append(output['name'])
        for Id, input in self.inputs.items():
            inNames.append(input['name'])
        for e in self.expressions:
            sepExp = e.split("=")
            intOutputs.append(sepExp[0].strip())
            vNames = re.findall("\w+",sepExp[1])
            for name in vNames:
                if name.isnumeric() == False:
                    varNames.append(name)
        # outputName = intOutputs[-1]
        # print(intOutputs)
        # print(varNames)
        # print(inNames)
        # print(outNames)
        for outName in outNames:
            if outName not in intOutputs:
                print('For transformator' + self.name +" the " +outName + ' is not define in the equations')
                return False
            else:
                print(f' For transformator {self.name}, all outputs define in the equations are correct')
        for varName in varNames:
            if varName not in inNames and varName not in intOutputs:
                print(varName + ' is in the equations but not value will be assigned')
                return False
        print(f'For transformator {self.name}, all variables within the equations are correctly defined')
                
        
        
        return outputsCorrect & inputsCorrect
            
        # if outputName != output['name']:
        #      outputCorrect = False
        
    def behavior(self, inputsFromConn = ['all'],outputsToConn = ['all'])-> None:
        """_summary_
        Computes the behavior of the component, by evaluating a set of expression, that must be
        sequencially defined and giving the result as the last value of the evaluation.
        """
        # expList = self.expressions.split('\n')
        assignedVals={}
        #get the data from the connector
        if inputsFromConn == ["all"] :
            inputsFromConn = self.inputsNames
        
        if outputsToConn == ["all"]:
            outputsToConn = self.outputsNames
        
        # if len(inputsFromConn) != 0 and ExeMode == 'Live':
        if len(inputsFromConn) != 0:
            self.inport_assigment (inputsFromConn)
            print('pulling data from connector')
        # self.inport_assigment()
        #get the value from the ports into the inputs
        self.input_update()
        
        
        
        for id, input in self.inputs.items():
            if input['value'] == '':
                input['value'] = 0
            assignedVals[input['name']] = self.src_fmt(input['value'])
        print(assignedVals)
        # assignedVals = self.var
        for e in self.expressions:
            assignedVals.update(self.evaluateExpression(e,assignedVals))
            # assignedVals = self.evaluateExpression(e,assignedVals)
            # print(assignedVals)
        # print(assignedVals)
        self.result = assignedVals
        
        #output operation for components
        outputsDict = {}
        for iD,output in self.outputs.items():
            name = output['name']
        #    self.outputs[iD]['value'] = assignedVals[name]
            outputsDict[name] = assignedVals[name]
        # return assignedVals
        print(outputsDict)
        # copy the output values into the outport
        self.output_update(outputsDict)
        #send the data to the connector
        self.outport_assigment(outputsToConn)
        
    def evaluateExpression(self,expression:str = 'Tc=(Tf-32)*5/9',assigned:dict = {'Tf':100}) -> any:
        tempval ={}
        sepExp = expression.split('=')
        # print(expression)
        # print(value)
        tempval[sepExp[0].strip()] = eval(sepExp[1],assigned)
        # print(tempval)
        return tempval
    
    def src_fmt(self, value:any = '4')->float:
        """_summary_
            transform all source values into floats
        Args:
            value (any, optional): _description_. Defaults to '4'.

        Returns:
            float: _description_
        """
        return float(value)
        
    def dst_fmt_trans(self, dst_fmt:str = 'int', value:float = 0.0)->any:
        """_summary_
            transform all values to the necessary format of the destination
        Args:
            dst_fmt (str, optional): _description_. Defaults to 'float'.
            value (float, optional): _description_. Defaults to 4.0.

        Returns:
            any: _description_
        """
        if dst_fmt == 'str':
            # print('trans to str= ' + str(value))
            return str(value)
        if dst_fmt == 'float':
            return value
        if dst_fmt == 'int':
            return int(value)
        if dst_fmt == 'bool':
            return bool(value)
    
class Connector:
    
    keys:list = ['name', 'unit' , 'datatype', 'val', 'components']
    
    def __init__(self, src:dict = {'component':object, 'output_name':'output1_Mod1'}, 
                 dst:dict = {'component':"Mod2", 'input_name':'input1_Mod2'},
                 exchange_pattern:dict = {'type': 'FIFO','PQ_conds':[]},
                 trans_expr:str = 'T=(T-32)*5/9') -> None:
        self.type = 'conn'
        self.src = src
        self.dst = dst
        self.src_port = self.find_port(component = self.src['component'],port_name = self.src['output_name'],type = 'output')
        self.dst_port = self.find_port(component = self.dst['component'],port_name = self.dst['input_name'],type = 'input')

        self.names = {'src':'','dst':''}
        self.components = {}
        self.units = {'src':'','dst':''}
        self.datatypes = {'src':'','dst':''}
        
        
        self.data_extraction()
        
        if 'PQ_conds' not in list(exchange_pattern.keys()):
            exchange_pattern['PQ_conds'] = []
            
        self.Pattern = Ex_Pattern(type = exchange_pattern['type'] , priority_guards=exchange_pattern['PQ_conds'])
        self.TransExpr = trans_expr
        
        
        self.relations = self.def_relations(self.names,self.components,self.TransExpr)
        # print(self.relations)
        self.con2ports()
    
    
    
    def find_port(self, component:object = [], port_name:str = 'Tempo',type:str = 'output'):
        port = ""
        if type == 'output':
            for id, properties  in component.outputs.items():
                if port_name == properties['name']:
                    port = component.outports[id]
        elif type == 'input':
            for id, properties  in component.inputs.items():
                if port_name == properties['name']:
                    port = component.inports[id]
        return port           
     
    def exchState(self,value = True, action = 'read')->None:
        """modify or reads the port state for exchange data in the port object. 
        Modification only works for outports, inports state should always be true

        Args:
            value (bool, optional): _description_. Defaults to True.
            action (str, optional): _description_. Defaults to 'read'.
        """
        # action = 'read'
        # action = 'modify'
        if action == 'modify':
            self.src_port.exchReady = value
            print(f'Modification of outport {self.src.name} has been performed to {value}')
       
        elif action == 'read':
            outportExch = self.src_port.exchReady
            inportExch = self.dst_port.exchReady
            print(f'Output {self.src_port.name} exchange state: {outportExch}')
            print(f'Input {self.dst_port.name} exchange state: {inportExch}')
       
        else:
            print(f'Action {action} is not supported, it is assume you want to read the data')
            outportExch = self.src_port.exchReady
            inportExch = self.dst_port.exchReady
            print(f'Output {self.src_port.name} exchange state: {outportExch}')
            print(f'Input {self.dst_port.name} exchange state: {inportExch}')
        
            
    def data_extraction(self ):
        
        src_port = self.src_port
        dst_port = self.dst_port
        # print(src_port)

        # print(dst_port)
        self.components['src'] = src_port.components
        self.components['dst'] = dst_port.components
        # self.components['src'] = 1
        # self.components['dst'] = 1
        self.names['src'] = src_port.name
        self.units['src'] = src_port.unit
        self.datatypes['src'] = src_port.datatype
        # self.values['src'] = src_port.val
        self.names['dst'] = dst_port.name
        self.units['dst'] = dst_port.unit
        self.datatypes['dst'] = dst_port.datatype
        
    
    def def_relations(self,names:dict = {},components:dict= {},expr:str = ''): 
        relations = []
        # print(components['dst'])
        if components['dst'] == 1:
            relation = names['src'],names['dst']
            relations.append(relation)
            # return relations
        else:
            expr_comps = expr.split(';')
            for ex_comp in expr_comps:
                variables = ex_comp.split('=')
                for comp,name in components['src'].items():
                    # print(name)
                    # print(variables[1])
                    if variables[1].rfind(name) != -1:
                        src_comp = comp

                        # print(src_comp)
                        break
                for comp,name in components['dst'].items():
                    # print(name)
                    # print(variables[0])
                    if variables[0].rfind(name) != -1:
                        dst_comp = comp
                        break
                relation = src_comp,dst_comp
                relations.append(relation)
        return relations
    
    def CData_relation(self, src_name:str = 'Temp_air',dst_name:str = 'Temp_amb'):
        for comp, name in self.components['src'].items():
            if name == src_name:
                src_comp = comp
                break
        for comp, name in self.components['dst'].items():
            if name == dst_name:
                dst_comp = comp
                break
        return (src_comp,dst_comp)
        
        
    def consistency_check(self)->bool:
        
        if self.components['dst'] != 1 and len(self.components['dst']) <= len(self.components['src']) :
            rel_len = len(self.relations)
            comp_len = len(self.components['dst'])
            src_rel = [src for src,dst in self.relations]
            if rel_len < comp_len:
                src_rel = [src for src,dst in self.relations]
                print(src_rel)
                dst_rel = [dst for src,dst in self.relations]
                print(dst_rel)
                src_noRel = [name for key,name in self.components['src'].items() if key not in src_rel]
                print(src_noRel)
                dst_noRel = [name for key,name in self.components['dst'].items() if key not in dst_rel]
                print(dst_noRel)
            index = 0
            for dst in dst_noRel:
                relation = self.CData_relation(src_name = src_noRel[index],dst_name = dst)
                self.relations.append(relation)
                index += 1
        
    def pull_src(self):
        '''
        Send the value of the outport(source port) to the queue of the connector
        '''
        
        temp_val = self.src_port.val
        
        dst_comp = {}
        exprs_dict ={}
        # var_dict = {}
        # variables =[]
        if self.components['src'] == 1:
            var_dict = {}
            # vars_name = 
            # vars_value =             
            var_dict[self.names['src']] = temp_val
            dst_comp[self.names['dst']] = var_dict
            # variables.append(var_dict)
            expr = self.TransExpr.split('=')
            # D_trandform = Data_Transformation(expression = expr[1],variables = var_dict,dst_fmt=self.datatypes['dst'])
            # queue_val = D_trandform.result
            queue_val = temp_val
        else:
            token = {}
            for rel in self.relations:
                var_dict = {}
              
                var_dict[self.components['src'][rel[0]]] = temp_val[rel[0]]
                dst_comp[rel[1]] = var_dict
            expressions = self.TransExpr.split(';')
            for c,name in self.components['dst'].items():
                # print(expressions)
                for expr in expressions:
                    # print(expr)
                    list_expr = expr.split('=')
                    # print(list_expr)
                    # print(list_expr[0].strip())
                    if name == list_expr[0].strip():
                        exprs_dict[c] = list_expr[1]
                d_transform = Data_Transformation(expression=exprs_dict[c],variables = dst_comp[c],dst_fmt=self.datatypes['dst'][c])
                # print(d_transform.result)
                token[c] = d_transform.result
            queue_val = token
            
        # print(queue_val)
        self.Pattern.push(queue_val)
        self.dst_port.queueState  = 'non-empty'
        if self.src_port.exchReady == True:
            self.Pattern.enableTransfer()
        

    def push_dst(self):
        '''
        get the value stored in the queue to later push it to the inport (destination port)
        '''
        queue_val = self.Pattern.pull()
        
        if self.Pattern.size() == 0:
            queue_state = 'empty'
        else:
            queue_state = "non-empty"
        # print(queue_val)
        # print(type(queue_val))
        if self.components ['dst'] == 1:
            # process to pass data to outport when the datatype is simple
            self.dst_port.val = queue_val
            
        else:
            # process to pass data when the data type is complex (i.e., many components)
            
            for c,val in queue_val.items():
                self.dst_port.val[c] = val 
                # print(c)
                # print(val)
        self.dst_port.queueState  = queue_state
        self.src_port.exchReady == False
 
    def con2ports(self):
        self.src_port.connector = self
        self.dst_port.connector = self
        
class Data_Transformation:
    def __init__(self,expression: str = '',variables: dict = {},dst_fmt:str = 'int') -> None:
        self.expression = expression
        self.invariables = variables
        self.var = {}
        self.dst_fmt = dst_fmt
        for name,val in self.invariables.items():
            self.var[name] = self.src_fmt(val)
        #     print(self.var[name])
        # print(self.var)
        print(self.var)
        print(self.expression)
        var_unit = self.unit_transformation(self.expression,self.var)
        # print(var_unit)
        
        self.result = self.dst_fmt_trans(self.dst_fmt,var_unit)
        # print(type(self.result))
    def src_fmt(self, value:any = '4')->float:
        
        return float(value)
        
    def dst_fmt_trans(self, dst_fmt:str = 'int', value:float = 4.0)->any:
        # print('format is ' + dst_fmt)
        # print('value is' + str(value))
        if dst_fmt == 'str':
            # print('trans to str= ' + str(value))
            return str(value)
        if dst_fmt == 'float':
            return value
        if dst_fmt == 'int':
            return int(value)
        if dst_fmt == 'bool':
            return bool(value)
    
    def unit_transformation(self,expression:str = 'x = y',value:dict = {"y":5}) -> any:
        expression_proc = expression.split('=')
        expression = expression_proc
        print(expression)
        print(value)
        result = eval(expression,value)
        return(result)


class Ex_Pattern:
    PATTERNS = ['FIFO', 'LIFO', 'PQ', 'LVQ', 'BPQ', 'BoC','LVoC']
    # LVQ = Last Value Queue
    # BPQ = Batch Processing Queue
    # PQ = Priority Queue

    def __init__(self, type='FIFO', priority_guards: list = []) -> None:
        # self.connector = connector
        self.type = type
        self.priority_guards = priority_guards
        self.piority_vals = [i for i in range(1, len(self.priority_guards) + 2)]
        self.prio_LP = 0
        self.batchData = []
        self.exchReady = True
        #possible states: active, inactive, waiting
        self.state = 'inactive'
        if type not in self.PATTERNS:
            print('Choose a valid pattern. Valid patterns: FIFO, LIFO, PQ (priority queue), LVQ (Last Value queue), BPQ (batch process Queue), BoC (Batch on Completion), LVoC (Last Value on Completion)')
        
        if self.type == 'FIFO':
            self.queue = queue.Queue()
        elif self.type == 'LIFO':
            self.queue = queue.LifoQueue()
        elif self.type == 'PQ':
            self.queue = queue.PriorityQueue()
        elif self.type == 'LVQ' or self.type == 'LVoC' or self.type == 'BPQ' or self.type == 'BoC':
            self.queue = queue.LifoQueue()
        else:
            self.queue = queue.Queue()

    def __str__(self) -> str:
        return f'Queue type {self.type} with size {self.size()}.'

    def size(self) -> int:
        return self.queue.qsize()

    def PQ_token_gen(self, token: any = 0, last_pos: int = 5) -> tuple:
        index = 0
        priority = self.piority_vals[-1]
        for guard in self.priority_guards:
            if guard.evaluation() == True:
                priority = self.piority_vals[index]
                break
            index += 1
        position = last_pos + 1
        return (priority, position, token)

    def push(self, token: any = 1) -> None:
        """push a message or token to the queue

        Args:
            token (any, optional): _description_. Defaults to 1.
        """
        if self.type == 'PQ':
            position = self.prio_LP
            token = self.PQ_token_gen(token, position)
            self.prio_LP = token[1]
            self.queue.put(token)
            self.state = 'active'
        elif self.type == 'LVQ':
            # self.batchData.append(token)
            if self.size() > 0:
                self.queue.get()
            self.queue.put(token)
            self.state = 'active'
        elif self.type == 'BPQ' :
            self.batchData.append(token)
            self.state = 'active'
        elif self.type == 'BoC'or self.type == 'LVoC': 
            # self.batchData.append(token)
            self.queue.put(token)
            logging.info(f' push value {token}')
            # logging.info('---------------this is the push of the LVoC queue+++++++++++')
            # logging.info(self.size())
            # logging.info(self.batchData)
            self.state = 'active'
        else:
            self.queue.put(token)
            self.state = 'active'

    def enableTransfer(self):
        if self.type == 'BoC':
            self.queue.put(self.batchData)
            self.batchData = []
            self.state = 'active'
        elif self.type == 'LVoC':
            # LV = self.batchData[-1]
            # self.batchData = []
            # self.queue.put(LV)
            self.state = 'active'
        else:
            pass

    def pull(self) -> any:
        if self.type == 'LVQ':
            # logging.info(f'size of queue {self.size()} for value ')
            val = self.queue.get()
            # logging.info(f' pull value {val}')
            self.queue.put(val)
            self.state = 'waiting'
        elif self.type == 'LVoC' or self.type == 'BoC':
            
            val = self.queue.get()
            logging.info(f' pull value {val}')
            self.state = 'active'
        elif self.type == 'PQ':
            val = self.queue.get()[2]
            self.state = 'active'
        elif self.type == 'BPQ':
            self.queue.put(self.batchData)
            self.batchData = []
            val = self.queue.get()
            self.state = 'active'
        # elif self.type == 'BPQ' or self.type == 'BoC':
        #     accumulated_data = []
        #     while not self.queue.empty():
        #         accumulated_data.append(self.queue.get())
        #     val = accumulated_data
        else:
            val = self.queue.get()
            self.state = 'active'
        
        return val



class OldEx_Pattern:
    PATTERNS = ['FIFO', 'LIFO' , 'PQ', 'LVQ','BPQ'] 
    # LVQ = Ladt Value queue
    # BPQ = Batch Processing Queue
    #  PQ = priority queue
    
    def __init__(self,type = 'FIFO', priority_guards:list = []) -> None:
        # self.connector = connector
        self.type = type
        self.priority_guards = priority_guards
        self.piority_vals = [i for i in range(1,len(self.priority_guards)+2)]
        self.prio_LP = 0
        self.batchData = []
        self.exchReady = True
        if type not in self.PATTERNS:
            print('choose a valid pattern. Valid patterns: FIFO, LIFO, PQ (priority queue), LVQ (Last Value queue), BPQ (batch process Queue), BoC (Batch on Completion),LVoC (Last Value on Completion)')
        
        if self.type == 'FIFO':
            self.queue = queue.Queue()
        elif self.type == 'LIFO':
            self.queue = queue.LifoQueue()
        elif self.type == 'PQ':
            self.queue = queue.PriorityQueue()
        elif self.type == 'LVQ' or self.type == 'LVoC':
            self.queue = collections.deque([])
        elif self.type == 'BPQ' or self.type == 'BoC':
            self.queue = collections.deque()
            
        else:
            self.queue = queue.Queue()
    
    def __str__(self) -> str:
        return f'Queue type {self.type} with size {self.size()}.'
          
    def lifo_eliminate(self):
        # queue.append(queue[0])
        # return queue.pop()
        self.queue.append(self.queue[0])
        return self.queue.pop()
    
    def size(self) -> int:
        if self.type != 'LVQ' and self.type !='BPQ' and self.type !='BoC' and self.type !='LVoC':
            return(self.queue.qsize())
        
        else:
            return(len(self.queue))
    
    def PQ_token_gen(self,token:any = 0, last_pos:int = 5)->tuple:
        index = 0
        priority = self.piority_vals[-1]
        for guard in self.priority_guards:
            if guard.evaluation() == True:
                priority = self.piority_vals[index]
                break
            index += 1    
        position = last_pos + 1
        return (priority,position,token)
         
    def push(self, token:any = 1) -> None:
        # q_size = self.size()
        if self.type == 'PQ':
            # if q_size == 0: 
            #     position = 0
            position = self.prio_LP
            token = self.PQ_token_gen(token,position)
            self.prio_LP = token[1]
            self.queue.put(token) 
        elif self.type =='LVQ':
            self.queue.append(token)
            if len(self.queue) > 1:
                self.queue.popleft()
        elif self.type == 'BPQ':
            self.queue.append(token) 
            self.batchData.append(token)
        elif self.type == 'BoC':
            # self.queue.append(token) 
            self.batchData.append(token)
        elif self.type == 'LVoC':
            # self.queue.append(token) 
            self.batchData.append(token)
        else:
            self.queue.put(token) 
    
    def enableTransfer(self):
        if self.type == 'BoC':
            self.queue.put(self.batchData)
            self.batchData = []
        elif self.type == 'LVoC':
            LV = self.batchData[-1]
            self.batchData = []
            self.queue.put(LV)
            pass
        else:
            pass
            
    
    def pull(self) -> any:
        if self.type == 'LVQ':
            val = self.lifo_eliminate()
        if self.type == 'LVoC':
            val = self.queue
        elif self.type == 'PQ':
            val = self.queue.get()[2]
        elif self.type == 'BPQ' or self.type == 'BoC':
            accumulated_data = list(self.queue)
            # accumulated_data = self.batchData
            # self.batchData = [] # reset the accumulated data
            self.queue.clear()
            val = accumulated_data
        else:
            val = self.queue.get()
        
        return val
               
    
    