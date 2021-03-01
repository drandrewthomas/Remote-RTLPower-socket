import matplotlib.pyplot as plt
import numpy as np

from remotepowerlib import remotepowerlib

rp=remotepowerlib()
rtlstr="-f 118M:137M:200k -c 50% -g 50 -i 2s -1 -e 2s"
rp.setsocketaddress("SERVER_IP_ADDRESS")
rp.parse(rtlstr)
if rp.getdata():
    xy=np.array(rp.samples)
    plt.plot(xy[:,0],xy[:,1],'-')
    plt.xlabel('Frequency (MHz)',fontsize=50)
    plt.ylabel('dB',fontsize=50)
    plt.tick_params(labelsize=30)
    plt.show()
else:
    print("Something went wrong!")
