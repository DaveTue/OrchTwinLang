from src.API.comm_protos.TCP import TCPServer as Server
from src.API.comm_protos.TCP import TCPClient as Client
import json
import os
import csv
import importlib

# from comm_protos.TCP import TCPServer as Server
# from comm_protos.TCP import TCPClient as Client

class Sensor:
    
    def __init__(self, comm_proto = 'TCP-IP', 
                    name  = 'tilt', config = {"type" : "freq", "unit": "s", "occurrences_per_unit":20},
                    sending_port = 55000, receiving_ports = [55001], outputsNames = ['temp']) -> None:
                
        self.comm_proto = comm_proto
        self.name =  name
        self.sending_port = sending_port
        self.receiving_ports =  receiving_ports
        
        self.outputsNames =  outputsNames
        self.output2Port = {}    
        
        self.config = config # can only be define in times per minute
        self.server = ''
        self.client = ''
        self.outputs ={}
        self.directory = 'D:\\Git_folders\\projects_app\\LOTTS\\sensors'
        self.portDefinition()
        # self.initialize_comm()
                
    def __str__(self) -> str:
            msg_model = "Sensor name: " + self.name
            msg_output =  '     The outputs of this sensor are: ' + self.outputs
            return msg_model + '\n' + msg_output    
    
      
    def portDefinition(self, outputs = [])-> None:
        """_summary_
        this method defines all outputs that a sensor has, the outputs should be a user defined.
        and should correlate the outputname with the corresponding port

        Args:
             outputs (list, optional): _description_. Defaults to ['name'].

        Returns:
            _type_: _description_
        """
        if outputs != []:
            self.outputsNames = outputs
        
        elements = len(self.outputsNames) 
        
        self.outputs ={name: 0 for name in self.outputsNames}
        
        for i in range(elements):
            self.output2Port[self.outputsNames[i]] = self.receiving_ports[i]      
        
    
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
            
            self.client = Client("127.0.0.1", send_port = self.sending_port, receive_ports = self.receiving_ports)
            self.client.connect()
            # print(self.client)
            return(self.client)

    def get_output(self, var_name,client)-> str:
        """_summary_
            this method checks the client object to get the outputs from the sensor
        Args:
            var_name (_type_): _description_

        Returns:
            str: _description_
        """
        name = str(var_name)
        port = self.output2Port[name]
        # print(port)
        # print(client.message_received[port])
        # datadict = json.loads(self.client.message_received[port])
        datadict = json.loads(client.message_received[port])
        self.outputs[name] = datadict['msg']
        # output_val = self.model.__getattribute__(var_name)   
        # self.outputs[name] = self.model.__getattribute__(var_name)   
        return self.outputs[name]
    
    def resume(self,client)-> None:
        command = 'resume'
        message = json.dumps({'command':command})
        client.send_message(message)
        # self.client.send_message(message)
        
    def pause(self,client)-> None:
        # message = 'pause'
        command = 'pause'
        message = json.dumps({'command':command})
        # self.client.send_message(message)
        client.send_message(message)
    
    def start(self,client)-> None:
        
        # message = 'start'
        command = 'start'
        message = json.dumps({'command':command})
        # self.client.send_message(message)
        client.send_message(message)
    
    def stop(self, client)-> None:
        # message = 'stop'
        command = 'stop'
        message = json.dumps({'command':command})
        # self.client.send_message(message)
        client.send_message(message)
   
    def set_config(self, client, config = {})->None:
        
        if config == {}:
            config = self.config
            
        message = json.dumps({'config':config})
        client.send_message(message)
        # self.client.send_message(message)    
         
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
            # writer.writerow(['inputsNames', ','.join(self.inputsNames)])
            writer.writerow(['outputsNames', ','.join(f'{o}' for o in self.outputsNames)])
            writer.writerow(['sending_port', self.sending_port])
            writer.writerow(['receiving_ports', ','.join(f'{p}' for p in self.receiving_ports)])
            # writer.writerow(['parametersNames', ','.join(self.parametersNames)])
            writer.writerow(['config', ','.join(f"{k}:{v}" for k, v in self.config.items())])
            writer.writerow(['name', self.name])
            # writer.writerow(['model', self.model.__class__.__module__ + '.' + self.model.__class__.__name__])
            

    @classmethod
    def load_from_csv(cls, name, directory):
        """Load data from a CSV file in the specified directory and create an instance of pythonEncap."""
        file_name = name + '.csv'
        if directory == '':
            directory = 'D:\\Git_folders\\projects_app\\dsl-orchestration\\sensors'
        file_path = os.path.join(directory, file_name)

        data = {}
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                key, value = row
                # print(value)
                if  key == 'outputsNames': # or key == 'receiving_ports':
                    data[key] = [o for o in  value.split(',')]
                    
                elif key == 'config':
                    data[key] = {str(k): v for k, v in (item.split(':') for item in value.split(','))}
                elif key == 'receiving_ports' :
                    data[key] = [int(p) for p in  value.split(',')]
                # elif key == 'model':
                #     # Use the model factory to recreate the model
                #     data[key] = cls.model_factory(value)
                else:
                    data[key] = value

        # Create and return an instance of pythonEncap
        
        return cls(
            # model=data['model'],
            name=data['name'],
            receiving_ports=data['receiving_ports'],
            outputsNames=data['outputsNames'],
            # parametersNames = data['parametersNames'],
            config=data['config']
            # directory=directory
        )
        
    
    @staticmethod
    def model_factory(model_name):
        """Factory method to recreate a model object by its class name."""
        module_name, class_name = model_name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        model_class = getattr(module, class_name)
        return model_class()
       
