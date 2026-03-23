#pyhton_class_inspector
import inspect
import os

class Model_wrapper:
    def __init__(self, model = object ,directory = os.getcwd(), modelName = 'unit_change') -> None:
        self.model =  model
        self.directory = directory
        self.modelName =  modelName
        self.attributes = []
        self.methods = []
        self.inputs = []
        self.outputs = []   
    
    def extract(self)-> dict:
        '''
        function that gets all the attributes and methods of a class in python
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
    
    def portDefinition(self,inputs = [], outputs =[]):
        port_list = [attr for attr in self.attributes if attr not in self.outputs]
        self.inputs = inputs
        self.outputs = outputs

        if inputs == []:
            message =  'Define the inputs of this class from the list: {}\n'.format(port_list)
            self.inputs = input(message)
        
        if outputs == []:
            port_list = [attr for attr in self.attributes if attr not in self.inputs]
            message =  'Define the outputs of this class from the list: {}\n'.format(port_list)
            self.outputs = input(message)
        portdata = dict(inputs = self.inputs,outputs = self.outputs)
        print("Inputs and outputs have been defined for this model")
        return portdata
    
    def set_input(self, var_name, var_val):
    
        self.model.__setattr__(var_name,var_val)

    def get_output(self, var_name)->any:

        return self.model.__getattribute__(var_name)    
    
    def pause(self):
        print("No pause needed")
    def resume(self):
        #print("methods call")
        self.model.step_increase()
        self.model.unit_transform()
        
        
    def stop(self):
        print("no stop necessary")

    def get_status(self):
        print("On-going")
        