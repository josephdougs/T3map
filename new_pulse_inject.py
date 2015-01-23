###############################################################################
# GPIB Class and Initializations

import visa
from struct import pack
import time

ADDRESS = "GPIB0::19::INSTR"
__AMP__ = 0.2
__OFFSET__ = __AMP__
__BURST_COUNT__ = 255
__DATA__ = [0, 0, 100, 0, 101, -2047, 200, 0]


def run():
	rm = visa.ResourceManager()
	ds345 = rm.open_resource('GPIB0::19::INSTR')

	ds345.write("*CLS") # clears registers
	ds345.write("*SRE 16") # enables "message available bit"

	ds345.write("AMPL " + str(__AMP__) + "VP") # sets amplitude
	ds345.write("OFFS %f" % __AMP__) # sets offset


	ok = ds345.query("LDWF? 1,%i" % (len(__DATA__) / 2)) # tells machine that 'len(__DATA__) / 2' vector vertices will be sent
	if str.rstrip(str(ok)) != "1": # quit if there's an error loading the waveform
		print "Error loading waveform"
		quit()
	else :
		print "Success loading waveform"

	# creates binary data to send to the generator, including the checksum
	chksum = 0
	input = pack('h', 0)
	for i in range (1, len(__DATA__)):
		input += pack('h', __DATA__[i])
		chksum += __DATA__[i]
		print __DATA__[i]

	print chksum
	input += pack('h', chksum)
	print input

	# write_raw is needed rather than just write, since write will try
	# to treat input as python's unicode type, which may only take
	# 8 bit values
	ds345.write_raw(input)

	ds345.write("FUNC5\n") # sets to arbitrary waveform to produce output
	ds345.write("BCNT %i" % __BURST_COUNT__) # sets burst count
	ds345.write("TRSC 0") # sets trigger source to single (triggers as many as burst count)
	ds345.write("MTYP 5") # sets the type of modulation to burst modulation
	ds345.write("MENA 1") # enables modulation
	ds345.write("TRG*") # triggers burst

run()