#Global_objects
from typing import List
import sched, time
import os
import datetime
import typing
from math import*
import src.Comm
import time,threading
import re
import random

class AppTime:
    def __init__(self) -> None:
        self.startTime = time.time()
        self.timePass = 0
    
    def re_startApp(self)->None:
        prevInitialtime = time.asctime(time.localtime(self.startTime) )
        self.startTime = time.time()
        newInitialtime = time.asctime(time.localtime(self.startTime) )
        print(f" Time has been re-started, new initial time is {newInitialtime}")
        print(f" Previous initial time was {prevInitialtime}")
    
    def __str__(self) -> str:
        initialtime = time.asctime(time.localtime(self.startTime) )
        return (f"The starting moment of the application is {initialtime}")
        
    def app_update(self):
        currenttime = time.time()
        self.timePass = currenttime - self.startTime 
        return self.timePass
    
    def local_update(self, clock:any = {'year':2024,'month':2,'day':26,'hr':15,'min':17,'s':0})->float:
        if type(clock) == dict: 
            comparing_time= dictToTime(clock)
        elif type(clock) == float:
            comparing_time = clock
        currenttime = time.time()
        return currenttime - comparing_time
    
def dictToTime(time_input:dict = {'year':2024,'month':2,'day':26,'hr':15,'min':17,'s':0} )->float:
    clocklist = [0]*6
    pos_dict = {'0':'year','1':'month','2':'day', '3':'hr','4':'min','5':'s'}
    
    for i in range(len(clocklist)):
        clocklist[i] = time_input[pos_dict[str(i)]]
    
    # clock_tuple = tuple(clocklist)
    # print(tuple(clocklist))
    # print(clocklist)
    clock_T = tuple(clocklist)
    clock_tuple = datetime.datetime(*clock_T)
    clock_sec= time.mktime(clock_tuple.timetuple())
    
    return clock_sec

class GlobalVars:
    def __init__(self,appTime = None):
        if appTime ==None:
            defaultAppTime = AppTime()
            
            self.startTime = defaultAppTime.startTime   
        else:
            self.startTime = appTime.startTime
        self.stopApp = False
        self.name = 'globals'
    
    def add_attribute(self, name, value):
        setattr(self, name, value)
    
    def list_attributes(self): 
        return [attr for attr in self.__dict__.keys()]
    
    def add_appTime(self,appTime = AppTime())->None:
        new_startTime = appTime.startTime
        self.startTime = new_startTime
        
    def get_attribute_value(self, attr_name): 
        return getattr(self, attr_name, None)
   
         
class Watchdog(threading.Thread):
    def __init__(self, interval=1, condition =[{'type': "time", 'value': 5, 'unit':'s',"action":'stop'}]):
        super().__init__()
        self.interval = interval #in seconds
        self.running = False
        self.condition = condition

    def run(self):
        self.running = True
        while self.running:
            self.watch()
            time.sleep(self.interval)

    def watch(self):
        # Replace this with the condition you want to watch
        print("Watchdog is running...")

    def start(self):
        self.running = True
    
    def stop(self):
        self.running = False            

