import time
start_time = time.time()


import numpy as np
import matplotlib.pyplot as mp
import math
import find_user_loc as location
import rsl_calculation as rsl
import SINR_calculation as SINR
import user

print("all modules imported")
#system statistics
prospective_active_callers = []
callers_for_retrials = []
callers_for_sinr_retrials = []
active_user_call_list = []
num_of_blocked_users = 0
num_available_channels = 56
num_of_calls_attempted = 0
num_of_completed_calls = 0
num_of_dropped_calls = 0

#CDMA system properties
processor_gain 	= 	20 		#in dB
noise_level 	= 	-110 	#in dB
required_SINR 	= 	6 		#in dB
min_pilot_RSL	=	-107 	#in dB

class caller():

	attempt_count = 0 # counter for number of users attempting to call - not counting retries
	attempt_count_including_retries = 0
	channels_occupied = 0 #counter for number of channels occupied
	call_duration = 0

	def __init__(self,num_of_available_channels):
		self.id 		= caller.attempt_count
		self.user_dist 	= location.distance_and_shadowing()
		self.user_rsl	= rsl.RSL_value(self.user_dist,num_of_available_channels)
		self.sinr_count_flag = 0
		self.rsl_count_flag = 0
		caller.attempt_count += 1
		caller.attempt_count_including_retries += 1

	def recalcu_rsl_value(self,num_of_available_channels):
		'''
			to recalculate the rsl value of the user at the same distance form the base station
			and assgin the new value to the user_rsl
		'''
		caller.attempt_count_including_retries += 1
		self.user_rsl =  rsl.RSL_value(self.user_dist,num_of_available_channels)
		if (self.user_rsl < min_pilot_RSL): 
			self.rsl_count_flag += 1
		else:
			caller.channels_occupied += 1
			self.rsl_count_flag = 0

	def call_time(self):
		self.call_duration = user.call_duration_in_seconds()

	def sinr_level(self,num_of_active_users):
		global required_SINR
		 #since rsl varies every second, we pass the user distance to recalculate rsl
		self.sinr_val =  SINR.current_SINR(rsl.RSL_value_for_SINR(self.user_dist),num_of_active_users)
		if (self.sinr_val < required_SINR): 
			self.sinr_count_flag += 1
		else:
			self.sinr_count_flag = 0



def call_connection(prospective_connecting_callers):
	global num_available_channels
	global active_user_call_list
	global num_of_blocked_users

	for each_caller in prospective_connecting_callers:
		if(num_available_channels):
			each_caller.call_time()
			active_user_call_list.append(each_caller)
			num_available_channels += -1
		else:
			num_of_blocked_users += 1

print("iterations start now........................\n")

for this_second in range(7200):

	#code for active users starts here
	#************************************************************************************************************************************
	if(active_user_call_list): # runs when there are active users

		count_of_users_dropped = 0 #to check the count of users dropped in the given second/current iteration

		for each_user in active_user_call_list:
			each_user.call_duration += -1

		channels_freed = len([i for i in active_user_call_list if i.call_duration == 0]) #gives the count of number of users whose call duration ended
		num_of_completed_calls += channels_freed #accumulates the completed calls as no.of channels freed = no.of calls completed
		num_available_channels += channels_freed
		active_user_call_list = [i for i in active_user_call_list if i.call_duration!=0]#removes references to users with zero call duration

		num_of_active_users = len(active_user_call_list)
		#check SINR for each user level by passing the num.of active users on cell and add the users to callers for retrials list if their SINR is < 6dB
		
		remove_these_users = []
		for this_connected_caller in active_user_call_list:
			this_connected_caller.sinr_level(num_of_active_users) #calculates the sinr level at this second/instance/iteration
			if (this_connected_caller.sinr_count_flag == 3): # check this 
				num_available_channels +=1
				remove_these_users.append(this_connected_caller)
				count_of_users_dropped += 1
		num_of_dropped_calls	=	num_of_dropped_calls + count_of_users_dropped
		active_user_call_list = [selected_user for selected_user in active_user_call_list if selected_user not in remove_these_users]
	#************************************************************************************************************************************

	#code for users who do not have active call and attempting to make call - starts here
	#************************************************************************************************************************************
	users_state = [user.user_call_flag() for i in range(1000 - (len(active_user_call_list)+len(callers_for_retrials)))]  #state true if users decide to call else false
	#user_id = [i for i,j in enumerate(users_state) if j == True]
	attempting_callers = [caller(num_available_channels) for i in users_state if i == True] #creating instance of users
	#print("number of users attempting in this second: ",len(attempting_callers))
	num_of_calls_attempted  = caller.attempt_count

	#code for processing callers for retrails
	if(callers_for_retrials):
		users_with_rsl_failure = []
		for this_retrying_caller in callers_for_retrials:
			this_retrying_caller.recalcu_rsl_value(num_available_channels)
			if(this_retrying_caller.rsl_count_flag == 3):
				users_with_rsl_failure.append(this_retrying_caller)
				#print("interfe level and rsl flag : ",this_retrying_caller.user_rsl,this_retrying_caller.rsl_count_flag)
				num_of_blocked_users += 1
		callers_for_retrials = [selected_user for selected_user in callers_for_retrials if selected_user not in users_with_rsl_failure]

	attempting_callers = callers_for_retrials + attempting_callers  #callers from retrials method

	prospective_active_callers = [callers for callers in attempting_callers if callers.user_rsl > min_pilot_RSL] 
	callers_for_retrials = [callers for callers in attempting_callers if callers.user_rsl < min_pilot_RSL]

	if(prospective_active_callers):

		if(num_available_channels == 0):
			print("no single channel is available")
			num_of_blocked_users = num_of_blocked_users + len(prospective_active_callers)
		else:
			call_connection(prospective_active_callers)
	if(this_second%120==0):		
		print("blocked_users,completed_calls,dropped_calls,calls_attempted,in_progress,calls_for_retrial")
		print(num_of_blocked_users,num_of_completed_calls,num_of_dropped_calls,num_of_calls_attempted,len(active_user_call_list),len(callers_for_retrials))
		print("sum is: ",num_of_blocked_users+num_of_dropped_calls+num_of_completed_calls+len(active_user_call_list)+len(callers_for_retrials))
		print("retries inculde: ",caller.attempt_count_including_retries)
		print("********************\n")
	#************************************************************************************************************************************
# print("total attempt count without retries: ",caller.attempt_count)
# print("retries inculde: ",caller.attempt_count_including_retries)
print("total time taken :",time.time()-start_time)

