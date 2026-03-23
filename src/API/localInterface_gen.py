#MatLabTests
import sys
import matlab.engine
import time
import os
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import shutil
from operator import itemgetter

class interfaceFile_gen:
    def __init__(self, file_name = "s_function_new", input_num = 1, output_num = 1, 
                 function_name = "func_interface",name_input_var = [], name_output_var=[],
                 template = 'S_functionbased.txt', directory = os.getcwd() ):

        self.file_name= file_name
        self.template = template #The name of the Simulink Model 
        self.directory = directory #directory of the model
        self.input_num = str(input_num)
        self.output_num = str(output_num) 
        self.function_name = function_name
        self.name_input_var = name_input_var
        self.name_output_var = name_output_var
       
    def generate(self):
        # Using readlines()
        path_template = os.getcwd() + '\\'+ 'support_files' + '\\' + self.template #consider maybe changing the path of the template
        file = open(path_template,'r')
        #file = open(self.template, 'r') #works for current file
        Lines = file.readlines()
        file.close()
        final_s_function_name = self.file_name + ".m"
        path_target = self.directory + '\\' + final_s_function_name
        input_dict = {}
        output_dict ={}
        #with open (final_s_function_name,"w") as f_w: #works with current path
        with open(path_target,'w') as f_w:
            count = 0
            # Strips the newline character
            loop_flag = False
            input_flag = False
            output_flag = False
            for line in Lines:
                new_line = line
                count += 1
                #print(line.find("[function_name]"))
                
                if '[function_name]' in new_line:
                    new_line = new_line.replace('[function_name]',self.function_name)
                
                if '[input_num]' in new_line:
                    new_line = new_line.replace('[input_num]',self.input_num)

                if '[output_num]' in new_line:
                    new_line = new_line.replace("[output_num]", self.output_num)

                if '[init_input_loop]' in new_line:
                    #new_line = new_line.replace('[init_input_loop]','#[init_input_loop]')
                    loop_flag = True
                    rep_num = int(self.input_num)
                    input_flag = True
                     
                elif '[init_output_loop]' in new_line:
                    #new_line = new_line.replace('[init_output_loop]','#[init_output_loop]')
                    loop_flag = True
                    rep_num = int(self.output_num)
                    output_flag = True
                
                if '[end_input_loop]' in new_line:
                    #new_line = new_line.replace('[end_input_loop]','#[end_input_loop]')
                    loop_flag = False
                    input_flag = False
                elif '[end_output_loop]' in new_line:
                    #new_line = new_line.replace('[end_output_loop]','#[end_output_loop]')
                    loop_flag = False
                    output_flag = False
                
                if loop_flag == True:

                    for i in range(0,rep_num):
                        new_line = line
                        new_line = new_line.replace("[i]",str(i+1))
                        #name_dict = str(i+1)
                        id_port = str(i+1)
                        if input_flag == True:
                            new_line = new_line.replace('[name_input_var]', self.name_input_var[i])
                            str_name_port = str(self.name_input_var[i])
                            input_dict[str_name_port] = id_port
                            '''
                            temp_dict = {name_dict: self.name_input_var[i] }
                            if temp_dict not in input_dict:
                                input_dict.append(temp_dict)
                            '''
                        elif output_flag == True:
                            new_line = new_line.replace('[name_output_var]', self.name_output_var[i])
                            str_name_port = str(self.name_output_var[i])
                            output_dict[str_name_port] = id_port
                            '''
                            temp_dict = {name_dict: self.name_output_var[i]}
                            if temp_dict not in output_dict:
                                output_dict.append(temp_dict)
                            '''
                            
                            
                        f_w.write(new_line)
                            
                #print("Line{}: {}".format(count, line))
                if loop_flag == False:
                    f_w.write(new_line)
        print("file " + final_s_function_name + " created" )
        ports_dictionary = dict(inputs = input_dict, outputs = output_dict )
        return ports_dictionary
