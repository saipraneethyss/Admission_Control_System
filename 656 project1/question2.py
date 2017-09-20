import numpy as np
import matplotlib.pyplot as mp
import math
import find_user_loc as location
import rsl_calculation as rsl
import SINR_calculation as SINR
import user

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

#obtaining the system information
# print("please enter the number of users: 1000 or 10000")
# data = input()
# if(data.isnumeric() and (eval(data) in [1000,10000])):
# 	num_of_users = int(data)
# else:
# 	print("please make sure you select a valid number")
cd = 57
ci = 0

class caller():

	attempt_count = 0 # counter for number of users attempting to call - not counting retries
	attempt_count_including_retries = 0 #counter for number of attemps including retries
	on_call = False
	call_duration = 0


	def __init__(self,user_id,current_num_of_channels_in_use):
		self.id 		= user_id
		self.user_dist 	= location.distance_from_base()
		self.user_rsl	= rsl.RSL_value(self.user_dist,current_num_of_channels_in_use)
		self.sinr_count_flag = 0
		self.rsl_count_flag = 0
		self.last_sinr_fail_time = 0
		caller.attempt_count += 1
		caller.attempt_count_including_retries += 1


	def recalcu_rsl_value(self,current_num_of_channels_in_use):
		'''
			to recalculate the rsl value of the user at the same distance form the base station
			and assgin the new value to the user_rsl
		'''
		self.user_rsl =  rsl.RSL_value(self.user_dist,current_num_of_channels_in_use)
		if (self.user_rsl < min_pilot_RSL): 
			self.rsl_count_flag += 1
		else:
			self.rsl_count_flag = 0
		caller.attempt_count_including_retries += 1


	def call_time(self):
		self.on_call = True
		self.call_duration = user.call_duration_in_seconds()


	def sinr_level(self,num_of_active_users):
		global required_SINR
		 #since rsl varies every second, we pass the user distance to recalculate rsl
		self.sinr_val =  SINR.current_SINR(rsl.RSL_value_for_SINR(self.user_dist),num_of_active_users)
		#print(self.sinr_val)
		if (self.sinr_val < required_SINR): 
			self.sinr_count_flag += 1
		else:
			self.sinr_count_flag = 0



def call_connection(current_active_users):
	global num_available_channels
	global active_user_call_list
	#connection_times = (each_caller.call_time() for each_caller in current_active_users)
	for each_caller in current_active_users:
		each_caller.call_time()
		# print("##################")
		# print(each_caller.call_duration)
	 #connection times is a generator here as () are used
	num_available_channels = num_available_channels - len(current_active_users)
	active_user_call_list = active_user_call_list + current_active_users #adds this batch of current active users to total active users list
	#print("#of active users: ",len(active_user_call_list))


for this_second in range(20):

	#code for active users starts here
	if(active_user_call_list): # runs when there are active users

		count_of_users_dropped = 0 #to check the count of users dropped in the given second/current iteration

		for each_user in active_user_call_list:
			each_user.call_duration += -1
			#print(each_user.call_duration)

		channels_freed = len([i for i in active_user_call_list if i.call_duration == 0]) #gives the count of number of users whose call duration ended
		num_of_completed_calls += channels_freed #accumulates the completed calls as no.of channels freed = no.of calls completed
		num_available_channels += channels_freed #check this
		active_user_call_list = [i for i in active_user_call_list if i.call_duration!=0]#removes references to users with zero call duration

		num_of_active_users = len(active_user_call_list)
		#check SINR for each user level by passing the num.of active users on cell and add the users to callers for retrials list if their SINR is < 6dB
		
		for this_connected_caller in active_user_call_list:
			this_connected_caller.sinr_level(num_of_active_users) #calculates the sinr level at this second/instance/iteration
			if (this_connected_caller.sinr_count_flag == 3): # check this 
				#print("sinr flag and sinr val: ",this_connected_caller.sinr_count_flag,this_connected_caller.sinr_val)
				caller.channels_occupied += -1
				active_user_call_list.remove(this_connected_caller)
				count_of_users_dropped += 1
		num_of_dropped_calls	=	num_of_dropped_calls + count_of_users_dropped


	#code for users who do not have active call and attempting to make call - starts here
	users_state = [user.user_call_flag() for i in range(1000 - (len(active_user_call_list)+len(callers_for_retrials)))] #state true if users decide to call else false
	user_id = [i for i,j in enumerate(users_state) if j == True]
	attempting_callers = [caller(u_id,num_available_channels) for u_id in user_id] #creating instance of users
	#print("number of users attempting in this second: ",len(attempting_callers),"\n")
	num_of_calls_attempted  = caller.attempt_count
	##check for conditions for attempting callers list not empty


	#code for processing callers for retrails
	if(callers_for_retrials):
		for this_retrying_caller in callers_for_retrials:
			this_retrying_caller.recalcu_rsl_value(num_available_channels)
			if(this_retrying_caller.rsl_count_flag == 3):
				callers_for_retrials.remove(this_retrying_caller)
				#print("interfe level and rsl flag : ",this_retrying_caller.user_rsl,this_retrying_caller.rsl_count_flag)
				num_of_blocked_users += 1

	attempting_callers = callers_for_retrials + attempting_callers  #callers from retrials method

	#add a fun o check the rsl for callers for retrials before adding to prospective callers
	prospective_active_callers = [callers for callers in attempting_callers if callers.user_rsl > min_pilot_RSL] 
	callers_for_retrials = [callers for callers in attempting_callers if callers.user_rsl < min_pilot_RSL]

	#num_available_channels = 56 - caller.channels_occupied
	
	if(prospective_active_callers):

		if(num_available_channels == 0):
			num_of_blocked_users = num_of_blocked_users + len(prospective_active_callers)
			
		else:
			if (num_available_channels>len(prospective_active_callers)):
				# batch_of_users = len(prospective_active_callers)
				batch_of_users = prospective_active_callers
			else:
				batch_of_users = prospective_active_callers[:num_available_channels]
				num_of_blocked_users = num_of_blocked_users + len(prospective_active_callers) - num_available_channels 
				# print("********************************************************************************")
				# print("users blocked due to lack of channels:",len(prospective_active_callers) - num_available_channels)
				# print("********************************************************************************")
			#print("#no of users connecting to call in this second: ",len(batch_of_users),"\n")
			call_connection(batch_of_users)

	if(this_second%120 == 0 ):
		print("blocked_users,completed_calls,dropped_calls,calls_attempted,in_progress,calls_for_retrial\n")
		print(num_of_blocked_users,num_of_completed_calls,num_of_dropped_calls,num_of_calls_attempted,len(active_user_call_list),len(callers_for_retrials))
		print("channels occupied: ",len(active_user_call_list))
		print("num available channels",num_available_channels)
		print("***********************************************************")
	# if(this_second%120 == 0 and active_user_call_list):
	# 	print("the num_of_blocked_users\tnum_of_completed_calls\tnum_of_dropped_calls\tnum_of_calls_attempted\tnum_of_calls_in_progress")





print("total attempt count without retries: ",caller.attempt_count)
