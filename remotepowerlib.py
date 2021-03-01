import time
from websocket import create_connection   # pip3 install websocket_client

class remotepowerlib:

    def __init__(self):
        self.cmd=""
        self.gotsamples=False
        self.samples=[]
        self.utc=-1
        self.socketaddr="127.0.0.1"
        self.socketport=43219
        self.rtlstring=""
        self.fstart=-1            # Requested start frequency (Hz)
        self.fend=-1              # Requested end frequency (Hz)
        self.fstep=-1             # Requested frequency step (Hz)           
        self.rxfstart=-1          # Received start frequency (Hz)
        self.rxfend=-1            # Received end frequency (Hz)
        self.rxfstep=-1           # Received frequency step (Hz)
        self.crop=-1              # Crop (percent)
        self.gain=-1              # Gain
        self.intint=-1            # Intergration interval (seconds)
        self.exittimer=-1         # Exit timer (seconds)
        self.dongle=-1            # SDR dongle index
        self.ppmerror=-1          # Crystal error (ppm)
        self.window="none"        # Window (hamming, blackman, blackman-harris, hann-poisson, bartlett, and youssef)
        self.downsample=-1        # Downsample filter configuration (0 to 9)
        self.peakhold=False       # Enable peak hold
        self.directsampling=False # Enable direct sampling
        self.offsettuning=False   # Enable offset tuning
        
    def clear(self):
        self.cmd=""
        self.gotsamples=False
        self.samples=[]
        self.utc=-1
        self.rtlstring=""
        self.fstart=-1            # Requested start frequency (Hz)
        self.fend=-1              # Requested end frequency (Hz)
        self.fstep=-1             # Requested frequency step (Hz)           
        self.rxfstart=-1          # Received start frequency (Hz)
        self.rxfend=-1            # Received end frequency (Hz)
        self.rxfstep=-1           # Received frequency step (Hz)
        self.crop=-1              # Crop (percent)
        self.gain=-1              # Gain
        self.intint=-1            # Intergration interval (seconds)
        self.exittimer=-1         # Exit timer (seconds)
        self.dongle=-1            # SDR dongle index
        self.ppmerror=-1          # Crystal error (ppm)
        self.window=""            # Window (hamming, blackman, blackman-harris, hann-poisson, bartlett, and youssef)
        self.downsample=-1        # Downsample filter configuration (0 to 9)
        self.peakhold=False       # Enable peak hold
        self.directsampling=False # Enable direct sampling
        self.offsettuning=False   # Enable offset tuning
        
    def __checkvalidtosend__(self):
        if self.fstart==-1 or self.fend==-1 or self.fstep==-1:
            return False
        if self.exittimer==-1:
            return False
        return True
        
    def makecommandstring(self):
        self.rtlstring=""
        if self.__checkvalidtosend__()==False:
            return False
        tstr=""
        if self.fstart!=-1 and self.fstep!=-1 and self.fend!=-1:
            tstr+="-f {0}:{1}:{2}".format(int(self.fstart),int(self.fend),int(self.fstep))
        if self.exittimer==-1:
            tstr+=" -1"
        if self.crop!=-1:
            tstr+=" -c {0}%".format(int(self.crop))
        if self.gain !=-1:
            tstr+=" -g {0}".format(int(self.gain))
        if self.intint!=-1:
            tstr+=" -i {0}s".format(int(self.intint))
        if self.exittimer!=-1:
            tstr+=" -e {0}s".format(int(self.exittimer))
        if self.dongle!=-1:
            tstr+=" -d {0}".format(int(self.dongle))
        if self.ppmerror!=-1:
            tstr+=" -p {0}".format(int(self.ppmerror))
        if self.window!="":
            tstr+=" -w "+self.window
        if self.downsample!=-1:
            tstr+=" -F {0}".format(int(self.downsample))
        if self.peakhold==True:
            tstr+=" -P"
        if self.directsampling==True:
            tstr+=" -D"
        if self.offsettuning==True:
            tstr+=" -O"
        self.rtlstring=tstr
        return True
        
    def parse(self,cstr,clr=True):
        # e.g. "-f 118M:137M:20k -c 50% -g 50 -i 2s -1"
        cnum=0
        if clr==True: self.clear()
        com=" ".join(cstr.split())
        bits=com.split(' ')
        for c in range(0,len(bits)):
            if cnum==0:
                if bits[c]=="-f": cnum=1   # Frequencies
                elif bits[c]=="-c": cnum=2 # Crop percent
                elif bits[c]=="-g": cnum=3 # Gain
                elif bits[c]=="-i": cnum=4 # Integration interval
                elif bits[c]=="-e": cnum=5 # Exit timer
                elif bits[c]=="-d": cnum=6 # SDR dongle index
                elif bits[c]=="-p": cnum=7 # Parts-per-million error
                elif bits[c]=="-w": cnum=8 # Window name
                elif bits[c]=="-F": cnum=9 # Downsample filter configuration (0 to 9)
                elif bits[c]=="-1": cnum=0 # Single-shot mode (ignored as is added anyway)
                elif bits[c]=="-P":        # Enable peak hold (no parameter following this)
                    cnum=0
                    self.setpeakhold(True)
                elif bits[c]=="-D":        # Enable direct sampling (no parameter following this)
                    cnum=0
                    self.setdirectsampling(True)
                elif bits[c]=="-O":        # Enable offset tuning (no parameter following this)
                    cnum=0
                    self.setoffsettuning(True)
            else:
                par=bits[c]
                if cnum==1:
                    self.__parsefrequencies__(par)
                elif cnum==2:
                    self.__parsecrop__(par)
                elif cnum==3:
                    self.__parsegain__(par)
                elif cnum==4:
                    self.__parseinterval__(par)
                elif cnum==5:
                    self.__parseexittimer__(par)
                elif cnum==6:
                    di=int(par)
                    self.setdongleindex(di)
                elif cnum==7:
                    ppm=int(par)
                    self.setppmerror(ppm)
                elif cnum==8:
                    self.setwindowname(par)
                elif cnum==9:
                    df=int(par)
                    self.setdownsamplefilter(df)
                cnum=0
        return self.__checkvalidtosend__()
                
    def __parsegain__(self,gstr):
        ns,ls=self.__splitnumbersletters__(gstr)
        if len(ns)==0 or ls!="":
            self.gain=-1
            return False
        nv=float(ns)
        if nv<0:
            self.gain=-1
            return False
        else:
            self.gain=nv
        return True
        
    def setgain(self,gn):
        if gn>0:
            self.gain=gn
        else:
            return False
        return True
                
    def __parsecrop__(self,cstr):
        ns,ls=self.__splitnumbersletters__(cstr)
        if len(ns)==0 or (ls!="" and ls!="%"):
            self.crop=-1
            return False
        nv=float(ns)
        if ls!="%":
            nv*=100
        if nv>=0 and nv<=100:
            self.crop=nv
        else:
            self.crop=-1
            return False
        return True
        
    def setcrop(self,cr):
        if cr>=0 and cr<=100:
            self.crop=cr
        else:
            return False
        return True
            
    def __parseinterval__(self,istr):
        mul=1
        ns,ls=self.__splitnumbersletters__(istr)
        if len(ns)==0:
            self.intint=-1
            return False
        nv=float(ns)
        if nv<0:
            self.intint=-1
            return False
        ls=ls.lower()
        if len(ls)==0 or ls=="s":
            mul=1
        elif ls=="m":
            mul=60
        elif ls=="h":
            mul=60*60
        else:
            self.intint=-1
            return False
        nv=int(nv*mul)
        self.intint=nv
        return True
        
    def setinterval(self,iv):
        if iv>0:
            self.intint=iv
        else:
            return False
        return True
                
    def __parseexittimer__(self,estr):
        mul=1
        ns,ls=self.__splitnumbersletters__(estr)
        if len(ns)==0:
            self.exittimer=-1
            return False
        nv=float(ns)
        if nv<0:
            self.exittimer=-1
            return False
        ls=ls.lower()
        if len(ls)==0 or ls=="s":
            mul=1
        elif ls=="m":
            mul=60
        elif ls=="h":
            mul=60*60
        else:
            self.exittimer=-1
            return False
        nv=int(nv*mul)
        self.exittimer=nv
        return True
        
    def setexittimer(self,et):
        if et>0:
            self.exittimer=et
        else:
            return False
        return True

    def __parsefrequencies__(self,fstr):
        bfstr=fstr.strip()
        fbits=bfstr.split(":")
        if len(fbits)!=3:
            return self.setfrequencies(-1,-1,-1)
        tfstart=self.str2hz(fbits[0])
        tfend=self.str2hz(fbits[1])
        tfstep=self.str2hz(fbits[2])
        return self.setfrequencies(tfstart,tfend,tfstep)
        
    def setfrequencies(self,f1,f2,f3):
        if f1>=00 and f2>0 and f3>0:
            self.fstart=f1
            self.fend=f2
            self.fstep=f3
            return True
        else:
            self.fstart=-1
            self.fstep=-1
            self.fend=-1
        return False
            
    def __splitnumbersletters__(self,nlstr):
        ns=""
        ls=""
        gotletter=False
        tnlstr=nlstr.replace(",",".")
        for c in tnlstr:
            if gotletter==False:
                if (not c.isdigit()) and c!=".":
                    ls+=str(c)
                    gotletter=True
                else:
                    ns+=str(c)
            else:
                ls+=str(c)
        return [ns,ls]
            
    def str2hz(self,fstr):
        mul=1
        ns,ls=self.__splitnumbersletters__(fstr)
        if len(ns)==0: return -1
        nv=float(ns)
        if nv<0:
            return -1
        ls=ls.lower()
        if len(ls)==0 or ls=="hz":
            mul=1
        elif ls=="k" or ls=="khz":
            mul=1E3
        elif ls=="m" or ls=="mhz":
            mul=1E6
        elif ls=="g" or ls=="ghz":
            mul=1E9
        else:
            return -1
        nv=int(nv*mul)
        return nv
                
    def setwindowname(self,wn):
        if wn in ["hamming","blackman","blackman-harris","hann-poisson","bartlett","youssef"]:
            self.window=wn
        elif wn!="none":
            self.window=""
            return False
        return True
                
    def setdownsamplefilter(self,df):
        if df>=0 and df<=9:
            self.downsample=df
        else:
            self.downsample=-1
            return False
        return True
        
    def setppmerror(self,ppm):
        if ppm>0:
            self.ppmerror=ppm
        else:
            self.ppmerror=-1
            return False
        return True
        
    def setdongleindex(self,di):
        if di>0:
            self.dongle=di
        else:
            self.dongle=-1
            return False
        return True
        
    def setpeakhold(self,ph=True):
        self.peakhold=ph
        
    def setdirectsampling(self,ds=True):
        self.directsampling=ds
        
    def setoffsettuning(self,ot=True):
        self.offsettuning=ot
        
    def setsocketaddress(self,addr):
        self.socketaddr=addr
        
    def setsocketport(self,port):
        self.socketport=port
        
    def getdata(self):
        self.gotsamples=False
        addr="ws://{0}:{1}".format(self.socketaddr,str(self.socketport))
        mk=self.makecommandstring()
        if mk==False: return False
        self.utc=time.time()
        try:
            ws=create_connection(addr)
            ws.send(self.rtlstring)
            result=ws.recv()
            ws.close()
        except:
            return False
        bits=str(result).strip().split(',')
        bits.pop() # Should be 'END'
        if len(bits)>4:
            self.rxfstart=float(bits[0])
            self.rxfend=float(bits[1])
            self.rxfstep=float(bits[2])
            #rxfnum=int(bits[3]) # Number of data items in line (not used)
            for c in range(4,len(bits)):
                freq=(((c-4)*self.rxfstep)+self.rxfstart)/1E6
                val=float(bits[c])
                self.samples.append([freq,val])
            self.gotsamples=True
            return True
        return False
 
