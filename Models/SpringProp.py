class Model:
    
    def __init__(self,R = 80,
                 param = {'R_25':15, 'alpha':0.0039,'d_wire' :0.127,
                          'd_coil':1, 'N':9.25}) -> None:
        self.R = R #ohms
        self.T_coil = 200 #C
        self.k = 200 #N/m
        self.param = param

    
    def __str__(self):
        return 'Current state is \n temp_in = {}\n mass_in = {}\n volume_in = {}\n time = {}\n temp_out = {}\n mass_out = {}\n vol_out = {}'.format(self.temp_in,self.mass_in,self.vol_in,self.time,self.temp_out,self.mass_out,self.vol_out)

    def Tcoil_calculation(self,R):
        
        Tcoil = (R/ self.param['R_25'] - 1)/self.param['alpha'] +25
        return Tcoil
    
    def k_calculation(self,Tcoil):
        #Dykhuizen, R. C., & Robino, C. V. (2004). 
        # Load relaxation of helical extension springs in transient 
        # thermal environments. 
        # Journal of Materials Engineering and Performance, 13, 151-157.
        G = 86.156 - 0.0352*Tcoil #GPa
        G_Pa = G * 10**9 #Pa
        d_wire = self.param['d_wire']/1000 #meters
        d_coil = self.param['d_coil']/1000 #meters
        N = self.param['N']
        k = (G_Pa * d_wire**4)/(8*d_coil**3*N)
        return k
    
    def execute(self):
        self.T_coil = self.Tcoil_calculation(self.R)
        self.k = self.k_calculation(self.T_coil)
        
        
        