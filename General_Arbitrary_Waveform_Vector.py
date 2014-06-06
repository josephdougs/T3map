###############################################################################
# GPIB Class and Initializations

# import visa
from struct import pack
import time


# class GpibInst(visa.GpibInstrument):
class GpibInst():
	__GPIB_ADDRESS = int(raw_input("Set GPIB Address: "))
	__VOLTAGE__ = float(raw_input("Set Voltage: "))
	__OFFSET__ = __VOLTAGE__
	__AMP__ = float(raw_input("Set Amplitude: "))
	__BURST_COUNT__ = int(raw_input("Set Burst Count (number of cycles): "))

	def __init__(self,reset=True):
		print "GENERATE WAVESSSS"
		#visa.GpibInstrument.__init__(self, self.__GPIB_ADDRESS, timeout=30)

	def get_vectors(self):
		data = []
		addVertex = True
		while(addVertex):
			x = int(raw_input("Enter an x vertex: "))
			y = int(raw_input("Enter a y vertex: "))
			addVertex = raw_input("0 for another vector pair / 1 to finish: ") == "0"
		print data
		return data

	def write(self, output):
		print output

	def read(self):
		print "reading..."

    # pass in an array of vectors (x-value, then y-value)
	def init_pulse(self):
		self.write("*CLS") # clears registers
		self.write("*SRE 16") # enables "message available bit"

		self.write("AMPL %i" % self.__AMP__)
		self.write("OFFS %i" % self.__OFFSET__)

		data = self.get_vectors()

		self.write("LDWF? 1,%i" % (len(data) / 2)) # tells machine that 'len(data) / 2' vector vertices will be sent

		if self.read() != "1": # quit if there's an error loading the waveform
			print "Error loading waveform"
			quit()
		else :
			print "Success loading waveform"

		sum = 0 # initializes checksum
		input = pack('h', data[0]) # input is the string of vertices after being packed
		for count in range(1, len(data)):
			sum += data
			input += pack('h', data[count])
        # adds packed checksum to end of data string
		input += pack('h', sum)
        # loads data string to machine
		self.write(input)

		self.write("FUNC5\n") # sets to arbitrary waveform to produce output
		self.write("BCNT %i" % self.__BURST_COUNT__) # sets burst count
		self.write("TRSC 0") # sets trigger source to single (triggers as many as burst count)
		self.write("MTYP 5") # sets the type of modulation to burst modulation
		self.write("MENA 1") # enables modulation
		self.write("TRG*") # triggers burst

generator = GpibInst() # makes a GPIB object through visa (connects with DS345)
generator.init_pulse() # runs code to generate a pulse