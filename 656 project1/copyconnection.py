import numpy as np
import matplotlib.pyplot as mp
import math
import find_user_loc as location
import rsl_calculation as rsl
import SINR_calculation as SINR
import user
from collections import defaultdict

#system information
num_of_channels = 56
prospective_active_callers = []
callers_for_retrials = []
callers_for_sinr_retrials = []
active_user_call_list = []
num_of_blocked_users = 0
num_available_channels = 56
num_of_completed_calls = 0

class caller():

	attempt_count = 0 # counter for number of users attempting to call - not counting retries
	attempt_count_including_retries = 0
	channels_occupied = 0 #counter for number of channels occupied
	on_call = False
	call_duration = 0

	def __init__(self,user_id):
		self.id 	= user_id
		self.user_dist 	= location.distance_from_base()
		self.user_rsl	= rsl.RSL_value(self.user_dist)
		caller.attempt_count += 1

	def recalcu_rsl_value(self,user_dist):
		'''
			to recalculate the rsl value of the user at the same distance form the base station
			and assgin the new value to the user_rsl
		'''
		self.user_rsl =  rsl.RSL_value(user_dist)

	def call_time(self):
		self.on_call = True
		self.call_duration = user.call_duration()

	def sinr_level(self,num_of_active_users):
		#return SINR.(self.user_rsl,num_of_active_users)
		return None



def call_connection(current_active_users):
	global num_available_channels, active_user_call_list
	connection_times = (each_caller.call_time() for each_caller in current_active_users) #connection times is a generator here as () are used
	num_available_channels = num_available_channels - len(current_active_users)
	active_user_call_list = active_user_call_list + current_active_users#adds this batch of current active users to total active users list


def sinr_status(current_user,num_of_active_users):
	current_user.sinr_level(num_of_active_users)


for i in range(10):

	#code for active users starts here
	if(active_user_call_list): # runs when there are active users
		for each_user in active_user_call_list:
			each_user.call_duration += -1

		channels_freed = len([i for i in active_user_call_list if i.call_duration == 0]) #gives the count of number of users whose call duration ended
		num_of_completed_calls += channels_freed #accumulates the completed calls as no.of channels freed = no.of calls completed
		num_available_channels += channels_freed
		active_user_call_list = [i for i in active_user_call_list if i.call_duration]#removes references to users with zero call duration

		#check SINR for each user level by passing the num.of active users on cell
		#callers_for_sinr_retrials = [list(map(sinr_status()))]
			










	#code for users who do not have active call and attempting to make call - starts here
	users_state = [user.user_call_flag() for i in range(1000)] #state true if users decide to call else false
	user_id = [i for i,j in enumerate(users_state) if j == True]
	attempting_callers = [caller(u_id) for u_id in user_id] #creating instance of users

	#add a fun o check the rsl for callers for retrails before adding to prospective callers
	prospective_active_callers = [callers for callers in attempting_callers if callers.user_rsl > -107] + callers_for_retrials
	callers_for_retrials = [callers for callers in attempting_callers if callers.user_rsl < -107]

	if(num_available_channels == 0):
		num_of_blocked_users = num_of_blocked_users + len(prospective_active_callers)
		
	else:
		if (num_available_channels>len(prospective_active_callers)):
			batch_of_users = len(prospective_active_callers)
		else:
			batch_of_users = num_available_channels
			num_of_blocked_users = len(prospective_active_callers) - num_available_channels 
		call_connection(prospective_active_callers[:batch_of_users])


	








print("total attempt count without retries: ",caller.attempt_count)
