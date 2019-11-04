import numpy as np
import math

class Predictor:

    error_threshold = 0.1  
    std_threshold   = 200
    count_threshold = 5
    width           = 3
    value_threshold = 10**3
    chi_threshold = 137

    @staticmethod
    def predict_test(curve, std_thr = std_threshold, count_thr = count_threshold):
        #pls add coment here 
        minimal_count = 1               

        discarded = curve.discard_n_sig(Predictor.width)
        count = len(discarded)

        if count <= minimal_count: return False        # prevents from calculating mean over empty set


        times   = np.array([ o[0] for o in discarded ])
        #mags   = np.array([ o[1] for o in discarded ])   
        #errors = np.array([ o[2] for o in discarded ])

        time_mean = times.mean()
        curve.time_mean, curve.some_value = Predictor.calculate_weighted_time_mean(curve, discarded)
        curve.time_std  = times.std()
        curve.discarded_count = count

        found = curve.time_std < std_thr and count > count_thr and curve.some_value > Predictor.value_threshold
        return found
        
        #GAUSS ADDED HERE
    def predict_test_Gauss(curve, std_thr = std_threshold, count_thr = count_threshold):
                chi=0
                x=0
                for x in range (len(Parser.data)):
                    chi=chi+((exp((-1)*((curve.mags-curve.some_value)**2)/(2*curve.time_std**2))/(curve.time_std*sqrt(2*math.pi)))-curve.mags)**2 #need to change curve.mags to sth what works
        
        foundG = chi<chi_threshold
        return foundG
    
    
    @staticmethod
    def calculate_weighted_time_mean(curve, discarded):
        ''' Calculates mean time for discarded points, but with
            weights. Weight is calculated by following formula:
            w_i = (mag[i] - mag_mean)^2 / error[i]^2 '''
        dist_from_mean = np.array([ curve.mag_mean - i[1] for i in discarded])
        errors = discarded[:,2]/curve.mag_mean
        weights = dist_from_mean**3 / errors**1
        times = discarded[:,0]

        return sum(times * weights) / sum(weights), sum(weights)