class model_inspection:
    def __init__(self, model_name = "Gain_model", directory = os.getcwd() , folder_name = "Gain_model"):
        self.model_name =  model_name
        self.directory = directory
        self.folder_name =  folder_name
    
    def unzipped(self):
        # importing the zipfile module
        
        path_original_file = self.directory + '\\' + self.model_name + ".slx"
        path_folder = self.directory + '\\' + self.folder_name
        # loading the temp.zip and creating a zip object
        print('original file path and name:' + path_original_file)
        print('new folder:' + path_folder)
        with ZipFile(path_original_file, 'r') as zObject:
        
            # Extracting all the members of the zip 
            # into a specific location.
            zObject.extractall(path_folder)
        print("unzipped file from matlab")
    
    def extract(self):
        #limitation can not hanlde branches in simulink
        #all inports and outputs are conceptualized from the point of view of the model, for the s-function are the otherway around
        xml_file_path= self.directory + '\\' + self.folder_name + '\\simulink\\graphicalInterface.xml'
        xml_file_path_connections= self.directory + '\\' + self.folder_name + '\\simulink\\systems\\system_root.xml'
        print(xml_file_path)

        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        tree_conn=ET.parse(xml_file_path_connections)
        root_connec=tree_conn.getroot()
       
        inports_names = []
        outports_names = []
        for inport in root.iter('Inport'):
            inports_names.append(inport.attrib['Name'])
        for  outport in root.iter('Outport'):
            outports_names.append(outport.attrib['Name'])
      
        #elements_connect = [elem.tag for elem in root_connec.iter()]
        
        input_data = {}
        output_data = {}
        all_blocks = {}
        
        for block in root_connec.iter('Block'):
            if block.attrib['BlockType'] == 'Inport':    
                input_data [block.attrib['SID']] = block.attrib['Name']
            elif block.attrib['BlockType'] == 'Outport':
                output_data[block.attrib['SID']]=block.attrib['Name']
                
            all_blocks[block.attrib['SID']]=block.attrib['Name']
            
           
        connections = []

        temp_dict = {}
        input_Ids = list(input_data.keys())
        outputs_Ids = list(output_data.keys())
        for connection in root_connec.iter('Line'):
            #print(connection)
            flag_input_source = False
            for connect_component in connection:
                #print(connect_component.attrib)#how to deal with branches in simulink? 
                if connect_component.attrib['Name'] == 'Src':
                    src = connect_component.text.rsplit('#')[0]#modify by
                    #src_id = connect_component.text.rsplit('#out:')[1]
                if connect_component.attrib['Name'] == 'Dst':
                    dst = connect_component.text.rsplit('#')[0]
                    #dst_id = connect_component.text.rsplit('#in:')[1]
            if src in input_Ids or dst in outputs_Ids:
                temp_dict = dict(src = all_blocks[src], dst = all_blocks[dst])
                #temp_dict = dict(src = [all_blocks[src],src_id], dst = [all_blocks[dst],dst_id])
            if temp_dict not in connections:
                connections.append(temp_dict)

        ports_data = dict(inports = inports_names,outports = outports_names,connections = connections)    

        #print(connections)

        print("Data for input, outputs and its connections collected")
                #connections.append(simulink_connection())
                #print(connect_component.tag, connect_component.attrib, connect_component.text)
        return ports_data

class model_copy:
    def __init__(self, model_name = "Gain_model.slx", directory = os.getcwd() ):
        self.model_name = model_name
        self.directory = directory

    def copy_file(self):
        original_path = self.directory + "\\" + self.model_name
        clean_name_model = self.model_name.rsplit('.slx')[0]
        new_name_path = self.directory + "\\" + clean_name_model + "_wI.slx"


        shutil.copyfile(original_path, new_name_path)
        print('Model:' + self.model_name + " copied as " + clean_name_model + "_wI.slx" + " in folder:" + self.directory)
        new_modelName = clean_name_model + "_wI"
        folder = self.directory
        return[new_modelName,folder]

#trial1=interfaceFile_gen(file_name = 'S_function_new_4', input_num = 3, output_num = 2, function_name = "func_interface",name_input_var = ["in_1","in_2","in_3"], name_output_var=["out_1","out_2"])
#trial1.generate()
########{}
#text = "assignin('base','[name_output_var]',output_var_[i]);"
#text_new = text.replace('[i]','2')
#print(text_new)
#text_new = text_new.replace('[name_output_var]','blocky')
#print(text_new)
#######}
#test_zip = model_inspection()
#test_zip.unzipped()
#data = test_zip.extract()
#print(data)
#print(data['inports'])
#print(len(data['inports']))
#test_copy = model_copy()
#test_copy.copy_file()