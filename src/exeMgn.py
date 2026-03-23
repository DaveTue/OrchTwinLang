import logging
import sys
import time
from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt

import src.GlOb
import src.Comm

logging.basicConfig(filename='loggings\\Exe.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConnectionHandler:
    def __init__(self) -> None:
        
        self.connections = []
        
    def __str__(self) -> str:
        message = 'Connections are:\n'
        for connection in self.connections:
            m =''
            for key, value in connection.items():
                if key == 'id':
                    m += 'id:' + str(value)
                if key == "src":
                    m += ' '+ str(value) + '->'
                if key == "dst":
                    m += '' + str(value)
            message = message + m + '\n'

        return message  
    
    def connect(self,source:dict = {'component':object, 'output':'name'}, 
                destination:dict = {'component':object, 'input':'name'} , 
                exPattern :dict = {'type': 'FIFO','PQ_conds':[]}):
        '''
        Define one connection each time by defining source and destination of the connection
        It also defines the relationship
        '''
        connection ={}
        # this is just to make sure it works
        srcPort = self.findPort(source['component'],source['output'], portType= 'output')
        dstPort = self.findPort(destination['component'],destination['input'], portType= 'input')
        
        
        if srcPort == None :
            print(" Connection can not be stablish because the source ("+ source['component'].name+") port name (" + source['output']+ ") is incorrect or not an output")
            return 0
        if dstPort == None:
            print(" Connection can not be stablish because the destination ("+ destination['component'].name+") port name (" + destination['input']+ ") is incorrect or not an input")
            return 0
        
        id = 'Conn' + str(len(self.connections))
        src =(source['component'].name,source['output'])
        dst =(destination['component'].name,destination['input'])
        conn = Comm.Connector(src = {'component':source['component'],'output_name':source['output']},
                              dst = {'component':destination['component'], 'input_name':destination['input']},
                            exchange_pattern = exPattern)
        conn_def = {'id': id,'connector':conn,'src':src,'dst':dst}
        
        self.connections.append(conn_def)
        
        # generation of connection
        
        
        # if source.direction != 'out' or destination.direction != 'in':
        #     print('The source must be an output of a model and/or the destination must be an input of a model')
        # else: 
        #     connection['src'] = source
        #     connection['dst'] = destination
        #     id_src = source.model.modelName +':'+source.name 
        #     id_dst = destination.model.modelName +':'+destination.name
            
        #     self.connections.append(connection)
        #     print('Connection generated:' + id_src + "->" + id_dst)
    
    def findPort(self, model = object, portName = "name" , portType = 'output')-> object:
        """_summary_
            return the object port for its ussage in the connection, by knowing the 
            object model, the name of the port and its type: input or output
        Args:
            model (_type_, optional): _description_. Defaults to object.
            portName (str, optional): _description_. Defaults to "name".
            portType (str, optional): _description_. Defaults to 'output'.

        Returns:
            object: _description_
        """
        # print(portType)
        if portType == 'output':
           for id,port in model.outports.items() :
                
                if port.name == portName:
                    
                    return port
        if portType == 'input':
           for id,port in model.inports.items() :
           
               if port.name == portName:
                    return port


class exeArea:
    
    COMUNICATION_TYPES = {'tr': 'Transformator', 'agg': 'Aggreggator',
                       'dup': 'Dupplicator','spl': 'Splitter','conn': 'Connector','swi': 'Switch', 
                       'inp': 'Input port', 'outp': 'Output port' }
    SINK_TYPES = {'sink': 'Sink' }
    COSIMULATION_TYPES = {'mod': 'Model'}
    SOURCE_TYPES = {'source': 'Source' }
    SIMTYPES = {'time_based':'time_based','invoke':'simulation','continues':'simulation'}
    
    def __init__(self, name = 'area',components=[],triggers =[], 
                 allComponents = [],appTime=None) -> None:
        self.name = name
        self.areaComponents =  components
        self.originalComponents =  []
        for comp in self.areaComponents:
            self.originalComponents.append(comp)
        self.appTime = appTime
        if allComponents == []:
            self.allComponents = self.areaComponents
        else:
            self.allComponents = allComponents
        
        self.startTrigger,self.stopTrigger = self.TriggerDef(triggers=triggers)         
        self.triggers = [self.startTrigger,self.stopTrigger]
        # self.triggers = triggers
      
            
        self.relationships = self.relationAnalysis(self.areaComponents,self.allComponents)
        # print(self.relationships)
        self.OutputMapping = self.OutputsrelationAnalysis(self.areaComponents,self.allComponents)
        areaSchedule = compScheduling(relationship_dict=self.relationships,title= self.name)
        # areaSchedule = cosimSchedule(self.relationships)
        self.cycleFlag = areaSchedule.cycleDetected
        self.cycleComp = areaSchedule.cycle_topological_order
        self.compSchedule = areaSchedule.topological_order
        self.cycleName = areaSchedule.cycleName
        
        self.exeComponents=[]
        for compName in self.compSchedule:
            # for exeComp in self.areaComponents:
            for exeComp  in self.originalComponents:
                if exeComp.name == compName:
                    self.exeComponents.append(exeComp)
                    break
        self.areaInputs, self.areaOutputs,self.innerAreaInputs,self.innerAreaOutputs = self.AreaPorts(Inputrelationships=self.relationships,
                                                           outputsRelationship=self.OutputMapping)
        
    def TriggerDef(self,triggers = [])-> tuple:
        """_summary_

        Args:
            triggers (list, optional): _description_. Defaults to [].

        Returns:
            tuple: _description_
        """
        defaultStart = {'type':'stop', 'class':'temporal','definition':{'type':'time','value': 5,'unit':'s'}}
        defaultStop = {'type':'stop', 'class':'guard','definition':'globals.stopApp == True'}
        stopTrig = None
        startTrig = None
        if triggers == []:
            print('Defult triggers will be used, no triggers as input')           
            stopTrig = defaultStop
            startTrig = defaultStart
        else:
            if len(triggers) > 2:
                print('Only the last start and stop triggers will be consider')
            for trigger in triggers:
                if trigger['type'] == 'start':
                    startTrig = trigger
                if trigger['type'] == 'stop':
                    stopTrig = trigger
            if stopTrig == None:
                stopTrig = defaultStop
            if startTrig == None:
                startTrig = defaultStart

        startTrigger = GlOb.Trigger(name = 'Starttrigger' + self.name, typ=startTrig['type'],
                                    category=startTrig['class'],definition=startTrig['definition']
                                    ,allComponents=self.allComponents,appTime=self.appTime)

        stopTrigger = GlOb.Trigger(name = 'Stoptrigger' + self.name, typ=stopTrig['type'],
                                    category=stopTrig['class'],definition=stopTrig['definition'],
                                     allComponents=self.allComponents,appTime=self.appTime)
        
            
        # trigger = {'type':'start', 'class':'guard','definition':'MassSpringMod.DisplacementOutput > 10'}
        # trigger = {'type':'start', 'class':'temporal','definition':{'type':'freq','value': 1,'unit':'s'}}
        # trigger = {'type':'start', 'class':'temporal','definition':{'type':'time','value': 5,'unit':'s'}}
        # trigger = {'type':'start', 'class':'data','definition':'MassSpringMod.DisplacementOutput'}
        return(startTrigger,stopTrigger)
    
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
              
    def relationAnalysis(self, components, allComponents) -> dict:
        """
        Analyze a set of components and generate a dictionary of dependencies.

        Args:
            components (list): The list of components to analyze.
            allComponents (list): The complete list of components in the system.

        Returns:
            dict: A dictionary mapping each component name to its dependencies.
                Components without dependencies or inports are mapped to an empty dictionary.
        """
        Alldependencies= {}
        allCompNames = {}
        areaCompNames = []
        for component in components:
            areaCompNames.append(component.name) 
        for component in allComponents:
            allCompNames[component.name] = component
        sizeDict = len(list(allCompNames.keys()))
        # if sizeDict != len(allComponents):
        #     print('All names in the system should be different, there are some repeated names')
        #     return 0
        if sizeDict != len(allComponents):
            raise ValueError("Duplicate names found in the system.")
        compFound =[]
        for component in components:
            dependsON ={}
            if component.inports == None:
                Alldependencies[component.name] = {}
            else:
                for inport,port in component.inports.items():
                    componentSrc =port.connector.src['component'].name
                    if componentSrc in dependsON.keys():
                        dependsON[componentSrc].append(port.name)
                    else:
                        dependsON[componentSrc]=[port.name]

                Alldependencies[component.name] = dependsON
            compfoundTemp = list(dependsON.keys())
            for comp in compfoundTemp:
                compFound.append(comp)
            
        flagRepeat = False
        
        for comp in compFound:
            if comp not in areaCompNames and allCompNames[comp].type in list(self.COMUNICATION_TYPES.keys()):
                flagRepeat = True
                components.append(allCompNames[comp])
        
        if flagRepeat == True:
            Alldependencies = self.relationAnalysis(components,allComponents)
        
        return Alldependencies
    
    def OutputsrelationAnalysis(self, components, allComponents) -> dict:
        """
        Analyze a set of components and generate a dictionary of dependencies.

        Args:
            components (list): The list of components to analyze.
            allComponents (list): The complete list of components in the system.

        Returns:
            dict: A dictionary mapping each component name to its dependencies.
                Components without dependencies or inports are mapped to an empty dictionary.
        """
        
        OutputsMapping= {}
        allCompNames = {}
        areaCompNames = []
        for component in components:
            areaCompNames.append(component.name) 
        for component in allComponents:
            allCompNames[component.name] = component
        sizeDict = len(list(allCompNames.keys()))
        # if sizeDict != len(allComponents):
        #     print('All names in the system should be different, there are some repeated names')
        #     return 0
        if sizeDict != len(allComponents):
            raise ValueError("Duplicate names found in the system.")
        compFound =[]
        for component in components:
            # print(component)
            # print('---------------------------------------------')
            # print(component.outports)
            dependsON ={}
            if component.outports == None:
                OutputsMapping[component.name] = {}
            else:
                for outport,port in component.outports.items():
                    # print(port.connector)
                    if port.connector !=[]:
                        componentSrc =port.connector.dst['component'].name
                    
                        if componentSrc in dependsON.keys():
                            dependsON[componentSrc].append(port.name)
                        else:
                            dependsON[componentSrc]=[port.name]

                OutputsMapping[component.name] = dependsON
            compfoundTemp = list(dependsON.keys())
            for comp in compfoundTemp:
                compFound.append(comp)
            
        flagRepeat = False
        
        for comp in compFound:
            if comp not in areaCompNames and allCompNames[comp].type in list(self.COMUNICATION_TYPES.keys()):
                flagRepeat = True
                components.append(allCompNames[comp])
        
        if flagRepeat == True:
            OutputsMapping = self.OutputsrelationAnalysis(components,allComponents)
        
        return OutputsMapping
    
    def AreaPorts(self, Inputrelationships, outputsRelationship)-> tuple:
        compNames = []
        for comp in self.exeComponents:
            compNames.append(comp.name)
        #extraction of outputs in the area
        areaOutputs ={}
        innerAreaOutputs ={}
        for areaComp, dependency  in outputsRelationship.items():
            aOInputs = []
            ainnerOutnputs =[]
            if areaComp in compNames:
                compsDepencency = list(dependency.keys())
                for compDepen in compsDepencency:
                    if compDepen not in compNames:
                        aOInputs += dependency[compDepen]
                        areaOutputs[areaComp] = aOInputs
                        innerAreaOutputs[areaComp] =ainnerOutnputs
                        # areaOutputs[areaComp] = aOInputs + dependency[compDepen]
                    else:
                        ainnerOutnputs += dependency[compDepen]
                        innerAreaOutputs[areaComp] = ainnerOutnputs 
                        areaOutputs[areaComp] = aOInputs
       #extraction of inputs of the area
        areaInputs ={}
        innerAreaInputs ={}
        for areaComp, dependency  in Inputrelationships.items():
            compsDepencency = list(dependency.keys())
            if areaComp in compNames:
                aInputs = []
                ainnerinputs =[]
                for compDepen in compsDepencency:
                    if compDepen not in compNames:
                        aInputs +=dependency[compDepen]
                        areaInputs[areaComp] = aInputs 
                        innerAreaInputs[areaComp] = ainnerinputs
                    else:
                        ainnerinputs +=dependency[compDepen]
                        innerAreaInputs[areaComp] = ainnerinputs 
                        areaInputs[areaComp] = aInputs 
                        
        return areaInputs, areaOutputs, innerAreaInputs,innerAreaOutputs
    
    def portObj_detect(self, exeComp = []):
        '''
        Detect all possible ports in the system and generate the system port objects (sys_port)
        '''
        # new implementation 
        allInports = []
        allOutports = []
        InputsNames = {}
        OutputNames = {}
        for component in exeComp:
            modelName = component.name
            # print("For {} the detected ports are:".format(component.name))
            if component.inports != None:
                innames =[]
                for id,input in component.inports.items():
                    
                    # port = sys_port(component,input)
                    allInports.append(input)
                    InputsNames[modelName]=innames.append(input.name)
                    # key = modelName + ':'+input.name
                    # self.ports[key] = input
                    # print(" Input port name {}".format(key))
            
                       
            if component.outports !=None:
                outnames =[]
                for id,output in component.outports.items():
                    allOutports.append(output)
                    OutputNames[modelName]=outnames.append(output.name)
                    # port = sys_port(component,output)
                    # key = modelName + ':'+output.name
                    # self.ports[key] = output
                    # print(" Output port name {}".format(key))
            
        
        return allInports,allOutports
    
    def outputsInCycle (self) -> dict:
        Componets_outputs ={}
        components =  self.exeCompCycle
        compNames = []
        for comp in components:
            compNames.append(comp.name)
            
        for component in components: 
            Componets_outputs[component.name] =[]
            for outportID,port in component.outports.items():
                    componentDst = port.connector.dst['component'].name
                    if componentDst in compNames:
                        Componets_outputs[component.name].append(port.name)
            
        
        return Componets_outputs

    def inputsInCycle (self) -> dict:
        Componets_inputs ={}
        components =  self.exeCompCycle
        compNames = []
        for comp in components:
            compNames.append(comp.name)
            
        for component in components: 
            Componets_inputs[component.name] =[]
            for inportID,port in component.inports.items():
                    componentSrc = port.connector.src['component'].name
                    if componentSrc in compNames:
                        Componets_inputs[component.name].append(port.name)
            
        
        return Componets_inputs
    
    def modelDetector(self, components = [])-> list:
        """_summary_
            detecs out of the inserted list which are models types. 
        Returns:
            list: _description_
        """
        models = []
        for component in components:
            if type(component) is Comm.Model:
                models.append(component)
        return models
    
    def DataProcDetector(self, components = [])-> list:
        """_summary_
            detecs out of the inserted list which are models types. 
        Returns:
            list: _description_
        """
        models = []
        for component in components:
            if type(component) is Comm.Model:
                models.append(component)
        return models

class cosim(exeArea):
    
    def __init__(self, name = 'Cosim Area 1',components=[],triggers =[], 
                 simexec_type = 'time_based', definition = {}, 
                 configuration = {},
                 allComponents = [],appTime = None) -> None:
        
        super().__init__(name,components,triggers,allComponents,appTime)
        
        self.models = self.modelDetector(components= components)
        self.definition = definition
            
        self.simexec_type = simexec_type
        self.configuration = configuration
        if self.simexec_type == 'continuous':
            if self.definition == {}:
                print( 'The continuos exection will execute based on the frequence of the inputs arriving to the models\n')
            if configuration != {}:
                print( '\nThe continuos exection will not use the configuration file set up. Since it does not require it')
        elif self.simexec_type == 'time_based':
            #config example config = {'exeTime':'FTRT',
            # 'exeConf':{'t_ini':(0,'s'),'t_period':(1,'hr'), 't_step':(1,'s')}}
            if configuration != {}:
                self.exeTime,self.exeConf =self.parseConfig(configDict=configuration)
            else:
                self.exeTime,self.exeConf =('','')
              
        if self.cycleFlag == True:
            self.loop = loop(cycleName=self.cycleName,
                             cycleCompNames= self.cycleComp,
                             areaCompSchedule=self.compSchedule,
                             exeComponents=self.allComponents,
                             exeType='UserSchedule',
                             relationships=self.relationships,
                             assumption={})
            #example of assumption 'Gain_modelFMU': [{ 'name': 'temp_in','value': 50 },
                                                        #  { 'name': 'mass_in','value': 12 }, 
                                                        #  { 'name': 'vol_in','value': 3.15 }] 
        else:
            self.loop =None
            
        self.newScheduleCompName,self.newExeComponents = self.compScheduleWLoops()
        self.allInputs, self.allOutputs = self.portObj_detect(self.newExeComponents)
        self.cout_withPath, self.cout_withOutPath,self.outputsToConn = self.ExPat_filter( execomponents = self.newExeComponents, 
                                                                      areaOutports =self.areaOutputs , exPat = 'LVoC')
            
    def initialize(self,models =[], config = {})-> None:
        """_summary_
        this method initialize all the models contained in this execution area

        Returns:
            str: _description_ returns the states of the models 
        """
        # example config = {'t_ini':0,'t_period' :30, 't_step':1}
        if models == []:
            models = self.models
        if models != []:
            if config == {}:
                config = self.exeConf
            for model in models:
                # model.initialize_model2()
                model.initialize() 
            for model in models:
                model.setConfig(confParam = config)
    
    def parseConfig(self,configDict= {})->tuple:
        """_summary_

        Args:
            configuration (dict, optional): _description_. Defaults to {}.

        Returns:
            tuple: _description_
        """
        if configDict == {}:
            print('No data, returning empty')
            return {}
        exeTime = configDict['exeTime']
        execonf = configDict['exeConf']
        new_execonf ={}
        for typ, val in execonf.items():
            new_execonf[typ] = self.timeconverter(unit=val[1],value=val[0])
        
        return exeTime,new_execonf
    
    def compScheduleWLoops(self)-> list:
        """_summary_
            This method actually computes the components that needs to be schedule considering loops.
            
            this method will compute the order to execute the components, which later will be 
            used in the other execution steps, only considers the components within a particular area. 
            It should detect automatically the "communication components" related to the area.
        Returns:
            list: _description_
        """
        # for compName in self.compSchedule:
        #     for exeComp in self.allComponents:
        #         if exeComp.name == compName:
        #             self.exeComponents.append(exeComp)
        #             break
        newSchedule =[]
        newExeSchedule =[]
        # print(self.cycleFlag)
        if self.cycleFlag == False:
            newSchedule = self.compSchedule
            newExeSchedule = self.exeComponents
            # exeComps = self.allComponents
            # for compName in self.compSchedule:
            #     for exeComp in exeComps:
            #         if exeComp.name == compName:
            #             newSchedule.append(compName)
            #             newExeSchedule.append(exeComp)
            #             break
        else:
            exeloop = self.loop
            exeComps = self.allComponents + [exeloop]
            for compName in self.compSchedule:
                if compName in self.cycleComp:
                    if self.loop.name not in newSchedule:
                        newSchedule.append(self.loop.name)
                        newExeSchedule.append(self.loop)
                else:
                    for exeComp in exeComps:
                        if exeComp.name == compName:
                            newSchedule.append(compName)
                            newExeSchedule.append(exeComp)
                            break
        
        return newSchedule,newExeSchedule
    
    def ExPat_filter(self, execomponents = [], areaOutports ={} , exPat = 'LVoC' ):
        """_summary_

        Args:
            execomponents (list, optional): _description_. Defaults to [].
            areaOutports (dict, optional): _description_. Defaults to {}.
            exPat (str, optional): _description_. Defaults to 'LVoC'.

        Returns:
            _type_: _description_
        """
        cout_withPath = {}
        cout_withOutPath ={}
        for components, outputs in areaOutports.items():
            if outputs != []:
                for comp in execomponents:
                    if comp.name == components:
                        output_PattExe =[]
                        output_woPattExe =[]
                        for id, port in comp.outports.items():
                            if port.name in outputs:
                                # print(port.name)
                                # print(port.connector.Pattern.type)
                                if port.connector.Pattern.type == exPat:
                                    output_PattExe.append(port.name)
                                    cout_withPath[comp.name] =output_PattExe
                                        # comp_LVoCExe.append(components)
                                else:
                                    output_woPattExe.append(port.name)
                                    cout_withOutPath[comp.name] =output_woPattExe
        outputsToConn = {}
        for comp in execomponents:
            if comp.name in list(cout_withPath.keys()):
                outputswPath = cout_withPath[comp.name]
                output2Conn =[]
                for id,output in comp.outputs.items():
                    if output['name'] not in outputswPath:
                        output2Conn.append(output['name'])
                outputsToConn[comp.name] = output2Conn       
                    
            else:
                outputsToConn[comp.name] = ["all"]
                
                
        return cout_withPath, cout_withOutPath,outputsToConn
     
    def execute(self, simexec_type = '')->None:
        """defines which function to use to execute the area, depending on the
        execution type (simexec_type) has been defined
        """
        # make sure that the simexec_type has a value
        if simexec_type == '':
            if self.simexec_type == '':
                print("Error, the simulation can not be executed since there is no execution type defined")
                return 0
            simexec_type = self.simexec_type
        print('\n***********************Execution of area' + self.name + '***********************\n')
        if simexec_type == 'continuous':
            if self.definition == {}:
                print( 'The continuos exection will execute based on the frequence of the inputs arriving to the models\n')
            if self.configuration != {}:
                print( '\nThe continuos exection will not use the configuration file set up. Since it does not require it')
            # need to create the method that execute a continues time execution
            # self.initialize()
            self.continuous(defintion=self.definition)
            
        elif simexec_type == 'time_based':
            if self.configuration == {}:
                print('\n Error in the definition of the execution type time_based. It must contain some kind of configuration')
                confExample = {'exeTime':'FTRT', 'exeConf':{'t_ini':0,'t_period' :11, 't_step':1}}
                print('An example of a configuration is ' + str(confExample) + ' all the values in examples are in seconds')
            else:
                
                #execute the area
                self.timeSync(exeTime = self.exeTime, exeConf = self.exeConf)    
                
        elif simexec_type == 'invoke':
            
            self.invoke()
        
        if self.allOutputs != None:
            for output in self.allOutputs:
                output.exchReady = True
                # output.connector.Pattern.enableTransfer()
                             
    def timeSync(self,exeTime = 'FTRT', 
                 exeConf = {'t_ini':0,'t_period' :11, 't_step':1},
                 exeComponents = [],iter = 0, ExeModeIter = 'Live')-> None:
        """_summary_

        Args:
            exeTime (str, optional): _description_. Defaults to 'FTRT'. It can only be FTRT = faster than real time or RT real time

        Returns:
            dict: _description_
        """
        # simType = 'time_based'
        if exeTime != 'FTRT' and exeTime != 'RT':
            print('The exeTime parameter can only have two values: \n FTRT: Faster Than Real-Time \n RT: Real-time')
            return False

        t_0= exeConf['t_ini']
        iter = iter
        t = t_0
        t_step = exeConf['t_step']
        t_end = t + exeConf['t_period']
        # ExeModeIter
        if exeComponents == []:
            exeComponents = self.newExeComponents
            # exeComponents = self.exeComponents
        # print(exeComponents)
        while t <= t_end and self.stopTrigger.evaluate() == False: 
            logging.info(f'---------------- time is {t} ----------------------')
            logging.info(f'---------------- iter is {iter} ----------------------')
            # print(f'-----------------{self.stopTrigger.evaluate()}----------------------------')
            for component in exeComponents:
                logging.info(f'---------------- {component.name} ----------------------')
                name = component.name
                if type(component) is Comm.Model:
                    
                    logging.info(f'---------------- {name} ----------------------')
                    print('\n')
                    print("component {} :".format(name))
                   
                    if iter == 0 and self.cout_withPath != {}:
                        component.runStep(outputsToConn=self.outputsToConn[name]) 
                        # logging.info(f'Output contain for {name}')
                    elif iter == 0:
                        component.runStep() 
                        # logging.info(f'why runing {name} ruunig step')
                    elif self.cout_withPath != {} and t < t_end:
                        # name = component.name
                        component.runStep(inputsFromConn= self.innerAreaInputs[name],
                                          outputsToConn=self.outputsToConn[name]) 
                        # logging.info(self.innerAreaInputs[name])
                        # logging.info(self.outputsToConn[name])
                        # logging.info(f'running {name} whtn t<tend')
                    else:
                        # name = component.name
                        component.runStep(inputsFromConn= self.innerAreaInputs[name],
                                          outputsToConn = ["all"]) 
                        # logging.info(f'running {name} when t =e_end and pass all otuputs')
                        
                    # if iter == 0 and exeComponents.index(component) == 0:
                    #     component.runStep(ExeMode = 'Initial')          
                    # else:
                       
                        
                    #     component.runStep() 
                        
                elif type(component) is Comm.ConfigComp:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.setParam()    
                         
                elif type(component) is loop:
                    print('\n')
                    print("component {} :".format(component.name))
                    
                    component.solve(simType = 'time_based',schedule = [], iter = iter)          
                    
                else:
                    print('\n')
                    print("component {} :".format(component.name))
                    # component.behavior()
                    if iter == 0 and self.cout_withPath != {}:
                        component.behavior(outputsToConn=self.outputsToConn[name]) 
                        # logging.info(f'Output contain for {name}')
                    elif iter == 0:
                        component.behavior() 
                        # logging.info(f'why runing {name} ruunig step')
                    elif self.cout_withPath != {} and t < t_end:
                        # name = component.name
                        component.behavior(inputsFromConn= self.innerAreaInputs[name],
                                          outputsToConn=self.outputsToConn[name]) 
                        # logging.info(f'running {name} whtn t<tend')
                    else:
                        # name = component.name
                        component.behavior(inputsFromConn= self.innerAreaInputs[name],
                                          outputsToConn = ["all"]) 
                        # logging.info(f'running {name} when t =e_end and pass all otuputs')
                    
            t +=t_step
            iter += 1
            print('\n')
            print('time is:' + str(t) )
            print('iteration is:' + str(iter) )
            print('\n')
            if exeTime == 'RT':
                time.sleep(t_step)

        for component in exeComponents:
                if type(component) is Comm.Model:
                    print("component {} has been stopped".format(component.name))
                    component.stop()
    
    def invoke(self)->None:
        exeComponents = self.newExeComponents        
         
        for component in exeComponents:
            if type(component) is Comm.Model:
                print('\n')
                print("component {} :".format(component.name))
                component.simulate()  
            elif type(component) is Comm.ConfigComp:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.setParam()        
            elif type(component) is loop:
                print('\n')
                print("component {} :".format(component.name))
                component.solve(simType = 'complete',schedule = [], iter = iter)          
            else:
                print('\n')
                print("component {} :".format(component.name))
                component.behavior()
        
        # iter += 1
        print('\n')
        # print('time is:' + str(t) )
        # print('iteration is:' + str(iter) )
        print('\n')
            

        for component in exeComponents:
                if type(component) is Comm.Model:
                    print("component {} has been stopped".format(component.name))
                    component.stop()
     
    def continuous(self, defintion = {})->None:   
        # example of definition = {'freq':1, 'unit':s}
        """_summary_

        Args:
            defintion (dict, optional): _description_. Defaults to {}.
        """
        #needs to define the definition if involved
        exeComponents = self.newExeComponents        
        while self.stopTrigger.evaluate() == False: 
            for component in exeComponents:
                if type(component) is Comm.Model:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.simulate() 
                    
                elif type(component) is Comm.ConfigComp:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.setParam()
                             
                elif type(component) is loop:
                    print('\n')
                    print("component {} :".format(component.name))
                    
                    component.solve(simType = 'simulation',schedule = [], iter = iter)          
                    
                else:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.behavior()
            
            # iter += 1
            print('\n')
            # print('time is:' + str(t) )
            # print('iteration is:' + str(iter) )
            print('\n')
            

        for component in exeComponents:
                if type(component) is Comm.Model:
                    print("component {} has been stopped".format(component.name))
                    component.stop()
                    
class srcExe(exeArea):
    
    def __init__(self,name = 'SrcArea51',components=[],triggers =[{'type':'start', 'class':'temporal','definition':{'type':'freq','value': 1,'unit':'s'}}], 
                 exec_type = 'time_specific', 
                 definition ={'type':'freq', 'value': 10, 'unit':'s'  },
                 allComponents = [], appTime = None,delayTime = 2) -> None:
        
        super().__init__(name,components,triggers,allComponents,appTime)
        self.dataProc = self.DataProcDetector(components= components)
        
        self.delayTime = delayTime
        self.running =True
        self.stop = False
        
        self.command = None
        
        self.exec_type = exec_type
        self.definition = definition
        
        if self.cycleFlag == True:
            print('There most be an error defining this area, since cycles in this area are not recommended')

        self.allInputs, self.allOutputs = self.portObj_detect(self.exeComponents)
        
    def initialize(self,sources =[], config = {"type" : "freq", "unit": "s", "occurrences_per_unit":1})-> None:
        """this method initialize all the sources contained in this execution area

        Args:
            sources (list, optional): _description_. Defaults to [].
            config (dict, optional): _description_. Defaults to {"type" : "freq", "unit": "s", "occurrences_per_unit":1}.
        """
        if sources == []:
            sources = self.exeComponents
        for source in sources:
            # model.initialize_model2()
            source.initialize() 
        for source in sources:
            # source.setConfig(confParam = config)
            if type(source) is Comm.Source:
                # source.controller(command = 'configuration',config = config)
                pass
                # print(source.interfaceObj.client)
    
    def execute(self, exec_type = '') -> None:
        if exec_type == '':
            if self.exec_type == '':
                print("Error, the source area can not be executed since there is no execution type defined")
                return 0
            exec_type = self.exec_type
        print('\n***********************Execution of area' + self.name + '***********************\n')
        if exec_type == 'streaming':
            self.streaming
            
            
        elif exec_type == 'time_specific':
            
            self.time_specific()
        elif exec_type == 'invoke':
            self.invoke()
        
        if self.allOutputs != None:
            for output in self.allOutputs:
                output.exchReady = True
        
    def time_specific(self,exeConf ={'type':'freq','value': 5,'unit':'s'})->None:
        # conf ={'type':'time','value': 1,'unit':'s'}
        iter = 0
        # t = 0
        t_sleep = self.timeconverter(unit=exeConf['unit'],value=exeConf['value'])
        # ExeModeIter
        
        exeComponents = self.exeComponents
        for component in exeComponents:
            if type(component) is Comm.Source:
                component.controller(command='start')
        # for component in exeComponents:
        #         if type(component) is Comm.Source:
        #             component.controller(command='start')
        time.sleep(self.delayTime)
        #as long as it is not stopped
        while self.stopTrigger.evaluate() == False: 
            for component in exeComponents:
                if type(component) is Comm.Source:
                    print('\n')
                    print("component {} :".format(component.name)) 
                    component.pull_data()
                elif type(component) is Comm.Model:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.runProcessing()
                elif type(component) is Comm.ConfigComp:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.setParam()         
                else:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.behavior()
            if self.stop == True:
                break
            time.sleep(t_sleep)
            # t +=t_step
            iter += 1
            print('\n')
            # print('time is:' + str(t) )
            print('iteration is:' + str(iter) )
            print('\n')
        for component in exeComponents:
            if type(component) is Comm.Source:
                component.controller(command='pause')
    
    def streaming(self)->None:
        
        exeComponents = self.exeComponents
        
        for component in exeComponents:
                if type(component) is Comm.Source:
                    component.controller(command='start')
        #as long as it is not stopped
        time.sleep(self.delayTime)
        while self.stopTrigger.evaluate() == False: 
            for component in exeComponents:
                if type(component) is Comm.Source:
                    print('\n')
                    print("component {} :".format(component.name)) 
                    component.pull_data()
                elif type(component) is Comm.Model:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.runProcessing()    
                elif type(component) is Comm.ConfigComp:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.setParam()     
                else:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.behavior()
            if self.stop == True:
                break
            
        for component in exeComponents:
            if type(component) is Comm.Source:
                component.controller(command='pause')
                    
    def invoke(self)->None:
                
        exeComponents = self.exeComponents
        
        for component in exeComponents:
                if type(component) is Comm.Source:
                    component.controller(command='start')
        time.sleep(self.delayTime)
        for component in exeComponents:
            if type(component) is Comm.Source:
                print('\n')
                print("component {} :".format(component.name)) 
                component.pull_data()
            elif type(component) is Comm.Model:
                print('\n')
                print("component {} :".format(component.name))
                component.runProcessing() 
            elif type(component) is Comm.ConfigComp:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.setParam()        
            else:
                print('\n')
                print("component {} :".format(component.name))
                component.behavior()
       
        print('\n')
        
        for component in exeComponents:
            if type(component) is Comm.Source:
                component.controller(command='pause')
          
class sinkExe(exeArea):
    
    def __init__(self,name = 'SrcArea51',components=[],
                 triggers =[{'type':'start', 'class':'temporal','definition':{'type':'freq','value': 1,'unit':'s'}}], 
                 exec_type = 'time_specific', 
                 definition ={'type':'freq', 'value': 10, 'unit':'s'  },
                 allComponents = [], appTime = None, delayTime = 3) -> None:
        
        super().__init__(name,components,triggers,allComponents,appTime)
        self.dataProc = self.DataProcDetector(components= components)
        
        self.delayTime =  delayTime
        self.running =True
        self.stop = False
        
        self.command = None
           
        self.exec_type = exec_type
        self.definition = definition        
        
        if self.cycleFlag == True:
            print('There most be an error defining this area, since cycles in this area are not recommended')
        
        self.allInputs, self.allOutputs = self.portObj_detect(self.exeComponents)
    
    def initialize(self,sinks =[], config = {"type" : "freq", "unit": "s", "occurrences_per_unit":1})-> None:
        """this method initialize all the sources contained in this execution area

        Args:
            sources (list, optional): _description_. Defaults to [].
            config (dict, optional): _description_. Defaults to {"type" : "freq", "unit": "s", "occurrences_per_unit":1}.
        """
        if sinks == []:
            sinks = self.exeComponents
        for sink in sinks:
            # model.initialize_model2()
            sink.initialize() 
        for sink in sinks:
            # source.setConfig(confParam = config)
            if type(sink) is Comm.Source:
                # sink.controller(command = 'configuration',config = config)
                pass
    
    def execute(self, exec_type = '') -> None:
        if exec_type == '':
            if self.exec_type == '':
                print("Error, the source area can not be executed since there is no execution type defined")
                return 0
            exec_type = self.exec_type
        print('\n***********************Execution of area' + self.name + '***********************\n')
        if exec_type == 'streaming':
            pass
            # need to create the method that execute a continues time execution
            self.streaming()
            
        elif exec_type == 'time_specific':
            
            self.time_specific()
        elif exec_type == 'invoke':
            
            self.invoke()
        
        if self.allOutputs != None:
            for output in self.allOutputs:
                output.exchReady = True
        
    def time_specific(self,exeConf ={'type':'freq','value': 1,'unit':'s'})->None:
        # conf ={'type':'time','value': 1,'unit':'s'}
        iter = iter
        # t = 0
        t_sleep = self.timeconverter(unit=exeConf['unit'],value=exeConf['value'])
        # ExeModeIter
        
        exeComponents = self.exeComponents
       
        for component in exeComponents:
                if type(component) is Comm.Sink:
                    component.controller(command='start')
        #as long as it is not stopped
        time.sleep(self.delayTime)
        while self.stopTrigger.evaluate() == False: 
            for component in exeComponents:
                if type(component) is Comm.Sink:
                    print('\n')
                    print("component {} :".format(component.name)) 
                    component.push_data()
                elif type(component) is Comm.Model:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.runProcessing() 
                elif type(component) is Comm.ConfigComp:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.setParam()        
                else:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.behavior()
            if self.stop == True:
                break
            # time.sleep(t_sleep)
            # t +=t_step
            iter += 1
            print('\n')
            # print('time is:' + str(t) )
            print('iteration is:' + str(iter) )
            print('\n')
        for component in exeComponents:
            if type(component) is Comm.Source:
                component.controller(command='pause')
    
    def streaming(self)->None:
        """_summary_
        """
        exeComponents = self.exeComponents
        
        for component in exeComponents:
                if type(component) is Comm.Sink:
                    component.controller(command='start')
        time.sleep(self.delayTime)
        #as long as it is not stopped
        while self.stopTrigger.evaluate() == False: 
            for component in exeComponents:
                if type(component) is Comm.Sink:
                    print('\n')
                    print("component {} :".format(component.name)) 
                    component.push_data()
                elif type(component) is Comm.Model:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.runProcessing()    
                elif type(component) is Comm.ConfigComp:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.setParam()     
                else:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.behavior()
            if self.stop == True:
                break
            
            print('\n')
            # print('time is:' + str(t) )
            # print('iteration is:' + str(iter) )
            # print('\n')
        for component in exeComponents:
            if type(component) is Comm.Sink:
                component.controller(command='pause')
    
    def invoke(self)->None:
        exeComponents = self.exeComponents
        
        for component in exeComponents:
                if type(component) is Comm.Sink:
                    component.controller(command='start')
        #as long as it is not stopped
        time.sleep(self.delayTime)
        for component in exeComponents:
            if type(component) is Comm.Sink:
                print('\n')
                print("component {} :".format(component.name)) 
                component.push_data()
            elif type(component) is Comm.Model:
                print('\n')
                print("component {} :".format(component.name))
                component.runProcessing()  
            elif type(component) is Comm.ConfigComp:
                    print('\n')
                    print("component {} :".format(component.name))
                    component.setParam()       
            else:
                print('\n')
                print("component {} :".format(component.name))
                component.behavior()
            
            print('\n')
            # print('time is:' + str(t) )
            # print('iteration is:' + str(iter) )
            # print('\n')
        for component in exeComponents:
            if type(component) is Comm.Sink:
                component.controller(command='pause')
 

#simScheduling works
class compScheduling:
    
    def __init__(self, relationship_dict = {}, assumtion = [], title = 'Directed Graph', printFlag = True):
        
        self.relationships = relationship_dict
        if type(assumtion) == str:
            self.assumtion = [assumtion]
        elif type(assumtion) == list:
            self.assumtion = assumtion
        else:
            print('Please intrudce the assumption as a list, even if it has only one element or as an empty list')
        self.printFlag = printFlag
        
        #methods created for usage
        self.graph = self.create_directional_graph_wIndNodes(self.relationships)
        
        self.sccs = self.tarjans_algorithm(self.graph)
        self.cycleDetected = False
        
        
        for group in self.sccs:
            if len(group) > 1:
                self.cycleDetected = True
        
        if self.cycleDetected == False:
            self.topological_order = self.topological_sort(self.graph)
            self.new_graph = None
            self.cycle_topological_order = None
            self.cycleName= None
        else:
            self.new_graph = self.create_scc_encapsulated_graph(self.graph,self.sccs)
            self.topological_order = self.topological_sort(self.new_graph)
            self.cycle_topological_order = self.sort_cycle(self.graph,self.sccs,self.assumtion)
            self.cycleName= self.findCycleName(self.topological_order)
        
        self.title = title
        if printFlag == True:
            self.plot_directed_graph_wIndNodes(self.graph)
    
    def __str__(self):
        message = "Scheduling order suggested for the simulation components." + '\n' "Order is: " + '\n'
        index = 0
        for comp in self.topological_order:
            index += 1
            message = message + str(index) + ':' + comp + '\n'
        if self.cycleDetected:
            cycle_message = 'There is a cycle and its name as a component is ' + str(self.cycleName) + " its components' order is:" + '\n'
            for comp in self.cycle_topological_order:
                cycle_message += comp + '\n'

    def findCycleName(self, names)->list:
        cycleNames = []
        for name in names:
            if name.find('Cycle') != -1 :
                cycleNames.append(name)
        return cycleNames
    
    def create_directional_graph(self, relationship_dict) ->dict:
        directional_graph = {}

        for node, connections in relationship_dict.items():
            for target_node in connections:
                if target_node:
                    if target_node not in directional_graph:
                        directional_graph[target_node] = set()
                    directional_graph[target_node].add(node)
                if node not in directional_graph:
                    directional_graph[node] = set()

        return {node: list(edges) for node, edges in directional_graph.items()}
    
    def create_directional_graph_wIndNodes(self, relationship_dict):
        directional_graph = {}

        # Iterate through each node and its connections in the input dictionary
        for node, connections in relationship_dict.items():
            # Ensure the node itself is included in the directional graph
            if node not in directional_graph:
                directional_graph[node] = set()
            
            for target_node in connections:
                # Add the node to the adjacency list of the target node
                if target_node:
                    if target_node not in directional_graph:
                        directional_graph[target_node] = set()
                    directional_graph[target_node].add(node)

        # Add any nodes that are in the relationships as independent nodes if they are not present
        for node in relationship_dict:
            if node not in directional_graph:
                directional_graph[node] = set()

        # Convert sets to lists for consistency
        return {node: list(edges) for node, edges in directional_graph.items()} 
    
    def plot_directed_graph_wIndNodes(self,directional_graph):
        # Create a directed graph object
        G = nx.DiGraph()

        # Add nodes and edges from the directional graph dictionary
        for node, edges in directional_graph.items():
            for edge in edges:
                G.add_edge(node, edge)
            # Ensure the node itself is included in the graph
            if node not in G:
                G.add_node(node)

        # Ensure all nodes from the original graph are included, even if they have no edges
        all_nodes = set(directional_graph.keys())
        for node in all_nodes:
            if node not in G:
                G.add_node(node)

        # Draw the graph
        pos = nx.spring_layout(G)  # Position nodes using the spring layout
        plt.figure(figsize=(14, 7))
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue", alpha=0.5, linewidths=5)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

        # Draw edges with arrows separately to ensure each direction is represented
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True, arrowstyle='-|>', 
                            arrowsize=20, edge_color="red", connectionstyle='arc3,rad=0.2')

        plt.title(self.title)
        # plt.title("Directed Graph")
        plt.show()
    
    def plot_bidirected_graph(self, directional_graph):
        # Create a directed graph object
        G = nx.DiGraph()

        # Add nodes and edges from the directional graph dictionary
        for node, edges in directional_graph.items():
            for edge in edges:
                G.add_edge(node, edge)

        # Draw the graph
        pos = nx.spring_layout(G)  # Position nodes using the spring layout
        plt.figure(figsize=(10, 6))
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", 
                font_size=10, font_weight="bold", edge_color="gray", arrows=True, 
                arrowstyle='-|>', arrowsize=20)

        plt.title("Directed Graph")
        plt.show()

    def plot_directed_graph(self, directional_graph):
        # Create a directed graph object
        G = nx.DiGraph()

        # Add nodes and edges from the directional graph dictionary
        for node, edges in directional_graph.items():
            for edge in edges:
                G.add_edge(node, edge)

        # Draw the graph
        pos = nx.spring_layout(G)  # Position nodes using the spring layout
        plt.figure(figsize=(15, 9))
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue", alpha= 0.5, linewidths=5)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

        # Draw edges with arrows separately to ensure each direction is represented
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True,arrowstyle='-|>', 
                            arrowsize=20, edge_color="red", connectionstyle='arc3,rad=0.2')

        plt.title("Directed Graph")
        plt.show()
   
    def tarjans_algorithm(self, directional_graph)->list:
        index = 0
        stack = []
        indices = {}
        lowlink = {}
        on_stack = {}
        sccs = []

        def strongconnect(node):
            nonlocal index
            indices[node] = index
            lowlink[node] = index
            index += 1
            stack.append(node)
            on_stack[node] = True

            for neighbor in directional_graph.get(node, []):
                if neighbor not in indices:
                    strongconnect(neighbor)
                    lowlink[node] = min(lowlink[node], lowlink[neighbor])
                elif on_stack[neighbor]:
                    lowlink[node] = min(lowlink[node], indices[neighbor])

            if lowlink[node] == indices[node]:
                scc = []
                while True:
                    w = stack.pop()
                    on_stack[w] = False
                    scc.append(w)
                    if w == node:
                        break
                sccs.append(scc)

        for node in directional_graph:
            if node not in indices:
                strongconnect(node)
        return sccs
    
    def topological_sort(self, directional_graph)->list:
        visited = set()
        stack = []

        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for neighbor in directional_graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(node)

        for node in directional_graph:
            if node not in visited:
                dfs(node)

        return stack[::-1]
    
    def create_scc_encapsulated_graph(self,directional_graph, sccs)->dict:
        # Create a mapping from nodes to their SCC index
        node_to_scc = {}
        for idx, scc in enumerate(sccs):
            for node in scc:
                node_to_scc[node] = f"Cycle{idx}" if len(scc) > 1 else node
        
        # Initialize the new graph
        new_graph = {scc_id: set() for scc_id in node_to_scc.values()}

        # Populate the new graph
        for node, neighbors in directional_graph.items():
            node_scc = node_to_scc[node]
            for neighbor in neighbors:
                neighbor_scc = node_to_scc[neighbor]
                if node_scc != neighbor_scc:
                    new_graph[node_scc].add(neighbor_scc)

        # Convert sets to lists for consistency
        new_graph = {k: list(v) for k, v in new_graph.items()}

        return new_graph
    
    def sort_cycle(self, directional_graph,sccs,assumption)->list:
        if assumption == []:
            assumption = list(self.relationships.keys())[0]
        else:
            assumption = assumption[0]
            
        for group in sccs:
            if len(group) != 1:
                cycle_comp = group
        cycle_directional_graph = {}
        for name, dependencies in directional_graph.items():
            new_dependency = []
            for comp in dependencies:
                if comp != assumption and comp in cycle_comp:
                    new_dependency.append(comp)
            if name in cycle_comp:
                cycle_directional_graph[name] = new_dependency
        
                
        cycle_order = self.topological_sort(cycle_directional_graph)
        # print(cycle_directional_graph)
        return(cycle_order)

