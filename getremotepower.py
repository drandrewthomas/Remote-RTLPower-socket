from remotepowerlib import remotepowerlib

rp=remotepowerlib()
rtlstr="-f 118M:137M:200k -c 50% -g 50 -i 2s -1 -e 2s"
rp.setsocketaddress("SERVER_IP_ADDRESS")
rp.parse(rtlstr)
if rp.getdata():
    print(rp.samples)
else:
    print("Something went wrong!")
