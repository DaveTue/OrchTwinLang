

class KalmanFilter:
    """Simple Kalman filter for a brewery fermentation process."""
    
    def __init__(self, P_init: float = 1648.12, sigma_sensor_default: float = 34.2):
        """
        Initialize the Kalman filter.
        
        Args:
            P_init: Initial covariance P [default: 1.0]
            sigma_sensor_default: Default sensor variance [default: 1.0]
        """
        self._P_prev = P_init
        self._sigma_sensor_default = sigma_sensor_default
    
    def reset(self):
        """Reset internal state to defaults."""
        self._P_prev = 1648.12
    
    def step(self, sigma_sensor: float, x_measure: float, x_cal: float) -> dict:
        """
        Perform one Kalman filter step.
        
        Args:
            sigma_sensor: Sensor measurement variance
            x_measure: Measured value
            x_cal: Model-calculated value
            
        Returns:
            state estimate 'x_hat'
        """
        p_prev = self._P_prev
        sigma = sigma_sensor if sigma_sensor > 0 else self._sigma_sensor_default
        x_m = x_measure
        x_c = x_cal
        
        # Kalman gain: K = p_prev / (p_prev + sigma)
        denom = p_prev + sigma
        K = 0.0 if denom <= 0.0 else p_prev / denom
        
        # Predicted covariance: p_nn = (1 - K) * p_prev
        p_nn = (1.0 - K) * p_prev
        
        # State estimate: x_hat = x_cal + K * (x_measure - x_cal)
        x_hat = x_c + K * (x_m - x_c)
        
        # Update covariance: P = p_nn + sigma
        P = p_nn + sigma
        
        # Store for next step
        self._P_prev = P
        
        return  x_hat
        # return {"K": K, "x_hat": x_hat}