class Trigger:
    # trigger = {'type':'start', 'class':'guard','definition':'MassSpringMod.DisplacementOutput > 10'}
        # trigger = {'type':'start', 'class':'temporal','definition':{'type':'freq','value': 1,'unit':'s'}}
        # trigger = {'type':'start', 'class':'temporal','definition':{'type':'time','value': 5,'unit':'s'}}
        # trigger = {'type':'start', 'class':'data','definition':'MassSpringMod.DisplacementOutput'}
        # trigger = {'type':'stop', 'class':'guard','definition':'globals.stopApp == True'}
    
    
    def __init__(self,name = 'trigger_area51',typ = 'start', category = 'temporal', 
                 definition = {'type':'freq','value': 1,'unit':'s'}, appTime = None , allComponents=[]):
        
        self.appComponents = []
        self.name = name + str(random.randint(1,1000))
        self.typ = typ
        self.category = category
        self.definition = definition
        self.appTime = appTime
        if appTime == None:
            print('*******************************************************************')
            print("DONT FORGET TO INCLUDE MANUALLY THE UNIQUE OBJECT OF THE APPLICATION CLOCK AND RE-RUN OBJ_GEN")
            print('******************************************************************')
        self.allComponents = allComponents
        if allComponents == [] and self.category != 'temporal':
            print('*******************************************************************')
            print("DONT FORGET TO INCLUDE MANUALLY ALL THE COMPONENTS AND RERUN THE OBJ_GEN")
            print('******************************************************************')
        if definition == {} or definition == '':
            print('ErrorDefinition: the defintion is empty for trigger ' + self.name)
            return False
        self.consistencyFlag = self.consistencyCheck(category=self.category,definition=self.definition)
        if self.consistencyFlag == True:
            if self.category == 'temporal':
                self.flagObject = TimeFlag(definition = self.definition,appClock=self.appTime) 
            elif self.category == 'guard':
                self.flagObject = GuardFlag(expression=self.definition,allComponents=self.allComponents)
            elif self.category == 'data':
                self.flagObject = DataFlag(identifiers=self.definition,allComponents = self.allComponents)
            else:
                print('That category of trigger for '+ self.name + ' is not supported. Only: temporal, guard and data triggers are supported')
        else:
            print(f'For trigger {self.name} of category {self.category} the definition or type is not consistent. Follow previous messages')
    
    def consistencyCheck(self,category='temporal', definition = {})-> bool:
        """
        
        Args:
            category (str, optional): _description_. Defaults to 'temporal'.
            definition (dict, optional): _description_. Defaults to {}.

        Returns:
            bool: _description_
        """
        if category == 'temporal':
            if type(self.definition) == dict:
                # self.flagObject = TimeFlag(definition = self.definition,appClock=self.appTime) 
                return True
            else:
                print(f'The definition of the temporal trigger {self.name} is wrong, definition should be a dictionary')
                return False
        elif self.allComponents == []:
            self.flagObject = None
            print(f'No object for the trigger {self.name} was created, it can only be created when you introduce the component list')        
            print('Use the obj_gen method to create the object')
            return False
        elif category == 'guard':
            if type(definition) == list:
                for DefUnit in definition:
                    eqNum = 0
                    if self.is_math_equation(DefUnit):
                        # self.flagObject = GuardFlag(expression=self.definition,allComponents=self.allComponents)
                        eqNum +=1
                        print(f'Correct guard definition for trigger {self.name}, for equation num {eqNum}')
                    else:
                        print(f'The guard, from equation {eqNum} for trigger {self.name} must be define as a mathematical equation using, >,<, == or !=')
                        return False
                return True
            else:
                if self.is_math_equation(definition):
                    print(f'Correct guard definition for trigger {self.name}')
                    return True 
                else:
                    print(f'the guard for trigger {self.name} must be define as a mathematical equation using, >,<, == or !=')
                    return False
        elif category == 'data':
            return True
        else:
            print('That category of trigger for '+ self.name + ' is not supported. Only: temporal, guard and data triggers are supported')
        
    def obj_gen(self,components = [], appTime = None):
        """_summary_

        Args:
            components (list, optional): _description_. Defaults to [].
            appTime (_type_, optional): _description_. Defaults to None.
        """
        if components != [] and self.category != 'temporal':
            if self.category == 'guard':
                if self.is_math_equation(self.definition):
                    self.flagObject = GuardFlag(expression=self.definition,allComponents=components)
                else:
                    print('the guard must be define as a mathematical equation using, >,<, == or !=')
            elif self.category == 'data':
                self.flagObject = DataFlag(expression=self.definition,allComponents = components)
            else:
                print('That category of trigger for '+ self.name + ' is not supported. Only: temporal, guard and data triggers are supported')
       
        if appTime != None and self.category == 'temporal':
            if type(self.definition) == dict:
                self.flagObject = TimeFlag(definition = self.definition,appClock=appTime) 
            else:
                print('The definition of the trigger is wrong, it should be a dictionary')  
       
    def evaluate(self)->bool:
        return self.flagObject.evaluation()
    
    def is_math_equation(self,text):
        """
        Determines if a string is a mathematical equation containing comparison operators.
        
        Supported operators: >, <, =, >=, <=, !=
        Supports dotted identifiers (e.g., object.attribute).
        """
        # Updated regex pattern
        pattern = r'^\s*[\w\s\d\.\+\-\*/\(\)]+(?:[><=]=?|!=)[\w\s\d\.\+\-\*/\(\)]+\s*$'
        
        # Match the pattern to the input text
        return bool(re.match(pattern, text))
    
