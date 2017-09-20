import time
import find_user_loc as location
import rsl_calculation as rsl
import SINR_calculation as SINR
import user

'''
	this module is used to perform the main simulation of the system
'''	

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
num_of_capacity_blocked = 0
current_max_caller_dist = 0
num_of_blocked_rsl_val = 0

#CDMA system properties
processor_gain 	= 	20 		#in dB
noise_level 	= 	-110 	#in dB
required_SINR 	= 	6 		#in dB
min_pilot_RSL	=	-107 	#in dB

class caller():
	'''
		caller class is used to create, modify and retreive attaributes of a calling user.
	'''
	#attributes for all users defined by caller class
	attempt_count = 0 # counter for number of users attempting to call - not counting retries
	attempt_count_including_retries = 0 # counter for number of users attempting to call - including retries

	def __init__(self,num_of_available_channels):
		self.id 				= caller.attempt_count 					#assigns user ID
		self.user_dist 			= location.distance_and_shadowing()		#assigns distance and shadowing value based on distance
		self.user_rsl			= rsl.RSL_value(self.user_dist,num_of_available_channels) #assigns RSL
		self.sinr_count_flag 	= 0
		self.rsl_count_flag 	= 0
		#increment count for each created caller
		caller.attempt_count += 1
		caller.attempt_count_including_retries += 1

	def recalcu_rsl_value(self,num_of_available_channels):
		'''
			recalculates the rsl value of the user whose is reattempting to connect to a call
		'''
		self.user_rsl =  rsl.RSL_value(self.user_dist,num_of_available_channels)
		if (self.user_rsl < min_pilot_RSL): 
			self.rsl_count_flag += 1
		else:
			self.rsl_count_flag = 0
		caller.attempt_count_including_retries += 1

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
	'''
		checks for availablity of channels and adds the user in prospective connecting callers list to active user list
	'''
	global num_available_channels
	global active_user_call_list
	global num_of_blocked_users
	global num_of_capacity_blocked

	for each_caller in prospective_connecting_callers:
		if(num_available_channels):
			each_caller.call_time()
			active_user_call_list.append(each_caller)
			num_available_channels += -1
		else:
			num_of_capacity_blocked += 1
			num_of_blocked_users += 1


def max_caller_distance(active_callers):
	if (active_callers) :
		max_dist = max([each_caller.user_dist[0] for each_caller in active_callers])
	else:
		max_dist = None
	return max_dist

print("Simulation starts now........................\n")
start_time = time.time()


simulation_time = 2*60*60
for this_second in range(simulation_time):
	#code for active users starts here
	#************************************************************************************************************************************
	if(active_user_call_list): # runs when there are active users
		#to check the count of users dropped in the given second/current iteration
		count_of_users_dropped = 0 

		for each_user in active_user_call_list:
			if (each_user.call_duration!=0) : each_user.call_duration += -1

		#check for active user' whose call is completed, & add count of those users to completed calls and free those channels 
		channels_freed = len([i for i in active_user_call_list if i.call_duration == 0]) 
		num_of_completed_calls += channels_freed
		num_available_channels += channels_freed
		#remove the references to users with zero call duration
		active_user_call_list = [i for i in active_user_call_list if i.call_duration!=0]

		num_of_active_users = len(active_user_call_list)
		#check SINR for each user level by passing the num of active users on cell 
		#and add the users to remove these users list if their SINR has been below 6dB for three consecutive times
		remove_these_users = []
		for this_connected_caller in active_user_call_list:
			this_connected_caller.sinr_level(num_of_active_users) #calculates the sinr level at this second/instance/iteration
			if (this_connected_caller.sinr_count_flag == 3): 
				num_available_channels +=1
				remove_these_users.append(this_connected_caller)
				count_of_users_dropped += 1
		num_of_dropped_calls	=	num_of_dropped_calls + count_of_users_dropped
		#remove the references to users whose calls have been dropped
		active_user_call_list = [selected_user for selected_user in active_user_call_list if selected_user not in remove_these_users]
		#print([each_caller.user_dist[0] for each_caller in active_user_call_list])
		current_max_caller_dist = max_caller_distance(active_user_call_list)
		#print(current_max_caller_dist)
	#************************************************************************************************************************************

	#code for users who do not have active call and attempting to make call - starts here
	#************************************************************************************************************************************
	num_of_attempting_users = len(active_user_call_list)+len(callers_for_retrials)
	#generate list of true and false values for users - True if they decide to call else False
	users_state = user.user_call_flag(num_of_attempting_users)  
	attempting_callers = [caller(num_available_channels) for i in users_state if i == True] #creating instance of users
	num_of_calls_attempted  = caller.attempt_count

	#code for processing callers for retrails - recalculate the rsl for retrying users 
	#if users RSL requirements fails 3 consecutive times, add them to users with rsl failure
	if(callers_for_retrials):
		users_with_rsl_failure = [] 
		for this_retrying_caller in callers_for_retrials:
			this_retrying_caller.recalcu_rsl_value(num_available_channels)
			if(this_retrying_caller.rsl_count_flag == 3):
				users_with_rsl_failure.append(this_retrying_caller)
				num_of_blocked_users += 1
				num_of_blocked_rsl_val +=1
		#remove the references to users whose calls have been blocked
		callers_for_retrials = [selected_user for selected_user in callers_for_retrials if selected_user not in users_with_rsl_failure]

	attempting_callers = callers_for_retrials + attempting_callers

	prospective_active_callers = [callers for callers in attempting_callers if callers.user_rsl > min_pilot_RSL] 
	callers_for_retrials = [callers for callers in attempting_callers if callers.user_rsl < min_pilot_RSL]

	if(prospective_active_callers):
		if(num_available_channels == 0):
			print("no single channel is available")
			num_of_blocked_users = num_of_blocked_users + len(prospective_active_callers)
			num_of_capacity_blocked += len(prospective_active_callers)
		else:
			#initaite call connection process
			call_connection(prospective_active_callers)

	#print the stats for every two minutes		
	if(this_second%120==0):		
		#print(num_of_blocked_users,num_of_completed_calls,num_of_dropped_calls,num_of_calls_attempted,len(active_user_call_list),len(callers_for_retrials))
		# print("blocked_users",num_of_blocked_users)
		# print("calls_for_retrial",len(callers_for_retrials))

		print("Number of call attempts not counting retries: ",num_of_calls_attempted)
		print("Number of call attempts including retries: ",caller.attempt_count_including_retries)
		print("Number of dropped calls: ",num_of_dropped_calls)
		print("Number of blocked calls due to signal strength: ",num_of_blocked_rsl_val)
		print("Number of blocked calls due to channel capacity: ",num_of_capacity_blocked)
		print("Number of successfully completed calls: ",num_of_completed_calls)
		print("Number of calls in progress at any given time: ",len(active_user_call_list))
		print("Number of failed calls (blocks + drops): ",num_of_blocked_users+num_of_dropped_calls)
		print("Current cell radius(most distant connected user): ",current_max_caller_dist)
		
		# print("sum is: ",num_of_blocked_users+num_of_dropped_calls+num_of_completed_calls+len(active_user_call_list)+len(callers_for_retrials))
		
		
		print("********************\n")
	#************************************************************************************************************************************
print("Simulation Statistics:")
print("======================")
print("total time taken for total simulation :",time.time()-start_time)
if(num_of_completed_calls):
	print("Ratio of the number of dropped calls to the number of completed calls:\n",num_of_dropped_calls/num_of_completed_calls)

