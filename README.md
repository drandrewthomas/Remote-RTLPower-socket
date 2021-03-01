# Remote RTLPower socket

## What is this project?

Remote RTLPower Socket is a Python 3 library for remotely accessing RTL-SDR software-defined radio power data over a websocket. It consistes of two parts, the first being a websocket server that can be run on a PC, or even a Raspberry Pi, that has been set up to use RTL-SDR dongles and has rtlpower installed. The second is a client library that can be used to request and receive data from the server on a remote computer. While the client is written in Python the server can also be accessed using your own code, including web-apps written in Javascript, using standard websockets: the client and server both run over port 43219 although you could change that if you wish in their code files. 

## Python prerequisites

There are few prerequisites for using this project. The main one is Python 3 itself (Python 2 isn't supported as it's deprecated and will raise errors due to data decoding if you try). On the server computer, with rtlpower installed, you will need to use pip to install 'websocket-server' and on the client computer you need 'install websocket_client'. If you want to try the example power graph program you'll also need matplotlib and numpy. Also, if you have a firewall don't forget to allow traffic through the websocket port (e.g. port 43219 if you haven't changed it)

## Running the server

On the PC you have your RTL-SDR setup on, make sure you have rtlpower installed. Then put the rtlpowersocket.py on that computer and run:

    python3 rtlpowersocket.py

When the server starts up it will print a simple message including the port number it is listening on.

## Running the client

Copy the Python files to your client computer, or even an andriod phone or tablet (the server should work fine using PyDroid3). Then just run the examples to try out your connection:

    python3 getremotepower.py

    python3 getremotepowergraph.py

## Using the library in your own code

Using this project is fairly straightforward. Firstly import the library into a Python file on your client computer (or Android device using PyDriod3) and create a remote power object:

    from remotepowerlib import remotepowerlib
    rp=remotepowerlib()

Now, tell it the IP address of the server on your local network (if you're accessing from the wider internet you'll need to port-forward the server port to this IP address too):

    rp.setsocketaddress("SERVER_IP_ADDRESS")

Next, set the rtlpower parameters for the power data you want. You can set them individually (e.g. rp.setfrequencies("118M","137M","200k")) and you'll find all the parameters in the remotepowerlib.py file. However, much easier is to get the library to parse a standard rtlpower commandline string:

    rtlstr="-f 118M:137M:200k -c 50% -g 50 -i 2s -1 -e 2s"
    rp.parse(rtlstr)

Finally, request the rtlpower data for your parameters using getdata() which will return True or False to indicate whether all went well. If all did go well you should see that the samples are a list of frequency/power values which you can process, use and store as you like.

    if rp.getdata():
        print(rp.samples)
    else:
        print("Something went wrong!")

## Credits

This project is copyright 2019-2021 Andrew Thomas and is distributed under the GPL3 license.
