import numpy as np
import math

#base station attributes & EIRP calculation
base_st_ht = 50 #metres
base_freq = 1900 #MHZ
max_base_power = 42 #in dBm
line_connector_loss = 2.1 #dB
antenna_gain = 12.1 #dB

EIRP_max = max_base_power - line_connector_loss + antenna_gain #dBm
EIRP_min = 30 #dBm

print("***************************Options********************")
print("\tEnter 1 to select simulation without admission control\n\tEnter 2 to select simulation with admission control")

selection = int(input())
while(selection not in [1,2]):
	print("please choose between the options and kindly enter only integers. . . .\nchoose 1 or 2 to start the simulation")
	selection = int(input())

(C_d,C_i) = (20,15) if selection==2 else (57,0)  #higher limit for channels in use

print("setting up the system................")

EIRP_current_val = EIRP_max

def EIRP(num_of_available_channels):
	global EIRP_current_val
	channels_in_use = 56 - num_of_available_channels
	if(channels_in_use > C_d):
		EIRP_current_val = EIRP_current_val - 0.5 if(EIRP_current_val >30) else 30
	elif(channels_in_use < C_i):
		EIRP_current_val = EIRP_current_val + 0.5 if(EIRP_current_val<52) else 52
	return EIRP_current_val

def PL_cost231(dist):
	#path loss using COST231 formula
	cost231_loss = 46.3 + 33.9*math.log10(base_freq) - 13.82*math.log10(base_st_ht) + (44.9 - 6.55*math.log10(base_st_ht))*math.log10(dist);
	return cost231_loss

def fading_value(): # have to call this in main file
	#method to find the fading value in dB
	rayliegh_value = np.random.rayleigh()
	fading_val = 20 * np.log10(rayliegh_value) # converting the value to dB
	return fading_val

def RSL_value(distance,num_of_available_channels):
	shadowing_value = distance[1]
	dist = distance[0] 
	rsl = EIRP(num_of_available_channels) - PL_cost231(dist) + shadowing_value + fading_value()
	return rsl

def RSL_value_for_SINR(distance):
	shadowing_value = distance[1]
	dist = distance[0] 
	rsl = EIRP_max - PL_cost231(dist) + shadowing_value + fading_value()
	return rsl







