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
num_of_users_connected = 0
prospective_active_callers = []
callers_for_retrials = []

class caller():

	attempt_count = 0 # counter for number of users attempting to call - not counting retries
	attempt_count_including_retries = 0
	def __init__(self,user_id):
		self.id 	= user_id
		self.user_dist 	= location.distance_from_base()
		self.user_rsl	= rsl.RSL_value(self.user_dist)
		caller.attempt_count+=1

	def recalcu_rsl_value(self,user_dist):
		'''
			to recalculate the rsl value of the user at the same distance form the base station
			and assgin the new value to the user_rsl
		'''
		self.user_rsl =  rsl.RSL_value(user_dist)

	def call_time(self):
		return user.call_duration()
		
	def call_duration_status(self,user,num_available):
		if(num_available): caller.channels_occupied += 1



# def call_connection(active_users):
# 	connection_times = [each_caller.call() for each_caller in active_users]





for i in range(10):
	users_state = [user.user_call_flag() for i in range(1000)] #state true if users decide to call else false
	user_id = [i for i,j in enumerate(users_state) if j == True]
	print("\nusers in this iteration:\n ",len(user_id))
	attempting_callers = [caller(u_id) for u_id in user_id] #creating instance of users
	print(*[(i.id,i.user_dist,i.user_rsl) for i in attempting_callers],sep="\n")
	
	#separating the users with RSL greater than minimum required pilot RSL value( -107dB) as prospctive active users
	#and the remaining for retrails
	# prospective_active_callers = [(callers.id, callers.user_dist) for callers in attempting_callers if callers.user_rsl > -107] + callers_for_retrials
	# callers_for_retrials = [(callers.id, callers.user_dist) for callers in attempting_callers if callers.user_rsl < -107]
	prospective_active_callers = [callers for callers in attempting_callers if callers.user_rsl > -107] + callers_for_retrials
	callers_for_retrials = [callers for callers in attempting_callers if callers.user_rsl < -107]
	#code for tring id in callers_for retrials 

	'''
		the users in prospective_active_callers can now communicate with base station provided a channel is available
	'''

	# if(num_of_channels>0):
	# 	# num_available = 
	# 	call_connection(prospective_active_callers)
	# else:
	# 	number_of_blocked_users = len(prospective_active_callers)



	#print(prospective_active_callers,callers_for_retrials)
	print("total attempt count without retries: ",caller.attempt_count)
	





