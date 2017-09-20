'''
	this module is used to calculate the SINR levels by using the rsl_calculation module.
	firstly, the signal_level is calculated by calling rsl_value() routine from the rsl_calculation module and adding the processor gain to it.
'''	
import rsl_calculation as rsl
import math

#CDMA system properties
processor_gain 	= 	20 		#in dB
noise_level 	= 	-110 	#in dB
required_SINR 	= 	6 		#in dB
min_pilot_RSL	=	-107 	#in dB

def interference(RSL,current_num_of_users):
	interference_level_dB = RSL + 10 * math.log10(current_num_of_users - 1) # val in dB
	interference_level_linear = 10**(interference_level_dB/20) 	# value in linear scale: used the formula val = 10^(gain in dB/20)
	noise_level_linear = 10**(noise_level/20)
	total_interference = interference_level_linear + noise_level_linear # adding noise and interference
	total_interference_dB = 20 * math.log10(total_interference)		#converting the value to dB scale
	return total_interference_dB
		


def current_SINR():
	RSL = rsl.RSL_value()
	print("sample vaue is: ",RSL)
	if(RSL > min_pilot_RSL):
		signal_level = RSL + processor_gain
		SINR_value = signal_level - interference(RSL,20)
		return SINR_value
	return None

print("current SINR is:", current_SINR())


