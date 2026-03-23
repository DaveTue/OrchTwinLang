

class biProducts:
    """calculation of the biproducts in a fermnation -> alcohol content, and yeast."""
    
    def __init__(self, sug_init:float = 1011.832, yeast_grams:float = 11.0, volume_squaremeters:float = 0.025):
        """
        Initiate the yest and volume in the fermenter
        
        Args:
           yeast_grams = 11 grams
           volume = 25 liters
        """
        self.yeast_gram = yeast_grams  # g
        self.volume = volume_squaremeters  # m3
        self.sug_init = sug_init
        self.MW_sug = 180.16; #g/mol
        self.MW_y = 24; #g/mol
        self.MW_etOH = 46.07; #g/mol
        
    def yeast_initial(self):
        """initial values of the yeast"""
        MW_yeast = 24  # g/mol
        self.y_0 = (self.yeast_gram/(self.volume*1000)) / MW_yeast  # mol/L)
    
    def conc_etOH(self, c_sugar: float = 1011.832) -> float:
        """
        calculates the ethanol concentration based on sugar concentration.
        
        Args:
            c_sugar: Current sugar concentration (g/L)
           
            
        Returns:
            ethanol concentration 'c_etOH'
        """
        st = 1.503 #stequeometry
        c_etOH = (self.sug_init - c_sugar) *st  # mol/L
        return c_etOH
    
    def conc_yeast(self, c_sugar: float = 1011.832) -> dict:
        """calculates the yeast concentration based on sugar concentration. 
        Args:
            c_sugar: Current sugar concentration (mol/L)
        Returns:
            yeast concentration 'c_yeast'
        """
        Y_trans = 0.1  # Yield coefficient (g yeast / g sugar)      
        c_yeast = (self.sug_init - c_sugar) * Y_trans * (self.MW_sug/self.MW_y) + self.y_0 # mol/L
        return c_yeast  
    
    def ABV_etOH(self, c_sugar: float) -> dict:
        """calculates the alcohol by volume (ABV) based on ethanol concentration.
        Args:
            c_sugar: Sugar concentration (mol/L)
        Returns:
            Alcohol by volume 'ABV'
        """
        density_etOH = 0.789  # g/mL
        c_etOH = self.conc_etOH(c_sugar)
        ABV = (c_etOH * self.MW_etOH/density_etOH) / 1000**2 *100  # % v/v
        
        return ABV
    
    def calculation(self, c_sugar: float) -> tuple:
        """ calculates all the biproducts based on the current sugar concentration."""
        self.yeast_initial()
        ABV_etOH = self.ABV_etOH(c_sugar)
        conc_yeast = self.conc_yeast(c_sugar)
        return ABV_etOH, conc_yeast