#it works
class loop:
    
    def __init__(self, cycleName = 'Loop',cycleCompNames = [], areaCompSchedule = [], exeComponents = [],
                 exeType = "UserSchedule", relationships = {},assumption = {'Gain_model':[{'name':'temp_in','value': 50},
                                                 {'name':'mass_in','value': 12},
                                                 {'name':'vol_in','value': 3.15}]},):
        self.cycleComp = cycleCompNames
        
        #for loop name 
        modNames = ''
        for comp in self.cycleComp:
            modNames = modNames + comp[0]
        if type(cycleName) == list:
            self.name = cycleName[0]
        elif type(cycleName) == str:
            self.name = cycleName
        else:
            print('error in input CycleName')
            self.name = 'Loop' + str(len(self.cycleComp)) + modNames
               
        self.compSchedule = areaCompSchedule
        self.allComponents = exeComponents
        
        self.exeType = exeType
        self.assumption = assumption
        
        self.cycleSchedule = self.cycleComp
        self.exeCompCycle = []
        
        for schComp  in self.cycleSchedule:
            for exeComp in self.allComponents:
                if exeComp.name == schComp:
                    self.exeCompCycle.append(exeComp)
                    break
        self.relationships = relationships
        self.inputsFromConnXcomp,self.loopExInputs = self.inputAnalysis()
        self.outputsToConnXcomp,self.loopExOutputs = self.outputAnalysis()

        # self.inputsFromConnXcomp = self.inputsInCycle()
        # self.outputsToConnXcomp = self.outputsInCycle()
        
    def __str__(self):
        message = 'Loop with ' + str(len(self.cycleComp)) + 'components'  
        message2 = '\n' + 'components are:\n'
        message3 = ''
        for component in self.cycleSchedule:
            message3 = message3 +component + '\n'
            
        
        return message + message2 + message3 
    
    def inputAnalysis(self)->tuple:
        allAppComp = []
        for comp in self.allComponents:
            allAppComp.append(comp.name)
        loopCompNames = self.cycleComp

        inputsFromConnXcomp = {}
        loopExInputs ={}
        # outputsToConnXcomp ={}
        # loopExOutputs ={}
        relationships= self.relationships

        #extract inputs from each component contained in the loop others put it in a other dict from relationshipw
        for component, rel in relationships.items():
            compInputsIn = []
            compInputsOut = []
            if component in loopCompNames:
                for comp,inputs in rel.items():
                    if comp in loopCompNames:
                        # print('Component is:' + comp)
                        # print('inputs are '+ str(inputs))
                        compInputsIn += inputs
                        inputsFromConnXcomp[component] = compInputsIn
                    else:
                        compInputsOut += inputs
                        loopExInputs[component] = compInputsOut 
        return inputsFromConnXcomp,loopExInputs
    
    def outputAnalysis(self)-> tuple:
        allAppComp = []
        for comp in self.allComponents:
            allAppComp.append(comp.name)
        loopCompNames = self.cycleComp

        # inputsFromConnXcomp = {}
        # loopExInputs ={}
        outputsToConnXcomp ={}
        loopExOutputs ={}
        # relationships= self.relationships
        
        #extract outputs from each component contained in the loop others put it in a other dict from the components themself
        # outputsToConnXcomp ={}
        components =  self.exeCompCycle
        # print(components)
        loopCompNames = self.cycleComp
        compNames = []
        for comp in components:
            compNames.append(comp.name)
            
        for component in components: 
            # print(component.outports)
            # if component.name in loopCompNames:
            #     outputsToConnXcomp[component.name] =[]
            # else:
            #     loopExOutputs[component.name] =[] 
            compOutputsIn = []
            compOutputsOut = []  
            for outportID,port in component.outports.items():
                    componentDst = port.connector.dst['component'].name
                    # print('Origin port is:' + component.name)
                    # print('Destination is:' + componentDst)
                    # print('Port Name: ' + port.name)
                    if componentDst in loopCompNames:
                        # print("BELONGS TO LOOP"+ '\n')
                        compOutputsIn.append(port.name) 
                        # print(outputsToConnXcomp)
                        # print(compOutputsIn)
                        # print('\n')
                    else:
                        # print("OUT OF TO LOOP" + '\n')
                        compOutputsOut.append(port.name)
                    if compOutputsIn != []:
                        outputsToConnXcomp[component.name] = compOutputsIn
                    if compOutputsOut != []:
                        loopExOutputs[component.name] = compOutputsOut
                    # print(outputsToConnXcomp)
        return outputsToConnXcomp, loopExOutputs
            
    def outputsInCycle (self) -> dict:
        
        Componets_outputs ={}
        components =  self.exeCompCycle
        compNames = []
        for comp in components:
            compNames.append(comp.name)
            
        for component in components: 
            Componets_outputs[component.name] =[]
            for outportID,port in component.outports.items():
                    componentDst = port.connector.dst['component'].name
                    if componentDst in compNames:
                        Componets_outputs[component.name].append(port.name) 
        return Componets_outputs

    def inputsInCycle (self) -> dict:
        
        Componets_inputs ={}
        components =  self.exeCompCycle
        compNames = []
        for comp in components:
            compNames.append(comp.name)
            
        for component in components: 
            Componets_inputs[component.name] =[]
            for inportID,port in component.inports.items():
                    componentSrc = port.connector.src['component'].name
                    if componentSrc in compNames:
                        Componets_inputs[component.name].append(port.name)    
        return Componets_inputs
    
    def solve(self, simType = 'time_based',schedule = [], iter = 0)->None:
        """_summary_
            It solves an algebraic loop using the simpliest solution. 
            defines which solution will follow depending on the simulation type
        Args:
            simType (str, optional): _description_. Defaults to 'time_based' or 'simulation'.
            
            schedule (list, optional): _description_. Defaults to [].
            iter (int, optional): _description_. Defaults to 0.
        """
        
        if simType == 'time_based':
            self.timeBasedsolution(schedule=schedule,iter=iter)
        elif simType == 'simulation':
            self.simulation(schedule=schedule,iter=iter)
        else:
            print('Simulation type (simType): ' + simType + ' is not supported')
    
    def timeBasedsolution(self, schedule = [], iter = 0)->None:
        """_summary_
            It solves an algebraic loop using the simpliest solution for a time based implementation
        Args:
            type (str, optional): _description_. Defaults to "UserSchedule" or "Automatic"

        Returns:
            object: _description_
        """
        inputsFromConnXcomp = self.inputsFromConnXcomp
        loopInputs = self.loopExInputs
        outputsToConnXcomp = self.outputsToConnXcomp
        loopOutputs = self.loopExOutputs
        if schedule == []:
            # schedule =  exeArea.exeCompCycle
            schedule =  self.exeCompCycle
            print('\nRunning loop iteration:'+ str(iter))
            tempList = []
            tempDict = {}
            inputsFromConn_init = []
            
            
            if self.assumption == {}:
                #if there is no assumption the initial value of the first element of the 
                # cycle will come from the connection. 
                ExeModeIter = 'Initial'
                for id, input in schedule[0].inputs.items():
                    tempDict['name'] = input['name']
                    tempDict['value'] = 'connection'
                    # print(tempDict)
                    tempList.append(tempDict)
                    # print(tempList)
                    tempDict ={}
                self.assumption[schedule[0].name] = tempList
            else:
                ExeModeIter = 'Live'
            
            
            if self.exeType == "UserSchedule":
                # actual implementation of loop solving using an usershedule type
                # this solution is simple assuming an initial value of the fist element to be simulated
                # either the value come from user (if there is a value in self.assuption)
                # or the assumption is taken from the connection. This loop solution only 
                # execute once... no iterative solution is needed. 
                
                maxIter = 1
                if iter == 0: #the iteration comes from the execution of the steps, a second step
                    # would become iteration number 1, then this solution will get its values always 
                    # from the connections since the previous iteration generated already a valid value
                    model_assumtion = list(self.assumption.keys())[0]
                    
                    
                    if model_assumtion != schedule[0].name:
                        # just making sure the assumption decided is from the first element that will be executed
                        # within the loop
                        print('Error the assumption must content values for the first element on the schedule of execution')
                        print('First element for execution is: ' + schedule[0].name)
                        return 0
                    
                    changes = list(self.assumption.values())[0]
                    # the following introduce the values of the assumtion to the port. 
                    # if it they come from the connection then only creates a dictionary with the names
                    # of the inputs so the run_step method acquire that data from the connection
                    for change in changes:
                        if change['value'] == 'connection':
                            print(change['name'] + " comes from connection")
                            inputsFromConn_init.append(change['name'])
                        else:
                            schedule[0].Port_update(type = 'input', port_update = change)
                for component in schedule:
                    # this is the actual execution of each component considering their 
                    inputsComp = inputsFromConnXcomp[component.name]
                    outputsComp = outputsToConnXcomp[component.name]
                    if type(component) is Comm.Model:
                        print('\n')
                        print("component {} :".format(component.name))
                        
                        if iter == 0 and schedule.index(component) == 0:
                            component.runStep(ExeMode = ExeModeIter,inputsFromConn = inputsFromConn_init,outputsToConn=outputsComp)  
                            # component.runStep(ExeMode = ExeModeIter,inputsFromConn = inputsFromConn_init)                  
                        else:
                            component.runStep(inputsFromConn=inputsComp, outputsToConn=outputsComp)          
                    else:
                        print('\n')
                        print("component {} :".format(component.name))
                        component.behavior(inputsFromConn=inputsComp, outputsToConn=outputsComp)
                
                edgeComponents = list(loopOutputs.keys())
                # maybe not needed to pause depending on implementation of area execution
                for component in schedule:
                    if type(component) is Comm.Model:
                        print("component {} has been paused".format(component.name))
                        component.pause()
                    # this makes sure that after paussing the execution of models and components
                    # all the values in the edge componets (components with connections outside the loop)
                    # send that value to the connector.
                    if component.name in edgeComponents:
                        name = component.name
                        outputs2update = loopOutputs[name]
                        component.outport_assigment(outputs2update)
    
    def simulation(self, schedule = [], iter = 0)->None:
        """_summary_
            It solves an algebraic loop using the simpliest solution for a time based implementation
        Args:
            type (str, optional): _description_. Defaults to "UserSchedule" or "Automatic"

        Returns:
            object: _description_
        """
        inputsFromConnXcomp = self.inputsFromConnXcomp
        loopInputs = self.loopExInputs
        outputsToConnXcomp = self.outputsToConnXcomp
        loopOutputs = self.loopExOutputs
        if schedule == []:
            # schedule =  exeArea.exeCompCycle
            schedule =  self.exeCompCycle
            print('\nRunning loop iteration:'+ str(iter))
            tempList = []
            tempDict = {}
            inputsFromConn_init = []
            
            
            if self.assumption == {}:
                #if there is no assumption the initial value of the first element of the 
                # cycle will come from the connection. 
                ExeModeIter = 'Initial'
                for id, input in schedule[0].inputs.items():
                    tempDict['name'] = input['name']
                    tempDict['value'] = 'connection'
                    # print(tempDict)
                    tempList.append(tempDict)
                    # print(tempList)
                    tempDict ={}
                self.assumption[schedule[0].name] = tempList
            else:
                ExeModeIter = 'Live'
            
            
            if self.exeType == "UserSchedule":
                # actual implementation of loop solving using an usershedule type
                # this solution is simple assuming an initial value of the fist element to be simulated
                # either the value come from user (if there is a value in self.assuption)
                # or the assumption is taken from the connection. This loop solution only 
                # execute once... no iterative solution is needed. 
                
                maxIter = 1
                if iter == 0: #the iteration comes from the execution of the steps, a second step
                    # would become iteration number 1, then this solution will get its values always 
                    # from the connections since the previous iteration generated already a valid value
                    model_assumtion = list(self.assumption.keys())[0]
                    
                    
                    if model_assumtion != schedule[0].name:
                        # just making sure the assumption decided is from the first element that will be executed
                        # within the loop
                        print('Error the assumption must content values for the first element on the schedule of execution')
                        print('First element for execution is: ' + schedule[0].name)
                        return 0
                    
                    changes = list(self.assumption.values())[0]
                    # the following introduce the values of the assumtion to the port. 
                    # if it they come from the connection then only creates a dictionary with the names
                    # of the inputs so the run_step method acquire that data from the connection
                    for change in changes:
                        if change['value'] == 'connection':
                            print(change['name'] + " comes from connection")
                            inputsFromConn_init.append(change['name'])
                        else:
                            schedule[0].Port_update(type = 'input', port_update = change)
                for component in schedule:
                    # this is the actual execution of each component considering their 
                    inputsComp = inputsFromConnXcomp[component.name]
                    outputsComp = outputsToConnXcomp[component.name]
                    if type(component) is Comm.Model:
                        print('\n')
                        print("component {} :".format(component.name))
                        
                        if iter == 0 and schedule.index(component) == 0:
                            component.simulate(ExeMode = ExeModeIter,inputsFromConn = inputsFromConn_init,outputsToConn=outputsComp)  
                            # component.runStep(ExeMode = ExeModeIter,inputsFromConn = inputsFromConn_init)                  
                        else:
                            component.simulate(inputsFromConn=inputsComp, outputsToConn=outputsComp)          
                    else:
                        print('\n')
                        print("component {} :".format(component.name))
                        component.behavior(inputsFromConn=inputsComp, outputsToConn=outputsComp)
                
                edgeComponents = list(loopOutputs.keys())
                # maybe not needed to pause depending on implementation of area execution
                for component in schedule:
                    if type(component) is Comm.Model:
                        print("component {} has been paused".format(component.name))
                        component.pause()
                    # this makes sure that after paussing the execution of models and components
                    # all the values in the edge componets (components with connections outside the loop)
                    # send that value to the connector.
                    if component.name in edgeComponents:
                        name = component.name
                        outputs2update = loopOutputs[name]
                        component.outport_assigment(outputs2update)
            