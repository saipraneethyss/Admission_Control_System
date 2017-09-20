import numpy as np
import math
import user

'''
	module is used to obtain an uniformly distributed random point, choose a uniformly random angle b/w [0,2*pi]
	and random variable b/w [0,1] mulitplied by actual radius ---explanation pending
	num_users in the below method gives us the points for num users 
'''

base_station_coverage_radius = 10 #radius in km
print("Please enter the number of users: 1000 or 10000")
#num_users = 10000
num_users = int(input())
while(num_users not in [1000,10000]):
	print("please choose between the options and kindly enter only integers. . . .\nchoose 1000 or 10000 to start the simulation")
	num_users = int(input())
user.set_num_users(num_users)


theta_list = 2 * np.pi * np.random.uniform(0,1,num_users) 
user_loc = base_station_coverage_radius * np.sqrt(np.random.uniform(0.0, 1.0,num_users))

#finding the x and y coordinates in polar form
x_coord_list = user_loc * np.cos(theta_list) 
y_coord_list = user_loc * np.sin(theta_list)
print("---------------------uniform distribution of users completed------------------------------")

mean = 0
variance = 2 # in dB
side_length = 2000
shadow_vals = np.random.lognormal(mean,variance,[side_length,side_length])
print("Shdaowing values are computed and assigned to sqaures of 10m x 10m with in the base radius")
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
