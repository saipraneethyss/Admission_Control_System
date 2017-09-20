import numpy as np
import matplotlib.pyplot as mp
import math
import find_user_loc as location
import rsl_calculation as rsl
import SINR_calculation as SINR
import user
from collections import defaultdict


def sinr_retrials(callers_for_sinr_retrials,num_of_active_users):
	for each_caller in callers_for_sinr_retrials:
		each_caller.