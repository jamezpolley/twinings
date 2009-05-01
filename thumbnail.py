#!/usr/bin/env python

import os
import Image
from pyinotify import WatchManager, Notifier, EventsCodes, ProcessEvent

thumb_size = 64, 64
thumb_path = 'thumb'
watch_path = 'html/image'

def thumbnail( in_path, out_path ):
	image = Image.open( in_path )
	image.thumbnail( thumb_size )
	image.save( out_path, 'JPEG', quality = 60 )

class process( ProcessEvent ):
	def process_IN_CLOSE_WRITE( self, event ):
		out_path = os.path.join( event.path, thumb_path, event.name )
		thumbnail( os.path.join( event.path, event.name ), out_path )
		print "Wrote thumbnail to '%s'" % out_path

if __name__ == '__main__':
	watch = WatchManager()
	notifier = Notifier( watch, process() )
	descriptor = watch.add_watch( watch_path, EventsCodes.IN_CLOSE_WRITE )

	while True:
		try:
			notifier.process_events()

			if notifier.check_events():
				notifier.read_events()
		except KeyboardInterrupt:
			notifier.stop()
			break
