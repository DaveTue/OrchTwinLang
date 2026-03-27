

class biProducts:
    """calculation of the biproducts in a fermnation -> alcohol content, and yeast."""
    
    def __init__(self, c_sugar:float = 1011.832, 
                 param = {'sug_init':1011.832, 'yeast_grams': 11.0, 
                 'volume_squaremeters':0.025}):
        """
        Initiate the yest and volume in the fermenter
        
        Args:
           yeast_grams = 11 grams
           volume = 25 liters
        """
        # self.yeast_gram = yeast_grams  # g
        # self.volume = volume_squaremeters  # m3
        # self.sug_init = sug_init # mol/L
        self.c_sugar = c_sugar # mol/L
        # self.MW_sug = 180.16; #g/mol
        # self.MW_y = 24; #g/mol
        # self.MW_etOH = 46.07; #g/mol
        self.conc_etOH = 0.0 # mol/L 
        self.conc_yeast = 0.0 # mol/L
        self.ABV_etOH = 0.0 # % v/v
        self.param = param
        
    def yeast_initial(self):
        """initial values of the yeast"""
        MW_yeast = 24  # g/mol
        yeast_grams = self.param.get('yeast_grams')  # g
        volume = self.param.get('volume_squaremeters') 
        self.y_0 = (yeast_grams/(volume*1000)) / MW_yeast  # mol/L)
    
    def conc_etOH(self, c_sugar: float = 1011.832) -> float:
        """
        calculates the ethanol concentration based on sugar concentration.
        
        Args:
            c_sugar: Current sugar concentration (g/L)
           
            
        Returns:
            ethanol concentration 'c_etOH'
        """
        st = 1.503 #stequeometry
        sug_init = self.param.get('sug_init')
        self.c_etOH = (sug_init - c_sugar) *st  # mol/L
        return self.c_etOH
    
    def conc_yeast(self, c_sugar: float = 1011.832) -> dict:
        """calculates the yeast concentration based on sugar concentration. 
        Args:
            c_sugar: Current sugar concentration (mol/L)
        Returns:
            yeast concentration 'c_yeast'
        """
        MW_sug = 180.16; #g/mol
        MW_y = 24; #g/mol
        sug_init = self.param.get('sug_init')
        
        Y_trans = 0.1  # Yield coefficient (g yeast / g sugar)      
        c_yeast = (sug_init - c_sugar) * Y_trans * (MW_sug/MW_y) + self.y_0 # mol/L
        return c_yeast  
    
    def ABV_etOH(self, c_sugar: float) -> dict:
        """calculates the alcohol by volume (ABV) based on ethanol concentration.
        Args:
            c_sugar: Sugar concentration (mol/L)
        Returns:
            Alcohol by volume 'ABV'
        """
        MW_etOH = 46.07; #g/mol
        density_etOH = 0.789  # g/mL
        self.c_etOH = self.conc_etOH(c_sugar)
        ABV = (self.c_etOH * MW_etOH/density_etOH) / 1000**2 *100  # % v/v
        
        return ABV
    
    def execute(self) -> None:
        """ calculates all the biproducts based on the current sugar concentration."""
        self.yeast_initial()
        self.ABV_etOH = self.ABV_etOH(self.c_sugar)
        self.conc_yeast = self.conc_yeast(self.c_sugar)
        