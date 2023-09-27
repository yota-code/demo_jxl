#!/usr/bin/env python3

import os

from cc_pathlib import Path

import cherrypy

https://unix.stackexchange.com/questions/104171/create-ssl-certificate-non-interactively

class Root(object):
    pass       

if __name__ == '__main__':
    root_dir = Path(__file__).resolve()

    cherrypy.config.update( {  # I prefer configuring the server here, instead of in an external file.
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 443,
        'server.ssl_certificate': "cert.pem",
        'server.ssl_private_key': "privkey.pem",
    } )
    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': root,
            'tools.staticdir.index': 'index.html'
        }
    }
    cherrypy.quickstart(Root(), '/', conf)
