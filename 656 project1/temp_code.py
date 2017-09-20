#code for users in main.py
'''
	users = defaultdict(list)
		# print(user_id)
		# users = dict.fromkeys(user_id)
		# print(users)
		for usr_id in user_id:
			user_dist 	= 	location.distance_from_base()
			user_rsl 	= 	rsl.RSL_value(user_dist)
			users[usr_id].append(user_dist)
			users[usr_id].append(user_rsl)
		# print("the user ID and attributes are")
		# for k,v in users.items():
		# 	print("the attributes for the user - ",k," : ", v)

'''

#code available in user.py
'''
	import numpy as np
	avg_call_dur = 1 #in minutes
	#call duration for each user is a sample form exponential distribution, with scale factor = 1 minute (avg_call_dur)
	#using random.exponential method from numpy
	curremt_user_dur = np.random.exponential(avg_call_dur)
'''

##code avaliable in  rsl_calculation
'''
	#base station attributes & EIRP calculation
	base_st_ht = 50 #metres
	base_freq = 1900 #MHZ
	max_base_power = 42 #in dBm
	line_connector_loss = 2.1 #dB
	antenna_gain = 12.1 #dB

	eirp = max_base_power - line_connector_loss + antenna_gain


	#path loss using COST231 formula
	print("please enter the values")
	dist = int(input())/1000;
	cost231_loss = 46.3 + 33.9*math.log10(base_freq) - 13.82*math.log10(base_st_ht) + (44.9 - 6.55*math.log10(base_st_ht))*math.log10(dist);
	print("the loss is ",cost231_loss);

'''
##code avaliable in find_user_loc
'''
	import matplotlib.pyplot as plt
	import numpy as np
	base_station_coverage_radius = 10 #radius in km
	num_users = 1000

	#to obtain an uniformly distributed random point, choose a uniformly random angle b/w [0,2*pi]
		and random variable b/w [0,1] mulitplied by actual radius ---explanation pending
		num_users in the below method gives us the points for 1000 users 
	
	theta = 2 * np.pi * np.random.uniform(0,1,num_users) 
	user_loc = base_station_coverage_radius * np.sqrt(np.random.uniform(0.0, 1.0,num_users))

	#finding the x and y coordinates in polar form
	x = user_loc * np.cos(theta) 
	y = user_loc * np.sin(theta)

	print("coordinates are", len(np.sqrt(x**2+y**2)))
	#to plot graph
	plt.plot(x, y, "ro", ms=1)
	plt.axis([-15, 15, -15, 15])
	plt.show()
'''

'''
import matplotlib.pyplot as plt
import numpy as np
import time


# theta = 2 * np.pi * np.random.uniform(0,1,1000) 
# user_loc = 10 * np.sqrt(np.random.uniform(0.0, 1.0,1000))

# 	#finding the x and y coordinates in polar form
# x = user_loc * np.cos(theta) 
# y = user_loc * np.sin(theta)

# plt.plot(x, y, "ro", ms=1)
# plt.axis([-10, 10, -10, 10])
# plt.show()	


################################assiging shadowing values###########################
# side_length = 10
# shadow_vals = np.random.normal(0,2,[side_length,side_length])
# print(shadow_vals)
# print("///////////////////////////////////////////////////////////////")
# sub_spilt = side_length//2

# matrix_val1 =  shadow_vals[:sub_spilt,:sub_spilt]
# matrix_val2 = shadow_vals[:sub_spilt,sub_spilt:]
# matrix_val3 = shadow_vals[sub_spilt:,:sub_spilt]
# matrix_val4 = shadow_vals[sub_spilt:,sub_spilt:]

# print(matrix_val1,"\n")
# print(matrix_val2,"\n")
# print(matrix_val3,"\n")
# print(matrix_val4)

start_t = time.time()

side_length = 20000
shadow_vals = np.random.normal(0,2,[side_length,side_length])
print(" time taken : ",time.time()-start_t)

'''

#code in shadowing
'''
	# import numpy as np
	# import math


	# base_power = 42 #in dBm
	# line_connector_loss = 2.1 #dB
	# antenna_gain = 12.1 #dB
	# eirp = base_power - line_connector_loss + antenna_gain

	# g1 = np.random.normal(0,2)
	# print("the values are "+str(g1))

	import matplotlib.pyplot as plt
	import numpy as np
	import math
	import time


	# theta = 2 * np.pi * np.random.uniform(0,1,1000) 
	# user_loc = 10 * np.sqrt(np.random.uniform(0.0, 1.0,1000))

	# 	#finding the x and y coordinates in polar form
	# x = user_loc * np.cos(theta) 
	# y = user_loc * np.sin(theta)

	# plt.plot(x, y, "ro", ms=1)
	# plt.axis([-10, 10, -10, 10])
	# # plt.show()	
	def random_location_coordinates():
		base_station_coverage_radius = 10 #radius in km
		num_users = 1000
		theta = 2 * np.pi * np.random.uniform(0,1,num_users) 
		user_loc = base_station_coverage_radius * np.sqrt(np.random.uniform(0.0, 1.0,num_users))

		#finding the x and y coordinates in polar form
		x = user_loc * np.cos(theta) 
		y = user_loc * np.sin(theta)

		random_index = np.random.randint(0,num_users)
		return (x[random_index], y[random_index],theta[random_index])

	def selected_square(x,y,theta):
		col = math.floor(x) if x>0 else math.floor(x)+1
		row = math.floor(y) if y>0 else math.floor(y)+1
		print(row,col)
		if(theta>=0 and theta<=np.pi/2):
			print("quad1")
			selected_square = shadow_vals[(sub_spilt-1)-row,sub_spilt+col]
		elif(theta>np.pi/2 and theta <= np.pi):
			print("quad2")
			selected_square = shadow_vals[(sub_spilt-1)-row,(sub_spilt-1)+col]
		elif(theta>np.pi and theta <= 3*(np.pi)/2):
			print("quad3")
			selected_square = shadow_vals[sub_spilt-row,(sub_spilt-1)+col]
		else:
			print("quad4")
			selected_square = shadow_vals[sub_spilt-row,sub_spilt+col]
		return selected_square

	start_t = time.time()
	################################assiging shadowing values###########################
	# side_length = 20000
	# shadow_vals = np.random.normal(0,2,[side_length,side_length])
	# num_of_val_in_quad = len(shadow_vals)//4
	# sub_spilt = side_length//2
	# print(num_of_val_in_quad)



	################################assiging shadowing values###########################
	side_length = 2000
	shadow_vals = np.random.normal(0,2,[side_length,side_length])
	print(" time taken : ",time.time()-start_t)
	sub_spilt = side_length//2
	print(shadow_vals)




	# # print(quad1_vals,len(quad1_vals))
	# matrix_val1 = [shadow_vals[sub_spilt*i:sub_spilt*(i+1)] for i in range(0,sub_spilt)]

	# matrix_val2 = [shadow_vals[sub_spilt*i:sub_spilt*(i+1)] for i in range(0,sub_spilt)]

	# matrix_val3 = [shadow_vals[sub_spilt*i:sub_spilt*(i+1)] for i in range(0,sub_spilt)]

	# matrix_val4 = [shadow_vals[sub_spilt*i:sub_spilt*(i+1)] for i in range(0,sub_spilt)]

	# ##############################shadowing values assigned#############################

	(x,y,theta) = random_location_coordinates()
	print(x,y)
	selected_shadow_value = selected_square(x,y,theta)
	print(selected_shadow_value)
	print("total time taken : ",time.time()-start_t)
'''