class TimeFlag:
    def __init__(self, definition = {'type':'freq','value': 1,'unit':'s'}, appClock = None ):
        
        self.typ = definition['type']
        self.value = definition['value']
        self.unit = definition['unit']
        self.time_sec = self.timeconverter(unit =self.unit,value=self.value) 
        self.appClock = appClock
        if self.appClock == None:
            self.init_time = time.time()
        else:
            self.init_time = self.appClock.startTime
        
        self.current_time = None
        self.passTime = 0
        self.executed = False
        
    def timeconverter(self, unit= 's', value = 1)->float:
        """_summary_

        Args:
            unit (str, optional): _description_. Defaults to 's'.
            value (int, optional): _description_. Defaults to 1.

        Returns:
            float: _description_
        """
        if unit == 's':
            return value
        elif unit == 'min':
            return value*60
        elif unit == 'hr':
            return value * 60*60
        else:
            print('Unit '+unit+' is not supported')
            return value
        
    def evaluation(self)->bool:
        self.current_time = time.time()
        self.pass_time = self.current_time-self.init_time
        compare_time = self.time_sec - self.pass_time
        if self.typ == 'freq':
            if compare_time <= 0:
                self.init_time += self.time_sec
                return True
            else:
                return False
        elif self.typ == 'time':
        # trigger = {'type':'start', 'class':'temporal','definition':{'type':'time','value': 5,'unit':'s'}}
            if compare_time <= 0 and self.executed == False:
                self.executed = True
                return True
            else:
                return False

