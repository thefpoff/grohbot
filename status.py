import pickle
import os
import time

# open the file where data is dumped
fileo = open('devices_states.pkl', 'rb')
# loading data
devices = pickle.load(fileo)
# close the file
fileo.close()


print("GROHBOT STATUS:")

for i in devices:
    print(devices[i].name + " : " + str(devices[i].state))

# Path
path = 'devices_states.pkl'

# Get the time of last modifation of the specified path since the epoch
modification_time = os.path.getmtime(path)
# convert the time in seconds since epoch to local time
local_time = time.ctime(modification_time)
print("Last modification time(Local time):", local_time)
