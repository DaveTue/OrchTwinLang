

class KalmanFilter:
    """Simple Kalman filter for a brewery fermentation process."""
    
    def __init__(self, x_measure: float = 1011.83, 
                 param = {'P_prev': 1648.12, 'sigma_sensor_default': 34.2}):
        """
        Initialize the Kalman filter.
        
        Args:
            P_init: Initial covariance P [default: 1.0]
            sigma_sensor_default: Default sensor variance [default: 1.0]
        """
        # self._P_prev = P_init
        # self._sigma_sensor_default = sigma_sensor_default
        self.x_measure = 1011.83 # Initial measured value from sensor [mol/L]
        self.x_cal = 1011.83 # Initial calculated value from a model [mol/L]
        self.x_hat = self.x_measure # Initial state estimate [mol/L]
        self.param = param
    
    def reset(self):
        """Reset internal state to defaults."""
        self.param['P_prev'] = 1648.12
        self.x_cal = 1011.83
        self.x_measure = 1011.83
    
    def step(self) -> None:
    # def step(self, sigma_sensor: float, x_measure: float, x_cal: float) -> dict:
        """
        Perform one Kalman filter step.
        
        Args:
            sigma_sensor: Sensor measurement variance
            x_measure: Measured value
            x_cal: Model-calculated value
            
        Returns:
            state estimate 'x_hat'
        """
        # p_prev = 
        p_prev = self.param['P_prev']
        # sigma = sigma_sensor if sigma_sensor > 0 else self._sigma_sensor_default
        sigma = self.param['sigma_sensor_default']
        x_m = self.x_measure
        x_c = self.x_cal
        
        # Kalman gain: K = p_prev / (p_prev + sigma)
        denom = p_prev + sigma
        K = 0.0 if denom <= 0.0 else p_prev / denom
        
        # Predicted covariance: p_nn = (1 - K) * p_prev
        p_nn = (1.0 - K) * p_prev
        
        # State estimate: x_hat = x_cal + K * (x_measure - x_cal)
        self.x_hat = x_c + K * (x_m - x_c)
        
        # Update covariance: P = p_nn + sigma
        P = p_nn + sigma
        
        # Store for next step
        self.param['P_prev'] = P
        
        # return  x_hat
        # return {"K": K, "x_hat": x_hat}
