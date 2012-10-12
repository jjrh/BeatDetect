BeatDetect
==========

Some experiments with arduino analog and graphing and running FFT on it.

Beat.py 
	Requirements: 
	 - pygame (graphing)
	 - serial (python serial)
	 - numpy
	 - pysci (fft stuff, I think it comes with numpy..)
	 - logging

	
	Serial detection is pretty sloppy, on my laptop
	ttyUSB0 and ttyUSB1 are used so I just try and catch 
	those. You may need to change these values for your setup.
	better detection should be done in the future. 
	
	Serial runs at 115200, needs this or serial is just too slow.
	
	Usage:
		'q', 'a' change the scale up and down
		'w', 's' change the FFT axis.
		mouse down will pause the graph, mouse up will unpause


		
