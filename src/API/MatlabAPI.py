import sys
import matlab.engine
import time
import os
# import localInterface_gen
from src.API import localInterface_gen

class Simulink:
    def __init__(self,modelName = 'plant', directory = os.getcwd()):
        
        self.modelName = modelName #The name of the Simulink Model original
        self.modelName_exe = modelName + '_wI'
        #maybe a need to change all the modelName in this script to modelName_exe- has been changed
        self.directory = directory #directory of the model 
        #Logging the variables
        self.yHist = 0 
        self.tHist = 0
        # self.MatEng = ''
        self.inputs = []
        self.outputs = [] 
        self.parameterNames = []
        self.initFlag = False
        
    def __str__(self) -> str:
        msg_model = "this class encapsulate a model name with s-function as interface" + self.modelName + '_wI'
        msg_director= 'This model is contain in directory:' + self.directory
        msg_input = 'The inputs of this model are: ' + self.inputs 
        msg_output =  'The outputs of this model are: ' + self.outputs
        return msg_model + '\n' + msg_director + '\n' + msg_input + '\n' + msg_output
        
    def connectToMatlab(self):
        #initial connection
        print("Starting matlab")
        self.eng = matlab.engine.start_matlab()
        # self.eng = matlab.engine.connect_matlab()
        # self.eng.desktop(nargout=0)
        print("Connected to Matlab")
        # matlabSession = matlab.engine.find_matlab()
        # print("matlab session is " + matlabSession[0])

    def disconnect(self):
        #disconnection of the engine
        self.eng.set_param(self.modelName,'SimulationCommand','stop',nargout=0)
        self.eng.quit()
        self.initFlag = False

    def load_model(self, model_name = 'Gain_model'):
        #Load the model
        model_name = self.modelName_exe
        self.eng.eval("model = '{}'".format(model_name),nargout=0) #store name of the model in matlab
        current_dir = self.directory
        self.eng.eval("cd('{}')".format(current_dir),nargout = 0)#setting matlab directory for the models

        self.eng.eval("load_system(model)",nargout=0)
        self.eng.eval("open_system(model)",nargout = 0)
        # self.eng.eval("set_param(model,'FastRestart','on')",nargout = 0)
        # self.eng.set_param(self.modelName_exe,"FastRestart","on")

        print("Model " + model_name + " loaded")
        
        #open model is necessary almost to evaluate anything
        #self.eng.eval("open_system(model)",nargout = 0)
        #Initialize Control Action to 0
        #self.setControlAction(0)
        #print("Initialized Model")
    
    def initialize_model(self,ini_val={})-> None:
        """_summary_
        initialize the model just by defining the inputs 
        Args:
            ini_val (dict, optional): _description_. Defaults to {}.
        """
        inputsDict ={}
        outputDict = {}
        # self.set_input('temp_in',0)
        # print("The initial inputs for model {} are:".format(self.modelName_exe))
        for input in self.inputs:
            if ini_val == {}:
                # print(input)
                self.set_input(input,0)
                inputsDict[input] = 0
            else:
                self.set_input(input,ini_val[input])
        print(self.eng.get_param(self.modelName_exe,'SimulationStatus'))
        
        # self.eng.set_param(self.modelName_exe,'SimulationCommand','start','SimulationCommand','stop',nargout=0)
        self.eng.set_param(self.modelName_exe,'SimulationCommand','start','SimulationCommand','pause',nargout=0)
        # self.eng.set_param(self.modelName_exe,'FastRestart', 'on')
        print(self.eng.get_param(self.modelName_exe,'SimulationStatus'))
        
        print('Model {} has been initiated with the input values: \n {}'.format(self.modelName, inputsDict))
        
        simTime = self.eng.get_param(self.modelName_exe,'SimulationTime')
        print("Current simulation time is " + str(simTime))
        # self.eng.set_param(self.modelName_exe,'StartTime','0')
        # simTime = self.eng.get_param(self.modelName_exe,'SimulationTime')
        # print("Current simulation time, after arrengement, is " + str(simTime))
        for output in self.outputs:
            src_val = self.get_output(output)
            outputDict[output] = src_val
        print('Model {} has been initiated with the output values: \n {}'.format(self.modelName, outputDict))
        self.eng.set_param(self.modelName_exe,'SimulationCommand','stop',nargout=0)
        self.initFlag = True
    def advance(self, inputs_val = {})-> dict:
        """_summary_
        
        Method advance 1 step of the mode, stoping it instantly
        """
        status = self.eng.get_param(self.modelName_exe,'SimulationStatus')
        # print(status)
        # for name in inputs_val:
        #     self.set_input(name,inputs_val[name])
        if status =="stopped" or status == "compiled":
            self.eng.set_param(self.modelName_exe,'SimulationCommand','start','SimulationCommand','pause',nargout=0)
        elif status == "paused":
            self.eng.set_param(self.modelName_exe,'SimulationCommand','step','SimulationCommand','pause',nargout=0)
            # self.eng.set_param(self.modelName_exe,'SimulationCommand','resume','SimulationCommand','pause',nargout=0)
        
                # print(input)
            # self.set_input(input,val)
        # print(self.eng.get_param(self.modelName_exe,'SimulationStatus'))
        simTime = self.eng.get_param(self.modelName_exe,'SimulationTime')
        # print("Current simulation time is " + str(simTime))
        output_vals = {}
        for output in self.outputs:
            output_vals[output] = self.get_output(output)
        return output_vals
      
    
    def initialize_model2(self,values = []):
        #Initialize with input
        if values == []:
            index = 0
            for input in self.inputs:
                values.append(0)
                index +=1
        idx = 0
        print("Initialized Model")
        print("The initial inputs for model {} are:".format(self.modelName_exe))
        for input in self.inputs:
            self.set_input(input,values[idx])
            print(" " + input + '=' + str(values[idx]))
            idx+=1
            
            #self.set_input('input',0)#how to change it?
        
        

        #Start Simulation and then Instantly pause
        print(self.eng.get_param(self.modelName_exe,'SimulationStatus'))
        self.eng.set_param(self.modelName_exe,'SimulationCommand','start','SimulationCommand','pause',nargout=0)
        print(self.eng.get_param(self.modelName_exe,'SimulationStatus'))
        idx = 0
        print("The initial outputs for model {} are:".format(self.modelName))
        for output in self.outputs:
            val_output = self.get_output(output) # how to change it?
            print(" " + output + '=' + str(val_output))
        print(self.eng.get_param(self.modelName_exe,'SimulationStatus'))
        #self.yHist,self.tHist = self.getHistory()
        #print(self.eng.eval('whos'))
    
    def set_input(self, var_name, var_val):
        name = str(var_name)
        self.eng.workspace[name] = var_val

    def get_output(self, var_name)->any:
        name = str(var_name)
        return self.eng.workspace[name]
    
    def pause(self):
        print(self.eng.get_param(self.modelName_exe,'SimulationStatus'))
        self.eng.set_param(self.modelName_exe,'SimulationCommand','pause',nargout=0)
        print(self.eng.get_param(self.modelName_exe,'SimulationStatus'))
    
    def resume(self):
        #print(self.eng.get_param(self.modelName_exe,'SimulationStatus'))
        self.eng.set_param(self.modelName_exe,'SimulationCommand','continue',nargout = 0)
        #print(self.eng.get_param(self.modelName_exe,'SimulationStatus'))
    
    def stop(self):
        print(self.eng.get_param(self.modelName_exe,'SimulationStatus'))
        self.eng.set_param(self.modelName_exe,'SimulationCommand','stop',nargout = 0)
        print(self.eng.get_param(self.modelName_exe,'SimulationStatus'))
    
    def simulate(self):
        # needs to be implemented properly
        pass
    
    def set_config(self, configIdName = 't_ini', configIdVal = 0 , startConfig =  False)-> bool:
        """_summary_
            this method re-configure a simulation, but it only supports
            time configuration IdNames such as t_ini, t_period and t_step
        Args:
            configIdName (str, optional): _description_. Defaults to 't_ini'.
            configIdVal (int, optional): _description_. Defaults to 0.
        """
        if startConfig == False:
            self.eng.eval("set_param(model,'Solver','FixedStep')",nargout = 0)
        # self.eng.set_param(self.modelName_exe,'Solver', 'FixedStep')
            solverType = self.eng.get_param(self.modelName_exe,'Solver')
            print ("Solver in matlab is: " + str(solverType))

        
        if configIdName == 't_ini':
            self.eng.eval("set_param(model,'StartTime','{}')".format(configIdVal),nargout=0)
            # self.eng.set_param(self.modelName_exe,'StartTime', str(configIdVal))
            startTime = self.eng.get_param(self.modelName_exe,'StartTime')
            print ("Start time in matlab is: " + str(startTime))
            return True
        elif configIdName == 't_period':
            startTime = self.eng.get_param(self.modelName_exe,'StartTime')
            endTime = int(startTime) + configIdVal
            self.eng.eval("set_param(model,'StopTime','{}')".format(endTime),nargout=0)
            # self.eng.set_param(self.modelName_exe,'StopTime', str(endTime))
            stopTime = self.eng.get_param(self.modelName_exe,'StopTime')
            print ("Stop time in matlab is: " + str(stopTime))
            return True
        elif configIdName == 't_step':
            self.eng.eval("set_param(model,'FixedStep','{}')".format(configIdVal),nargout=0)
            # self.eng.set_param(self.modelName_exe,'FixedStep', str(configIdVal))
            t_step = self.eng.get_param(self.modelName_exe,'FixedStep')
            print ("Step time in matlab is: " + str(t_step))
            return True
        else:
            print('only three possible time configurations: t_ini, t_peior and t_step, please change')
            return False

    def set_parameter(self,name ="u", value=1):
        '''
        this set the value of a parameter by its name and a desire value
        only works when the block in matlab has the same name as the name set in this function and the block is a constant

        '''
        block_name = str(self.modelName_exe + '/' + name)
        self.eng.set_param('{}'.format(block_name),'value',str(value),nargout=0)
    
    def get_params(self)->list:
        name = self.modelName_exe
        # self.eng.eval("param = find_system('" + name +"','BlockType','Constant')",nargout=0)
        prevresults = self.eng.find_system(name,'BlockType','Constant')
        # result = self.eng.workspace['param']
        result = []
        # print(prevresults)
        for component in prevresults:
            # print(component)
            r = component.replace(name + '/','')
            # print(r)
            result.append(r)
        # print(result)
        return result
    
    def get_status(self):
        return self.eng.get_param(self.modelName_exe,'SimulationStatus')
    
    def setControlAction(self,u):
        #Helper Function to set value of control action
        self.eng.set_param('{}/u'.format(self.modelName),'value',str(u),nargout=0)
    
    def getHistory(self):
        #Helper Function to get Plant Output and Time History
        return self.eng.workspace['out.output'],self.eng.workspace['out.tout']
         
    def connectController(self,controller):
        self.controller = controller
        self.controller.initialize()
    
    def simulate_2(self):
        # Control Loop
        while(self.eng.get_param(self.modelName,'SimulationStatus') != ('stopped' or 'terminating')):
            
            #Generate the Control action based on the past outputs
            u = self.controller.getControlEffort(self.yHist,self.tHist)
            
            #Set that Control Action
            self.setControlAction(u)
            
            #Pause the Simulation for each timestep
            self.eng.set_param(self.modelName,'SimulationCommand','continue','SimulationCommand','pause',nargout=0)
            
            self.yHist,self.tHist = self.getHistory()
    
    def block_format(self,model_name = 'Gain_model_wI',block_name = 'interface', comparison_blocks =[]):
        left_loc = 0
        for block in comparison_blocks:
            full_block= model_name + '/' +block
            self.eng.eval("pos = get_param('{}','Position');".format(full_block), nargout = 0)
            
            self.eng.eval("x_pos = pos(1);", nargout = 0)
            block_loc = self.eng.workspace['x_pos']
            if block_loc >= left_loc:
                left_loc = block_loc
        self.eng.workspace["most_leftPos"] = left_loc
        self.eng.eval("position = get_param('{}','Position');".format(model_name+'/'+block_name),nargout = 0)
        self.eng.eval("x = position(1) +most_leftPos;", nargout =0)
        self.eng.eval("y = position(2);", nargout =0)
        self.eng.eval("width = position(3)+x;", nargout =0)
        self.eng.eval("height = position(4)+y;", nargout =0)
        self.eng.eval("set_param('{}','Position',[x y width height]);".format(model_name+'/'+block_name), nargout =0)

    def model_change(self, model_name = 'Gain_model_wI', function_name = 's-interface',block_name = 'interface', ports_data = [],id_ports = {}):
        '''
        Add a block to a simulink model
        '''

        #function_name = 's-interface'
        #block_name = 'interface'
        self.connectToMatlab()
        self.eng.desktop(nargout=0)
        self.load_model(model_name) #model needs to be open to work (this method load and open the model)
        #sim_model.eng.eval("model_name = '{}'".format(sim_model.modelName),nargout=0) #store name of the block in matlab
        #self.eng.eval("load_system(model)",nargout=0)
        clean_name_model = model_name.rsplit('.slx')[0]
        name_param = clean_name_model + '/' + block_name

        #evaluete names in matlab so can be reuse by matlab itself
        self.eng.eval("func_name = '{}';".format(function_name),nargout=0) #store name of the function in matlab
        self.eng.eval("model_name = '{}';".format(clean_name_model),nargout=0) #store name of the block in matlab
        self.eng.eval("name_param = '{}';".format(name_param),nargout=0) #store name of the block in matlab


        #add the s-function block to the model
        self.eng.eval("add_block('simulink/User-Defined Functions/Level-2 MATLAB S-Function',name_param,'FunctionName',func_name);",nargout=0)
        print('model ' + clean_name_model + ' has been changed with a new block named ' + block_name)
       
        #generate connections
        name_input_var = ports_data['inports']
        name_output_var =ports_data['outports']
        connections = ports_data['connections']
        input_num = int(len(name_input_var))
        output_num = int(len(name_output_var))
         #change position and size
        self.block_format(model_name = clean_name_model,block_name = block_name, comparison_blocks = name_output_var)

        ports_names = name_output_var + name_input_var
        self.eng.eval("interface_block = get_param(name_param,'PortConnectivity');",nargout = 0)
       
        #print(ports_names)
        for port in range(0,len(ports_names)):
            
            self.eng.eval("port_pos = interface_block({}).Position;".format(port+1),nargout = 0)
            self.eng.eval("name = '{}';".format(ports_names[port]),nargout = 0)
            if ports_names[port] in name_output_var:
                self.eng.eval("size_text = strlength(name)*5;",nargout = 0)
            else:
                self.eng.eval("size_text = strlength(name);",nargout = 0)
            self.eng.eval("annotation = Simulink.Annotation(gcs,name);", nargout =0)
            self.eng.eval("port_pos = [port_pos(1)-size_text,port_pos(2)];", nargout =0)
            self.eng.eval("annotation.Position = port_pos;", nargout =0)
       
        #print(connections)
        for connec in connections:
            #delete all connection with input and outputs
            src_name = connec['src']
            dst_name = connec['dst']
            # src_name = connec['src'][0]
            # dst_name = connec['dst'][0]

            if src_name in name_input_var:
                src_Id = id_ports['inputs'][src_name]
                new_src_name = block_name
            else:
                new_src_name = src_name
                src_Id = '1' 
                # src_Id = connec['src'][1] 
            if dst_name in name_output_var:
                dst_Id = id_ports['outputs'][dst_name]
                new_dst_name = block_name
            else:
                new_dst_name = dst_name
                dst_Id= '1'
                # dst_Id= connec['dst'][1]
            
            interface_BN = block_name
            #self.eng.eval("delete_line(model_name,'temp_in/1','Gain/1')")
            src_str_delete=src_name + '/' + '1'
            dst_str_delete=dst_name + '/' + '1'
            # src_str_delete=src_name + '/' + connec['src'][1] 
            # dst_str_delete=dst_name + '/' + connec['dst'][1]
            src_str_create=new_src_name + '/' + src_Id
            dst_str_create=new_dst_name + '/' + dst_Id
            #print("delete_line(model_name,'{}','{}')".format(src_str_delete,dst_str_delete))
            self.eng.eval("delete_line(model_name,'{}','{}');".format(src_str_delete,dst_str_delete),nargout = 0)
            src_str=src_name + '/' + '1'
            dst_str=dst_name + '/' + '1'
            # src_str=src_name + '/' + connec['src'][1] 
            # dst_str=dst_name + '/' + connec['dst'][1]
            text = "model_name,'{}','{}','autorouting','on'".format(src_str_create,dst_str_create)
            #print("add_line({})".format(text))
            self.eng.eval("add_line({});".format(text),nargout = 0)
               

        #save model at the end of the changes
        self.eng.eval("save_system(model_name);",nargout =0)
        print('Model' + model_name+' has been saved')
        #self.disconnect

    def interface_gen(self):
        model_inspect = localInterface_gen.model_inspection(model_name = self.modelName, directory = self.directory , folder_name = self.modelName)
        #generate all the xml files for inspection
        model_inspect.unzipped()
        print('\n')
        #extract input,output and connections data
        model_data = model_inspect.extract()
        print('\n')
        #generate a copy of the model ready to be change to write the interface
        #for copying it is necessary the name with extension .slx
        name4copy=self.modelName + '.slx'
        model_copy = localInterface_gen.model_copy(model_name = name4copy, directory = self.directory)
        #create a copy of the model and return the new name and the directory where it is stored
        [model_name, directory] = model_copy.copy_file()
        #print(model_name, directory) 
        print('\n')
        
        

        #generate the object to genereta the file for the interface: this case s-function function
        func_name = model_name + "_func"
        name_input_var = model_data['inports']
        name_output_var =model_data['outports']
        #safe inputs and outputs names in the object
        self.inputs = name_input_var
        self.outputs = name_output_var
        input_num = int(len(name_input_var))
        output_num = int(len(name_output_var))
        s_func_name = localInterface_gen.interfaceFile_gen(file_name = func_name, 
                                                           input_num=input_num, output_num = output_num, 
                                                           function_name = func_name,name_input_var = name_input_var, 
                                                           name_output_var=name_output_var, directory = directory)
        #generate the .m file
        id_ports = s_func_name.generate()
        print('\n')
        #print(id_ports)

        #change the model
        self.model_change(model_name = model_name ,function_name = func_name, block_name = 'interface', ports_data = model_data,id_ports = id_ports)
        self.eng.eval("close_system",nargout=0)
        print("simulink model is closed")
        #sim_model = Simulink(modelName = model_name, directory = os.getcwd())
        #sim_model.connectToMatlab()
        #sim_model.Load_model() #model needs to be open to work (this method load and open the model)
        