class GuardFlag:
    def __init__(self,expression = 'MassSpringMod.DisplacementOutput > 10',
                 allComponents = []):
        self.expression = expression
        self.allComponents=  allComponents
        identifier = self.split_expression(expression=self.expression)
        
        elements = self.split_identifier(identifier=identifier[0])
        
        self.compName = elements[0]
        self.portName = elements[1]
        self.new_expression = self.substitute_identifier(self.expression,old_identifier=identifier[0],new_identifier=self.portName)
        self.obj = self.find_object(componentName=self.compName,portName=self.portName)
        
    def add_components(self, components = [])->None:
        if type(components) == list:
            self.allComponents += components
        else:
            self.allComponents.append(components)
    
    def split_expression(self, expression)->tuple:
        """
        Splits an expression into the left and right parts based on the comparison operator.

        Args:
            expression (str): The expression to split (e.g., 'MassSpringMod.DisplacementOutput > 10').

        Returns:
            tuple: A tuple containing the left part, operator, and the right part of the expression.
        """
        # Define a regex pattern to match comparison operators
        pattern = r'(.+?)\s*(>|<|>=|<=|==|!=)\s*(.+)'
        
        match = re.match(pattern, expression)
        if match:
            left_part = match.group(1).strip()
            operator = match.group(2).strip()
            right_part = match.group(3).strip()
            return left_part, operator, right_part
        else:
            raise ValueError("Invalid expression format")
    
    def split_identifier(self, identifier)->list:
        """
        Splits a dotted identifier into its components.

        Args:
            identifier (str): The dotted identifier (e.g., 'MassSpringMod.DisplacementOutput').

        Returns:
            list: A list of components (e.g., ['MassSpringMod', 'DisplacementOutput']).
        """
        return identifier.split('.')

    def substitute_identifier(self, expression, old_identifier, new_identifier)->str:
        """
        Substitutes an identifier in an expression with a new text.

        Args:
            expression (str): The original expression (e.g., 'MassSpringMod.DisplacementOutput > 10').
            old_identifier (str): The identifier to replace (e.g., 'MassSpringMod.DisplacementOutput').
            new_text (str): The new text to substitute (e.g., 'variable').

        Returns:
            str: The updated expression with the identifier replaced.
        """
        # Escape the old identifier to safely use it in a regex
        escaped_identifier = re.escape(old_identifier)
        # Substitute the old identifier with the new text
        updated_expression = re.sub(rf'\b{escaped_identifier}\b', new_identifier, expression)
        return updated_expression
    
    def find_object(self,componentName, portName)->object:
        components = self.allComponents
        exeComp = None
        val = 0
        is_Input = False
        is_Output = False
        
        
        for component in components:
            if component.name == componentName:
                exeComp = component
                break
        if type(exeComp) == GlobalVars:
            obj = exeComp
            # obj = exeComp.get_attribute_value(portName)
        else:
            #identified if it is input or output
            if portName in exeComp.inputsNames:
                is_Input = True
            elif portName in exeComp.outputsNames:
                is_Output = True
            else:
                print('errorType: the port name ' + portName + ' is not part of component' + componentName)
                return 0
            
            if is_Input == True:
                for ID, input in exeComp.inputs.items():
                    if input['name'] == portName:
                        obj = input
                        # obj = input['value']
                        break
            elif is_Output == True:
                for ID, output in exeComp.outputs.items():
                    if output['name'] == portName:
                        obj = output
                        # val = output['value']
                        break
        return obj
    
    def find_value(self,componentName, portName)->float:
        components = self.allComponents
        exeComp = None
        val = 0
        is_Input = False
        is_Output = False
        
        
        for component in components:
            if component.name == componentName:
                exeComp = component
                break
        if type(exeComp) == GlobalVars:
            val = exeComp.get_attribute_value(portName)
        else:
            #identified if it is input or output
            if portName in exeComp.inputsNames:
                is_Input = True
            elif portName in exeComp.outputsNames:
                is_Output = True
            else:
                print('errorType: the port name ' + portName + ' is not part of component' + componentName)
                return 0
            
            if is_Input == True:
                for ID, input in exeComp.inputs.items():
                    if input['name'] == portName:
                        val = input['value']
                        break
            elif is_Output == True:
                for ID, output in exeComp.outputs.items():
                    if output['name'] == portName:
                        val = output['value']
                        break
        return val
            
    def evaluate_expression(self,expression, variable_name,variable_value):
        """
        Evaluates a simple mathematical or logical expression with a single variable.

        Args:
            expression (str): The expression to evaluate (e.g., 'variable > 10').
            variable_value: The value of the variable in the expression.

        Returns:
            bool: The result of the evaluated expression.
        """
        # Replace the placeholder 'variable' with the actual value
        parsed_expression = expression.replace(variable_name, repr(variable_value))
        
        # Evaluate the parsed expression
        try:
            return eval(parsed_expression)
        except Exception as e:
            raise ValueError(f"Invalid expression or variable value: {e}")
    
    def evaluation(self)->bool:
        
        if type(self.obj) == GlobalVars:
            value = self.obj.get_attribute_value(self.portName)
        else:
            value = self.obj['value']
        # value = self.find_value(componentName=self.compName,portName=self.portName)
        flag = self.evaluate_expression(expression=self.new_expression,variable_name=self.portName,variable_value=value)
        return flag       
    
