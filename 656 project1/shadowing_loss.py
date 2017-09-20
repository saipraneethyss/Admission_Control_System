import numpy as np
import math


mean = 0
variance = 2 # in dB
side_length = 2000
shadow_vals = np.random.normal(mean,variance,[side_length,side_length])
sub_spilt = side_length//2

def selected_square(x,y,theta):
	col = math.floor(x) if x>0 else math.floor(x)+1
	row = math.floor(y) if y>0 else math.floor(y)+1
	print(row,col)
	if(theta>=0 and theta<=np.pi/2):
		print("quad1")
		shadowing_val = shadow_vals[(sub_spilt-1)-row,sub_spilt+col]
	elif(theta>np.pi/2 and theta <= np.pi):
		print("quad2")
		shadowing_val = shadow_vals[(sub_spilt-1)-row,(sub_spilt-1)+col]
	elif(theta>np.pi and theta <= 3*(np.pi)/2):
		print("quad3")
		shadowing_val = shadow_vals[sub_spilt-row,(sub_spilt-1)+col]
	else:
		print("quad4")
		shadowing_val = shadow_vals[sub_spilt-row,sub_spilt+col]
	return shadowing_val





