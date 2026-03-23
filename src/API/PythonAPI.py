import inspect
import os
import csv
import importlib

class Wrapping:
    
    def __init__(self, model = object ,directory = os.getcwd(), 
                 modelName = 'UnitChange', typ = 'SimModel',
                 inputsNames = [], outputsNames = [],
                 exeSchedule = {}, printFlag = False ) -> None:
            
        self.model =  model
        self.typ = typ # two types SimModel or DataProc
        # self.parametersNames = self.get_params_names()
        self.directory = directory
        self.modelName =  modelName
        self.attributes = []
        self.methods = []
        class_data = self.extract()
        self.compIsValid = True
        self.exeSchedule = exeSchedule
        if self.typ == 'DataProc':
            if 'execute' in self.methods or 'processData' in self.methods:
                self.compIsValid =True
                if 'execute' in self.methods:
                    index = self.methods.index('execute')
                    self.exeDesign([self.methods[index]],[1])
                    # self.exeSchedule = {1:'execute'}
                    print("For type " + self.typ + ' the complete execution will be performed only by the method called: execute ')
                elif 'processData' in self.methods:
                    index = self.methods.index('processData')
                    self.exeDesign([self.methods[index]],[1])
                    # self.exeSchedule = {1:'processData'}
                    print("For type " + self.typ + ' the complete execution will be performed only by a method called: processData ')
            else:
                print('This component DataProcessing is not correctly created.It should have a method called either execute or processData, which will be the one used to execute this component')
            
        self.inputsNames = []
        self.outputsNames =   []
        self.parametersNames = self.get_params_names()
        self.parameters = {}
        self.inputs = {}
        self.outputs ={}
        if inputsNames != [] and outputsNames != []:
            self.portDefinition(inputs = inputsNames, outputs=outputsNames)
        else:
            print('define the inputs and outputs using the portDefinition method')
            
        # self.exeSchedule = exeSchedule
        
        self.initFlag = False
        if printFlag == True:
            print(class_data)
    
    def extract(self)-> dict:
        '''
        function that gets all the attributes and methods of a model built in python
        '''
        #self.attributes=[]
        att_dict = self.model.__dict__
        for att  in att_dict.keys():
            self.attributes.append(att)
        
        
        #method_list = [method for method in dir(self.model) if method.startswith('__') is False and method not in self.attributes ]
        #print(method_list)
        all_methods = dir(self.model)
        for method in all_methods:
            if method.startswith('__') or method in self.attributes:
                pass
            else:
                self.methods.append(method)
        class_data = dict(ports = self.attributes, methods = self.methods)
        print('Data of the class has been extracted')
        return class_data
    
    def portDefinition(self,inputs = [], outputs =[])->None:
        """_summary_
        this method defines all the inputs and outputs that a model build in python has
        if the inputs of the methods has empty list, this method inspects the model and automatically returns
        and populates the inputs and outputs names. But the user can mannually puts the names of the inputs and outputs
        to populte the object atteibutes inputs and outputs.

        Args:
            inputs (list, optional): _description_. Defaults to [].
            outputs (list, optional): _description_. Defaults to [].

        Returns:
            _type_: _description_
        """
        
        port_list = [attr for attr in self.attributes if attr not in self.outputs]
        self.inputsNames = inputs
        self.outputsNames = outputs

        if inputs == []:
            message =  'Define the inputs of this class from the list: {}\n'.format(port_list)
            self.inputsNames = input(message)
        
        if outputs == []:
            port_list = [attr for attr in self.attributes if attr not in self.inputs]
            message =  'Define the outputs of this class from the list: {}\n'.format(port_list)
            self.outputsNames = input(message)
        portdata = dict(inputs = self.inputsNames,outputs = self.outputsNames)
        print("Inputs and outputs have been defined for this model")
        for name in self.inputsNames:
            self.inputs[name] = 0
            
        for name in self.outputsNames:
            self.outputs[name] = 0
        return None
    
    def exeDesign(self, methodsNames=[], order = []) -> bool:
        
        """_summary_
            This method enables the definition of the methods execution to define how to use this model
            user must define the order of function calling. 
        Args:
            methodsNames (_type_): _description_

        Returns:
            str: _description_
        """
        idx = 0
        # print(len(methodsNames))
        # print(len(order))
        if len(methodsNames) != len(order):
            print('the number of elements of the list names of the methods and the set defining their order should be the same')
            return False
        else:
            temp_dict = {} 
            for o in order:
                
                temp_dict[o] = methodsNames[idx]
                

                idx += 1
            self.exeSchedule = dict(sorted(temp_dict.items()))
            return True
    
    def get_params_names(self):    
        
        if self.model.param == {}:
            print("no parameters")
            parameters = {}
        else:
            parameters = list(self.model.param.keys())
        
        return parameters
    
    def __str__(self) -> str:
            msg_model = "this class encapsulate a model name with s-function as interface" + self.modelName + '_wI'
            msg_director= 'This model is contain in directory:' + self.directory
            msg_input = 'The inputs of this model are: ' + self.inputs 
            msg_output =  'The outputs of this model are: ' + self.outputs
            return msg_model + '\n' + msg_director + '\n' + msg_input + '\n' + msg_output
            
    def initialize_model(self,ini_val={})-> None:
            """_summary_
            initialize the model just by defining the inputs 
            Args:
                ini_val (dict, optional): _description_. Defaults to {}.
            """
            # oD ={}
            # self.set_input('temp_in',0)
            if self.typ != 'DataProc':
                temp_dict = {}
                for input in self.inputs:
                    if ini_val == {}:
                        # print(input)
                        self.set_input(input,0)
                        temp_dict[input]=0
                    else:
                        self.set_input(input,ini_val[input])
                        temp_dict[input]=ini_val[input]
                print('Model {} has been initiated with the input values: \n {}'.format(self.modelName, temp_dict))
            
                outputDict = self.advance()
                # for outName,outputDict  in self.outputs:
                #     oD[outputDict['name']] = outputDict['value']
                print('Model {} current output values: \n {}'.format(self.modelName, outputDict))
                self.initFlag = True
            else:
                print('Data Processing does not need to be initialized, it will recieve its first input from sources')
            
            
    def advance(self, inputs_val = {})-> dict:
            """_summary_
            
            Method advance 1 step of the mode, stoping it instantly
            """
            for order,method in self.exeSchedule.items():
                func = getattr(self.model, method)
                func()
        # return("All function have been executed in the order define in the list ")
            output_vals = {}
            for output in self.outputs:
                output_vals[output] = self.get_output(output)
            return output_vals
        
    def simulate(self,sim_inputs = {}):
        """in the case of sim models of python classes the advace and simulate are the same implemetation
        """
        self.advance(inputs_val=sim_inputs)
    
    def execution(self)-> None:
        """_summary_
        
        Method advance 1 step of the mode, stoping it instantly
        """
        for order,method in self.exeSchedule.items():
            func = getattr(self.model, method)
            func()
        # return("All function have been executed in the order define in the list ")
        output_vals = {}
        for output in self.outputs:
            output_vals[output] = self.get_output(output)
        return output_vals
        
    def set_input(self, var_name, var_val):
            name = str(var_name)
            self.inputs[name] = var_val
            # getattr(self.model,name) = self.inputs[name]
            self.model.__setattr__(var_name,self.inputs[name])
            # input = self.inputs[name]
            # 

    def get_output(self, var_name)->any:
            name = str(var_name)
            # output_val = self.model.__getattribute__(var_name)   
            self.outputs[name] = self.model.__getattribute__(var_name)   
            return self.outputs[name]
        
    def pause(self):
            print("no need for pause")
    
    def resume(self):
            for order,method in self.exeSchedule.item():
                func = getattr(self.model, method)
                func()
    
    def stop(self):
           print("no need for stop")
   
    def set_config(self, configIdName = 't_ini', configIdVal = 0, startConfig = False )->bool:
            """_summary_
                this method re-configure a simulation, but it only supports
                time configuration IdNames such as t_ini, t_period and t_step
            Args:
                configIdName (str, optional): _description_. Defaults to 't_ini'.
                configIdVal (int, optional): _description_. Defaults to 0.
            """
            if startConfig == False:
                print(" this model is configure for first time")
            
            if configIdName == 't_ini':
            
                print ("initial time is : " + str(configIdVal))
                return True
            elif configIdName == 't_period':
                
                print ("Stop time  is: " + str(configIdVal))
                return True
            elif configIdName == 't_step':
                
                print ("step time  is: " + str(configIdVal))
                return True
            else:
                print('only three possible time configurations: t_ini, t_peior and t_step, please change')
                return False
            
    def set_parameter(self,name ="u", value=1):
        '''
        this set the value of a parameter by its name and a desire value
        only works when the block in matlab has the same name as the name set in this function and the block is a constant

        '''
        param_names = self.parametersNames
        if name not in param_names:
            print(f'Name: {name} does not match the parameters allow in model {self.modelName}')
            return 0
        else:
            self.parameters[name] = value
            self.model.param[name] =value
    
    def save_to_csv(self, file_name):
        """Save class data to a CSV file in the specified directory."""
        # Ensure the file has a .csv extension
        if not file_name.endswith('.csv'):
            file_name += '.csv'
        
        # Full path to save the file
        file_path = os.path.join(self.directory, file_name)
        
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write headers
            writer.writerow(['Field', 'Value'])
            # Write data
            writer.writerow(['inputsNames', ','.join(self.inputsNames)])
            writer.writerow(['outputsNames', ','.join(self.outputsNames)])
            writer.writerow(['parametersNames', ','.join(self.parametersNames)])
            writer.writerow(['exeSchedule', ','.join(f"{k}:{v}" for k, v in self.exeSchedule.items())])
            writer.writerow(['modelName', self.modelName])
            writer.writerow(['type', self.typ])
            writer.writerow(['model', self.model.__class__.__module__ + '.' + self.model.__class__.__name__])

    @classmethod
    def load_from_csv(cls, name, directory):
        """Load data from a CSV file in the specified directory and create an instance of pythonEncap."""
        file_name = name + '.csv'
        file_path = os.path.join(directory, file_name)

        data = {}
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                key, value = row
                if key == 'inputsNames' or key == 'outputsNames' or key == 'parametersNames':
                    data[key] = value.split(',')
                elif key == 'exeSchedule':
                    data[key] = {int(k): v for k, v in (item.split(':') for item in value.split(','))}
                elif key == 'model':
                    # Use the model factory to recreate the model
                    data[key] = cls.model_factory(value)
                else:
                    data[key] = value

        # Create and return an instance of pythonEncap
        return cls(
            model=data['model'],
            modelName=data['modelName'],
            typ = data['type'],
            inputsNames=data['inputsNames'],
            outputsNames=data['outputsNames'],
            # parametersNames = data['parametersNames'],
            exeSchedule=data['exeSchedule'],
            directory=directory
        )
        
    
    @staticmethod
    def model_factory(model_name):
        """Factory method to recreate a model object by its class name."""
        module_name, class_name = model_name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        model_class = getattr(module, class_name)
        return model_class()
    
    