# data processing example



class TiltSens:
    
    def __init__(self, rawTemperature = ['tilt', '18', '7/9/2022 20:19', '{"temp": 37.78, "gravity": 1070}'], 
                 rawSg = ['tilt', '18', '7/9/2022 20:19', '{"temp": 37.78, "gravity": 1070}'],
                 param = {})->None:
    # def __init__(self, temperature = 20, CO2 = 15, sg = 1.05 , temp_H2O = 18, 
                #  param = {})->None:
        self.rawTemperature = rawTemperature
        self.rawSg = rawSg
        # self.CO2 = CO2
        # self.temp_H2O = temp_H2O
        #units of parameters are PM_sug in g/mol and density in kg/L (density is assume equal to water)
        self.param= param
        #outputs
        self.sug_conc = 0
        self.temp = 0
        self.sg = 1
        self.temp_hystory = []
        self.sg_hystory = []
        self.sug_conc_hystory =[]
        self.ABV_hys =[]
    
    def dataExtraction(self):
        
        extract_data_T = eval(str(self.rawTemperature[3]))
        
        extract_data_sg = eval(str(self.rawSg[3]))
        self.temp = extract_data_T['temp']
        self.sg = extract_data_sg['gravity']/1000
        self.temp_hystory.append(self.temp)
        self.sg_hystory.append(self.sg)
        
    def sg_tranformation(self,sg,T):
        # density = self.param['density']
        # /https://powderprocess.net/Tools_html/Data_Diagrams/Water_Properties_Correlations.html
        a=  -2.8054253e-10
        b = 1.0556302e-7
        c = -4.6170461e-5
        d = -0.0079870401
        e = 16.945176
        f = 999.83952
        g = 0.01687985
        
        densityTemp = (f + e*T + d*T**2 + c*T**3 + b*T**4 + a*T**5)/(1+g*T) #kg/m**3 needs transformation
        
        PM_sug = 342.3 #g/mol
        brig_grade0=self.brixTransform(self.sg_hystory[0])
        brig_grade = self.brixTransform(sg)
        self.sug_conc = densityTemp/1000 * abs(brig_grade) * 10 *1000 / PM_sug
        self.sug_conc_hystory.append(self.sug_conc)
        return(self.sug_conc)
    
    def brixTransform(self, sg):
        if sg <= 0:
            sg = 1
        brix_grade = 143.254*(sg)**3 - 648.67*(sg)**2+1125.805*(sg)-620.389
        # brix_grade = (((182.4601 * sg -775.6821) * sg +1262.7794) * sg -669.5622)
        return brix_grade
    
    def EtOHpercentage(self,sg):
        # https://www.instructables.com/Measuring-Alcohol-Content-With-a-Hydrometer/
        # ABV(%) = (Initial Gravity - Final Gravity) * 131.25
        ABV = abs(self.sg_hystory[0] - sg) * 131.25
        self.ABV_hys.append(ABV)
    
    def processData(self):
        
        self.dataExtraction()
        self.sg_tranformation(self.sg,self.temp)
        self.EtOHpercentage(self.sg)

class TempSens:
    
    def __init__(self, 
                 rawTemp = ['tilt', '18', '7/9/2022 20:19', '{"temp": 37.78, "gravity": 1070}'], 
                 
                 param = {})->None:
    # def __init__(self, temperature = 20, CO2 = 15, sg = 1.05 , temp_H2O = 18, 
                #  param = {})->None:
        self.rawTemp = rawTemp
        
        self.param= param
        #outputs
        
        self.temp = 0
        
        self.temp_hystory = []
        
    
    def dataExtraction(self):
        
        extract_data_T = eval(str(self.rawTemp[3]))
        
        self.temp = extract_data_T['temp']
    
        self.temp_hystory.append(self.temp)
        
        
    
    
    def processData(self):
        
        self.dataExtraction()

class CurrentSens:
    
    def __init__(self, 
                 rawData = ['current',32,'2025-01-12 21:48:33',{'current': 0.6908518662808606}], 
                 
                 param = {})->None:
    # def __init__(self, temperature = 20, CO2 = 15, sg = 1.05 , temp_H2O = 18, 
                #  param = {})->None:
        self.rawData = rawData
        
        self.param= param
        #outputs
        
        self.eCurrent = 0
        
        self.eCurr_hystory = []
        
    
    def dataExtraction(self, data):
        if type(data) == list:
            for element in data:
                try:
                    eCurrent = eval(element)
                    if type(eCurrent) == dict:
                        self.eCurrent = eCurrent['current']
                        self.eCurr_hystory.append(self.eCurrent)
                except:
                    pass
                # extract_data_T = eval(str(self.rawTemp[3]))
                
                # self.temp = extract_data_T['temp']
            
                # self.temp_hystory.append(self.temp)
    
    def processData(self):
        
        self.dataExtraction(self.rawData)
       
    