import numpy as np
import matplotlib.pyplot as mp
import math
import find_user_loc as location
import rsl_calculation as rsl
import SINR_calculation as SINR
import user
from collections import defaultdict

#system statistics
num_of_channels = 56
prospective_active_callers = []
callers_for_retrials = []
callers_for_sinr_retrials = []
active_user_call_list = []
num_of_blocked_users = 0
num_available_channels = 56
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
	on_call = False
	call_duration = 0

	def __init__(self,user_id):
		self.id 		= user_id
		self.user_dist 	= location.distance_from_base()
		self.user_rsl	= rsl.RSL_value(self.user_dist)
		self.sinr_count_flag = 0
		self.rsl_count_flag = 0
		caller.attempt_count += 1

	def recalcu_rsl_value(self):
		'''
			to recalculate the rsl value of the user at the same distance form the base station
			and assgin the new value to the user_rsl
		'''
		self.user_rsl =  rsl.RSL_value(self.user_dist)
		self.rsl_count_flag()

	def call_time(self):
		self.on_call = True
		self.call_duration = user.call_duration()

	def sinr_level(self,num_of_active_users):
		self.sinr_val = SINR.current_SINR(self.user_rsl,num_of_active_users)

	def recalcu_sinr_level(self,num_of_active_users):
		'''
			to recalculate the SINR level of the user for 2nd and 3rd time and assgin the new value to the sinr_val
		'''
		self.sinr_val =  SINR.current_SINR(rsl.RSL_value(self.user_dist),num_of_active_users)
		self.sinr_retrail_count()

	def sinr_retrail_count(self):
		self.sinr_count_flag = self.sinr_count_flag + 1 if (self.sinr_count_flag < 2) else 0

	def rsl_retrail_count(self):
		self.rsl_count_flag = self.rsl_count_flag + 1 if (self.rsl_count_flag < 2) else 0



def call_connection(current_active_users):
	global num_available_channels, active_user_call_list
	connection_times = (each_caller.call_time() for each_caller in current_active_users) #connection times is a generator here as () are used
	num_available_channels = num_available_channels - len(current_active_users)
	active_user_call_list = active_user_call_list + current_active_users#adds this batch of current active users to total active users list

def sinr_retrials(callers_for_sinr_retrials,num_of_active_users):
	global num_of_dropped_calls, active_user_call_list
	#check for the users whose SINR retrails have exceeded three tries and count them as dropped users
	count_of_users_dropped = 0 #to check the count of users dropped in the given second/current iteration
	for this_reconnecting_caller in callers_for_sinr_retrials:
		if(this_reconnecting_caller.sinr_count_flag == 2):
			active_user_call_list.remove(this_reconnecting_caller)
			count_of_users_dropped += 1
		else:
			this_reconnecting_caller.recalcu_sinr_level()
	num_of_dropped_calls	=	num_of_dropped_calls + count_of_users_dropped



def sinr_retrials(callers_for_sinr_retrials,num_of_active_users):
	global num_of_dropped_calls, active_user_call_list
	#check for the users whose SINR retrails have exceeded three tries and count them as dropped users
	count_of_users_dropped = 0 #to check the count of users dropped in the given second/current iteration
	for this_reconnecting_caller in callers_for_sinr_retrials:
		if(this_reconnecting_caller.sinr_count_flag == 2):
			active_user_call_list.remove(this_reconnecting_caller)
			count_of_users_dropped += 1
		else:
			this_reconnecting_caller.recalcu_sinr_level()
	num_of_dropped_calls	=	num_of_dropped_calls + count_of_users_dropped



for i in range(10):

	#code for active users starts here
	if(active_user_call_list): # runs when there are active users
		for each_user in active_user_call_list:
			each_user.call_duration += -1

		channels_freed = len([i for i in active_user_call_list if i.call_duration == 0]) #gives the count of number of users whose call duration ended
		num_of_completed_calls += channels_freed #accumulates the completed calls as no.of channels freed = no.of calls completed
		num_available_channels += channels_freed #check this
		active_user_call_list = [i for i in active_user_call_list if i.call_duration]#removes references to users with zero call duration

		num_of_active_users = len(active_user_call_list)

		#to check for any users whose SINR levels are below the required 6dB in the previous second/iteration.
		#this if condition will not execute for 1st iteration as there will be no active users
		if(callers_for_sinr_retrials): #executes only when the list of users for sinr retrials is not empty
			#call the retrial module's sinr user returns method to find users whose sinr criterion is met in 3 tries
			sinr_retrials(callers_for_sinr_retrials,num_of_active_users)



		#check SINR for each user level by passing the num.of active users on cell and add the users to callers for retrials list if their SINR is < 6dB
		
		for connected_caller in active_user_call_list:
			connected_caller.sinr_level(num_of_active_users)
			if connected_caller.sinr_val < required_SINR: callers_for_sinr_retrials.append(connected_caller)
		
		 

		#check users 
			










	#code for users who do not have active call and attempting to make call - starts here
	users_state = [user.user_call_flag() for i in range(1000)] #state true if users decide to call else false
	user_id = [i for i,j in enumerate(users_state) if j == True]
	attempting_callers = [caller(u_id) for u_id in user_id] #creating instance of users
	attempting_callers = attempting_callers + callers_for_retrials #callers from retrials method
	##check for conditions for attempting callers list not empty

	#add a fun o check the rsl for callers for retrials before adding to prospective callers
	prospective_active_callers = [callers for callers in attempting_callers if callers.user_rsl > min_pilot_RSL] 
	callers_for_retrials = [callers for callers in attempting_callers if callers.user_rsl < min_pilot_RSL]

	if(num_available_channels == 0):
		num_of_blocked_users = num_of_blocked_users + len(prospective_active_callers)
		
	else:
		if (num_available_channels>len(prospective_active_callers)):
			batch_of_users = len(prospective_active_callers)
		else:
			batch_of_users = num_available_channels
			num_of_blocked_users = num_of_blocked_users + len(prospective_active_callers) - num_available_channels 
		call_connection(prospective_active_callers[:batch_of_users])


	








print("total attempt count without retries: ",caller.attempt_count)