class DataFlag:
    def __init__(self,identifiers = 'MassSpringMod.DisplacementOutput',
                 allComponents = []):
        if type(identifiers) == list:
            self.identifiers = identifiers
            self.idenNum = len(self.identifiers)
        elif type(identifiers) == str:
            self.identifiers = [identifiers]
            self.idenNum = 1
        else:
            raise TypeError(f'Error defining the identifier, only a list of identifiers or a sinlgle indentifer as a string is accepted')
            
        # self.expression = expression
        self.allComponents=  allComponents
        # identifier = self.split_expression(expression=self.expression)
        self.objects = []
        self.compNames = []
        self.portNames = []
        self.Flags = {}
        for indentifier in self.identifiers:
            elements = self.split_identifier(identifier=indentifier)
            self.compNames.append(elements[0])
            self.portNames.append(elements[1])
        # self.new_expression = self.substitute_identifier(self.expression,old_identifier=identifier[0],new_identifier=self.portName)
            self.objects.append(self.find_object(componentName=elements[0],portName=elements[1]))
            self.Flags[elements[1]] = False
        
    def add_components(self, components = [])->None:
        if type(components) == list:
            self.allComponents += components
        else:
            self.allComponents.append(components)
    
    def split_identifier(self, identifier)->list:
        """
        Splits a dotted identifier into its components.

        Args:
            identifier (str): The dotted identifier (e.g., 'MassSpringMod.DisplacementOutput').

        Returns:
            list: A list of components (e.g., ['MassSpringMod', 'DisplacementOutput']).
        """
        return identifier.split('.')

    def find_object(self,componentName, portName)->object:
        components = self.allComponents
        exeComp = None
        val = 0
        is_Input = False
        is_Output = False
        
        
        for component in components:
            if component.name == componentName:
                exeComp = component
                break
        if type(exeComp) == GlobalVars:
            obj = exeComp
            # obj = exeComp.get_attribute_value(portName)
        else:
            #identified if it is input or output
            if portName in exeComp.inputsNames:
                is_Input = True
            elif portName in exeComp.outputsNames:
                is_Output = True
            else:
                print('errorType: the port name ' + portName + ' is not part of component' + componentName)
                return 0
            
            if is_Input == True:
                for ID, input in exeComp.inports.items():
                    if input.name == portName:
                        obj = input.connector.Pattern
                        # obj = input['value']
                        break
            elif is_Output == True:
                for ID, output in exeComp.outports.items():
                    if output.name == portName:
                        obj = output.connector.Pattern
                        # val = output['value']
                        break
        return obj
    
    def evaluation(self)->bool:
        # portNames = self.portNames
        idx = 0
        for obj in self.objects:
            if obj.state == 'active':
                value = True
            else:
                value = False
            
            self.Flags[self.portNames[idx]] = value
            idx += 1
            
        flag = all(value for value in self.Flags.values())     
        # value = self.find_value(componentName=self.compName,portName=self.portName)
        # flag = self.evaluate_expression(expression=self.new_expression,variable_name=self.portName,variable_value=value)
        return flag       
        


    
       
class Event:
    '''
    An event is always a combination of other types of events, a complex event can be a combination of higher level events
    '''
    def __init__(self, ID:str = 'ev_1',name:str = 'Time_and_data',expression:str = '', events:list = [] ) -> None:
        
        self.ev_type = 'event'
        self.ID = ID
        self.name = name
        self.events = events
        self.expression = expression
        self.eval = False
    
    def evaluation(self)->bool:
        variables = dict()
        
        for event in self.events:
            variables[event.name] = event.evaluation()
        self.eval = eval(self.expression,variables)
        return self.eval
        # return eval(self.expression,variables)
    
class DataEvent(Event):
    
    def __init__(self, ID: str = 'ev_1', name: str = 'Time_and_data', ports:list = [] ) -> None:
        if type(ports)!= list:
            ports = [ports]
        self.ports = ports
        super().__init__(ID, name)
        self.ev_type = 'data'
    
    def evaluation(self)->bool:
        inports = self.ports
        dataStates = []
        for port in inports:
            dataState = port.queueState 
            dataStates.append(dataState)
        self.eval = 'empty' not in dataStates
        return self.eval
        # return 'empty' not in dataStates

class GuardEvent(Event):
    
    def __init__(self, ID: str = 'ev_1', name: str = 'Time_and_data', 
                 expression: str = '',variables: dict = {},
                 var2comp:dict ={}) -> None:
        self.variables = variables
        self.expression = expression
        self.var2comp = var2comp
        self.mapc2var ={}
        # the variables dictionary must contain only ports objects or constant values
        super().__init__(ID, name,expression)
        self.ev_type = 'guard'
    
    def mapComp2Name(self):
        #example {Temp_beer:Temp_beer,Temp:Temp_air}
        name2c = {v: k for k, v in port.components.items()}
        for variable,port in self.variables.items():
            name2c = {v: k for k, v in port.components.items()}
            self.mapc2var[variable] = name2c[self.var2comp[variable]]        
                     
    def evaluation(self)->bool:
        var_dict = {}
        #extracting port objects values
        for key,value in self.variables.items():
            if isinstance(value,Comm.Port):
                if self.var2comp != {}:
                    self.mapComp2Name()
                    var_dict[key] = value.val[self.mapc2var[key]]    
                else:
                    var_dict[key] = value.val
                
            else:
                var_dict[key] = float(value)
        self.eval = eval(self.expression,var_dict)            
        return self.eval
        # return eval(self.expression,self.variables)
    
