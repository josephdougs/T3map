###############################################################################
# GPIB Class and Initializations

import visa
from struct import pack
import time


class GpibInst(visa.GpibInstrument):
    __GPIB_ADDRESS = 19
    __VOLTAGR__ = 0.3

    def __init__(self,reset=True):       
        visa.GpibInstrument.__init__(self, self.__GPIB_ADDRESS, timeout=30)

    # create a pulse
    def init_pulse(self, numVertex, amp = 0.2, burst_count = 255): # runs wave
    	self.write("*CLS") # clears standard event status byte
        self.write("*SRE 16") # enable "message available" bit 
                                # (sees if data is in the output buffer)
	

        self.write("AMPL " + str(amp))

	##### We are building up the pulse
	
        checkSum = 0 # initialize checksum
 
        data = [0, 0, 100, 0, 101, -2047, 1000, 0] # list of x,y vector values
	
        for count in range(0, len(data)): # makes a checksum that is sent after all 
            checkSum += data[count]         # vector pairs to ensure integrity
	
        self.write("LDWF? 1,%i" % (len(data) / 2)) # checks if machine is ready in vector mode


        if self.read() != "1": # quit if there's an error loading the waveform
            print "Error with LDWF"
            quit()

	# initialize input
        input = pack('h', 0)

        # adds the values from data into input
        for v in range(len(data)):
            if v == 0:
                input = pack('h', data[0])
            else:
                input = input + pack('h', data[v])
        
        input = input + pack('h', checkSum)

	# actually writes input to the function generator
        self.write(input)
	
	###### small test
        #input = pack('h', 0)  + pack('h', 0)
        #self.write(input)	

        self.write("FUNC5\n") # sets to arbitrary waveform to produce output
        
        # FOR TESTING! DELETE UPON FINAL
        print "The generator make the vector waveform"

        # sets the burst count (default is 255)
        self.write("BCNT " + str(burst_count))

        # sets the trigger source to single (actually triggers as many bursts as burst count)
        self.write("TSRC 0")

        # enables modulation
        self.write("MENA 1")
        
        # actually triggers the bursts
        self.write("TRG*")

        

generator=GpibInst() # makes a GPIB object through visa (connects with DS345)
generator.init_pulse(4) # runs code to create a pulse


