import matplotlib.pyplot as plt
import numpy as np
import math

base_station_coverage_radius = 10 #radius in km
num_users = 1000

'''to obtain an uniformly distributed random point, choose a uniformly random angle b/w [0,2*pi]
	and random variable b/w [0,1] mulitplied by actual radius ---explanation pending
	num_users in the below method gives us the points for 1000 users 
'''
theta_list = 2 * np.pi * np.random.uniform(0,1,num_users) 
user_loc = base_station_coverage_radius * np.sqrt(np.random.uniform(0.0, 1.0,num_users))

#finding the x and y coordinates in polar form
x_coord_list = user_loc * np.cos(theta_list) 
y_coord_list = user_loc * np.sin(theta_list)
print("users distributed completed")

mean = 0
variance = 2 # in dB
side_length = 2000
shadow_vals = np.random.normal(mean,variance,[side_length,side_length])
print("Shdaowing caclulation completed")
sub_spilt = side_length//2

def selected_square_shadowing(x,y,theta):
	col = math.floor(x) if x>0 else math.floor(x)+1
	row = math.floor(y) if y>0 else math.floor(y)+1
	if(theta>=0 and theta<=np.pi/2):
		shadowing_val = shadow_vals[(sub_spilt-1)-row,sub_spilt+col]
	elif(theta>np.pi/2 and theta <= np.pi):
		shadowing_val = shadow_vals[(sub_spilt-1)-row,(sub_spilt-1)+col]
	elif(theta>np.pi and theta <= 3*(np.pi)/2):
		shadowing_val = shadow_vals[sub_spilt-row,(sub_spilt-1)+col]
	else:
		shadowing_val = shadow_vals[sub_spilt-row,sub_spilt+col]
	return shadowing_val

def distance_and_shadowing():
	global x_coord_list
	global y_coord_list
	random_index = np.random.randint(0,num_users)
	(x,y,theta) = (x_coord_list[random_index], y_coord_list[random_index],theta_list[random_index])
	shadowing = selected_square_shadowing(x,y,theta)
	distance = np.sqrt(x**2+y**2)
	return (distance,shadowing)