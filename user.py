import numpy as np

'''
	this module is used to obtain an the call probability of all the users and also to set the call duration for each user 
	who is connected to the call 
'''

#System User properties:
call_arrival_rate = 6 #6 calls in 1 Hour 
call_probability =call_arrival_rate/3600 #6 calls in 3600 seconds
num_users = 0


def user_call_flag(num_of_attempting_users):
	'''
		this routine returns the true or false flag - true if user decides to call else false
		the call probability is determined by call arrival rate as computed above
	'''
	global num_users
	call_flag = np.random.choice([True,False],num_users - num_of_attempting_users,p=[call_probability,1 - call_probability]) #returns an array with one element
	return call_flag.tolist() # call_flag has one element in array hence the call is made with zero index


def call_duration_in_seconds():
	#code for determining the call duration of a user in seconds
	avg_call_dur = 60 #in seconds
	#call duration for each user is a sample form exponential distribution, with scale factor = 1 minute (avg_call_dur)
	#using random.exponential method from numpy
	current_user_dur = np.random.exponential(avg_call_dur,size=None)
	return int(current_user_dur) 

def set_num_users(number):
	global num_users
	num_users = number

	