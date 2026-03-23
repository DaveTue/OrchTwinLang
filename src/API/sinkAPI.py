# from API.comm_protos.TCP import TCPServer as Server
from src.API.comm_protos.TCP2 import TCPClient as Client
import json
import os
import csv

# from comm_protos.TCP import TCPServer as Server
# from comm_protos.TCP import TCPClient as Client

class Sink:
    def __init__(self, comm_proto = 'TCP-IP', 
                    name  = 'tilt', config = {"type" : "freq", "unit": "s", "occurrences_per_unit":1},
                    instruction_port = 60000, sending_ports=[60001,60002,60003,60004,60005],  
                    inputsNames = ['temperature','sg','simTime','real_temperature', 'real_sg']) -> None:
                
        self.comm_proto = comm_proto
        self.name =  name
        self.sending_ports = sending_ports
        self.receiving_ports =  [60500]
        self.instruction_port = instruction_port
        
        
        self.inputsNames =  inputsNames
        
        self.inputs2ports = {name:port for name, port in zip(self.inputsNames, sending_ports)}    
        
        self.config = config # can only be define in times per minute
        self.server = ''
        self.client = ''
        self.inputs ={}
        self.directory = 'D:\\Git_folders\\projects_app\\LOTTS\\sensors'
        self.portDefinition()
        # self.initialize_comm()
                
    def __str__(self) -> str:
            msg_model = "Sink name: " + self.name
            msg_output =  '     The inputs of this sink are: ' + self.inputsNames
            return msg_model + '\n' + msg_output    
    
      
    def portDefinition(self, inputs = [])-> None:
        """_summary_
        this method defines all inputs that a sink has, the inputs should be a user defined.
        and should correlate the outputname with the corresponding port

        Args:
             outputs (list, optional): _description_. Defaults to ['name'].

        Returns:
            _type_: _description_
        """
        if inputs != []:
            self.inputsNames = inputs
        
        # elements = len(self.inputsNames) 
        
        self.inputs ={name: 0 for name in self.inputsNames}
        
        # for i in range(elements):
        #     self.inputs2ports[self.inputsNames[i]] = self.receiving_ports[i]      
        
    
    def initialize_comm(self)-> None:
            """_summary_
            This initialize the server and client for the TCP-IP communication protocol
            
            """
            # ports = []
            # ports.append(self.sending_port)
            # ports = ports + self.receiving_ports 
            # port_pairs = [(sending_port,receiving_port)]

            # self.server = Server(ports)
            # self.server.start_server()
            
            self.client = Client("127.0.0.1", send_ports = self.sending_ports + [self.instruction_port], receive_ports = [self.instruction_port])
            self.client.connect()
            return self.client
        
    
    def set_input(self, var_name = 'temperature', value = [],client = None )-> None:
        """This method send the desire value to the desire port, the values can be of time 
        list. 

        Args:
            var_name (str, optional): _description_. Defaults to 'temperature'.
            value (list, optional): _description_. Defaults to [].
        """
        name  = str(var_name)
        port = self.inputs2ports[name]
        if value == []:
            value = 0
        self.inputs[name] = value
        rawData = {'msg':value}
        message = json.dumps(rawData)
        client.send_message(port = port,message=message)
        # self.client.send_message(port = port,message=message)
     
    def resume(self,client)-> None:
        command = 'resume'
        message = json.dumps({'command':command})
        client.send_message(port = self.instruction_port,message=message)
        # self.client.send_message(port = self.instruction_port,message=message)
        
    def pause(self,client)-> None:
        # message = 'pause'
        command = 'pause'
        message = json.dumps({'command':command})
        client.send_message(port = self.instruction_port,message=message)
        # self.client.send_message(port = self.instruction_port,message=message)
    
    def start(self,client)-> None:
        
        # message = 'start'
        command = 'start'
        message = json.dumps({'command':command})
        print(message)
        print(message)
        client.send_message(port = self.instruction_port,message=message)
        # self.client.send_message(port = self.instruction_port,message=message)
    
    def stop(self,client)-> None:
        # message = 'stop'
        command = 'stop'
        message = json.dumps({'command':command})
        client.send_message(port = self.instruction_port,message=message)
        # self.client.send_message(port = self.instruction_port,message=message)
   
    def set_config(self, config = {},client =  None)->None:
        
        if config == {}:
            config = self.config
            
        message = json.dumps({'config':config})
        client.send_message(port = self.instruction_port,message=message)   
        # self.client.send_message(port = self.instruction_port,message=message)   
            
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
            
            writer.writerow(['inputsNames', ','.join(f'{o}' for o in self.inputsNames)])
            writer.writerow(['instruction_port', self.instruction_port])
            writer.writerow(['sending_ports', ','.join(f'{p}' for p in self.sending_ports)])
            # writer.writerow(['parametersNames', ','.join(self.parametersNames)])
            writer.writerow(['config', ','.join(f"{k}:{v}" for k, v in self.config.items())])
            writer.writerow(['name', self.name])
            
            # name  = 'tilt', 
            # config = {"type" : "freq", "unit": "s", "occurrences_per_unit":1},
            # instruction_port = [60000], 
            # send_ports=[60001,60002,60003,60004,60005],  
            # inputsNames = ['temperature','sg','simTime','real_temperature', 'real_sg']

    @classmethod
    def load_from_csv(cls, name, directory):
        """Load data from a CSV file in the specified directory and create an instance of pythonEncap."""
        file_name = name + '.csv'
        if directory == '':
            directory =  'D:\\Git_folders\\projects_app\\dsl-orchestration\\sensors'
        file_path = os.path.join(directory, file_name)

        data = {}
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                key, value = row
                # print(value)
                if  key == 'inputsNames': # or key == 'receiving_ports':
                    data[key] = [o for o in  value.split(',')]
                    
                elif key == 'config':
                    data[key] = {str(k): v for k, v in (item.split(':') for item in value.split(','))}
                elif key == 'sending_ports': #or key == 'instruction_port':
                    data[key] = [int(p) for p in  value.split(',')]
                # elif key == 'model':
                #     # Use the model factory to recreate the model
                #     data[key] = cls.model_factory(value)
                elif key == 'instruction_port':
                    data[key] = int(value)
                else:
                    data[key] = value

        # Create and return an instance of pythonEncap
        
        return cls(
            # model=data['model'],
            name=data['name'],
            instruction_port=data['instruction_port'],
            sending_ports=data['sending_ports'],
            inputsNames=data['inputsNames'], 
            config=data['config']
            # directory=directory
        )
        