import datetime



def time_to_run(devisor):

    current_minutes = datetime.datetime.now().minute
    remainder = current_minutes % devisor 

    if remainder == 0:
    	return True 
    else:
    	return False 


print(time_to_run(2))
