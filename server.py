#!/usr/bin/env python

import glob
import os
import re
import web

from Cheetah.Template import Template

urls = (
	'/twinings/',		'html_server',
	'/twinings/(.*)',	'data_server'
)

type = {
	'.css'	: 'text/css',
	'.gif'	: 'image/gif',
	'.jpg'	: 'image/jpeg',
	'.js'	: 'text/javascript',
	'.png'	: 'image/png'
}

template = Template( file = 'html/index.html' )
pattern = re.compile( '.*\((.*) (.*)\).*' )
stem = os.path.join( 'twinings', 'image' )

class image( object ):
	def __init__( self, path ):
		base = os.path.basename( path )
		match = pattern.search( path )

		self.path = os.path.join( stem, base )
		self.thumb = os.path.join( stem, 'thumb', base )
		self.date = match.group( 1 )
		self.time = match.group( 2 )

	def __cmp__( self, other ):
		return cmp( self.path, other.path )

class html_server:
	def GET( self ):
		image_list = [ image( i ) for i in glob.glob( 'html/image/*.jpg' ) ]
		image_dict = {}

		for i in image_list:
			image_dict.setdefault( i.date, [] ).append( i )

		template.image_dict = image_dict
		print template

class data_server:
	def GET( self, path ):
		full = os.path.join( 'html', path )

		if not os.path.isfile( full ):
			web.notfound()
			return

		extension = os.path.splitext( path )[ 1 ]
		web.header( 'Content-Type', type[ extension ] )
		print open( full, 'rb' ).read()

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