class TimeEvent(Event):
    
    TIME_TYPES = {'freq':'Frequence', 'RWC':'Real-world clock', 'RC':'Relative clock'}
    UNITS = {'freq': ['s','min','hr'], 'RWC': ['year','month','day', 'hr', 'min','s'], 'RC':['day', 'hr','min','s']}
    FORMAT = {'freq': ['freq','unit'], 'RWC': ['year','month','day', 'hr','min','s'], 'RC':['day','hr','min','s']}
    
    def __init__(self, ID: str = 'ev_1', name: str = 'Time_and_data', 
                 Ss_start:object = AppTime,type:str = 'freq', 
                 definition:dict = {'ref_start':{'year':2024,'month':2,'day':27,'hr':15,'min':14,'s':0},'freq':2,'unit':'min'} ) -> None:
        self.type = type
        self.definition = definition
        reqkeys = self.FORMAT[self.type]
        keys = list(definition.keys())
        # print(keys)
        for key in keys:
            if key not in reqkeys:
                # print('the key ' + key + 'is missing in the definition of the time event' )
                # self.__del__()
                break
        # self.ref_time = time.time()
        self.ref_time = time.time()
        self.ss_start = Ss_start
        
        super().__init__(ID, name)
        self.ev_type = 'time'
    
  
        
    def evaluation(self):
    # def evaluation(self, ref_time:object = time.time(), appTime:object = []):
        
        app_init = self.ss_start.startTime
        current_time =  time.time()
               
        if self.type == 'freq':
            # mult = 0
            ref_time = self.definition['ref_start']
            
            if type(ref_time) == dict:
                ref_time = dictToTime(ref_time)
            elif isinstance(ref_time, AppTime) == True:
                ref_time = ref_time.startTime
                
            original_ref = ref_time
            if self.definition['unit'] == 's':
                t_sec = self.definition['freq'] 
            elif self.definition['unit'] == 'min':
                t_sec = self.definition['freq'] *60
            elif self.definition['unit'] == 'hr':
                t_sec = self.definition['freq']*60*60
            else:
                print('error in recognising units')
            if self.eval == True:
                mult = (current_time - original_ref)//t_sec
                self.ref_time = ref_time + mult*t_sec
                self.eval = False
                print('multiplicand='+ str(mult))
            if current_time - self.ref_time >= t_sec:
                self.eval = True
            
        if self.type == 'RC':
            t_sec = 0
            ref_time = self.definition
            conversions = {'day':86400,'hr':3600,'min':60,'s':1}
            val_units = list(ref_time.keys())
            # val_units = list(self.definition.keys())
            for unit in val_units:
                t_sec = t_sec + ref_time[unit]*conversions[unit]
            if current_time - app_init >= t_sec:
                self.eval = True
        
        if self.type == 'RWC':
            ref_time = app_init
            t_sec = ref_time
            if current_time - t_sec >= 0:
                # print(time.localtime(current_time))
                # print(time.localtime(t_sec))

                # print(current_time-t_sec)
                self.eval = True
        return self.eval
                        
                        
   
class Sim_Eng:
    '''
    This class should initialize and terminate all the simulation engines necessary to execute the DT
    This class contains all the available simulation engine API, and should also subscribe the requires simulation engines the models in the application need
    '''
    def __init__(self) -> None:
        self.engines = {}
        self.status_eng = dict()
        
    
    def __str__(self) -> str:
        pass
        
    def add_SimEng(self, Eng:object):
        if Eng == '' :
           print('No simulation engine has been addded') 
        else:
            self.engines[Eng.name] = Eng
            self.status_eng[Eng.name] = 'inactive'
    
    def activate_Eng(self):
        for name,Eng in self.engines.items():
            Eng.activate()
            self.status_eng[name] = 'active'
    
class Simulink:
    '''
    This class implements the control and data exchange code for a simulink model
    
    '''
    def __init__(self) -> None:
        pass