#!/usr/bin/env python
#-*- coding:utf-8 -*-

import BaseHTTPServer
import SimpleHTTPServer

import mimetypes
import sys
import os
import re
import codecs
import json
import urllib2
import urllib

import conf
import log
import parser


class PrHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    """
    def sendResponseWithOutput(self, response, contentType, body):
        """
        handles both str and unicode types
        """
        self.send_response(response)
        self.send_header("Content-Type", contentType)
        self.send_header("Content-Length", len(body))
        if response == 301:
            self.send_header("Location", body)
        self.end_headers()
        if response != 301:
            self.wfile.write(body)

    def urlProxy(self , url):
        response = urllib2.urlopen(url)
        contentType = response.info()['Content-Type']
        body = response.read()
        return (contentType,body)

    def pluginsProxy(self , plugins , params):
        try:
            exec("from " + plugins+" import main")
            return main(params)
        except:
            return ('text/html;charset=utf-8' , "Unexpected error:"+ str(sys.exc_info()))
        

    
    def do_GET(self):
        """
        
        Arguments:
        - `self`:
        """
        truncate_path = self.path.split('?')[0].split('#')[0]
        path_items = self.path.split('?')
        response = 200


        serverConfig = conf.getConfig()

        isInServerConfig = False
        for reg,target in serverConfig.items():
            if re.search(reg , truncate_path):
                isInServerConfig = True
                if target.startswith('http'):#http url
                    contentType,body =self.urlProxy(target)
                elif target.startswith('plugins'):#local plugins
                    path = ''
                    if( len(path_items) >1 ):
                        path = path_items[1]
                    contentType , body = self.pluginsProxy(target , path)

        if not isInServerConfig:
            print truncate_path
            if truncate_path.endswith('.do'):#为模版文件
                tplToken = truncate_path.replace('.do'  , '') 
                tplToken = tplToken[1:]
                body = parser.parse(tplToken)
                
                if len(body):
                    response,contentType = (200 , 'text/html')
                else:
                    response,contentType,body = (404 , 'text/html' , 'no template called ' + tplpath)
            else:
                response, contentType, body = self.server_static(truncate_path) 
        self.sendResponseWithOutput(response , contentType , body)
           
        

    def server_static(self,file_path):
        file_path = '.' + file_path
        if not os.path.exists(file_path):
            return (404, 'text/html', 'no such file, may be your forget add /doc/, for example "/doc/' + file_path + '"')
    
        if os.path.isfile(file_path):
            stat_result = os.stat(file_path)    
            mime_type, encoding = mimetypes.guess_type(file_path)

            file = open(file_path, "rb")
            try:
                return (200, mime_type, file.read())
            finally:
                file.close()
            
        elif os.path.isdir(file_path):
            if file_path.endswith('/'):
                index_file = os.path.join(file_path, 'index.html')
                if os.path.exists(index_file):
                    return (200, 'text/html', open(index_file).read())
                else:
                    return (200 , 'text/html; charset=utf-8' , self.list_directory(os.path.abspath(file_path)).read().encode('utf-8')[150:])
            else:
                return (301, 'text/html', file_path + '/')
        else:
            pass







def run(port = 8150 , handler_class = PrHandler):
    httpd = BaseHTTPServer.HTTPServer(('', port), handler_class)
    log.success('server in http://localhost:' + str(port) )
    httpd.serve_forever()
    '''try:
        httpd = BaseHTTPServer.HTTPServer((conf.getPath(), port), handler_class)
        print 'server in http://localhost:' + str(port) 
        httpd.serve_forever()
    except socket.error:
        log.error('Maybe port ' + str(port) + ' already in use')
        log.error('You can try another port by use "ursa start 8234"')
        sys.exit(1)'''
        


  
