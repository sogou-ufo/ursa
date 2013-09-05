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
import uparser as parser
import utils
import mgr
import socket

sys.path.append( conf.getConfig()['path'] ) # add local plugins


class PrHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """
    """
    def sendResponseWithOutput(self, response, contentType, body):
        """
        handles both str and unicode types
        """
        self.send_response(response)
        self.send_header("Content-Type", contentType)

        if response == 301:
            self.send_header("Location", body)
        if not contentType or (contentType.find('image') != 0 and contentType.find('flash')==-1 and contentType.find('audio')==-1 ):
            try:
                body = body.encode(conf.getConfig()['encoding']);
            except UnicodeDecodeError:
                body = body
        self.send_header("Content-Length", len(body))
        self.end_headers()
        if response != 301:
            self.wfile.write(body)

    def urlProxy(self , url , query , reg , truncate_path):
        s = re.search('\$\{(.+)\}' , url) 
        if s:
            name = s.group(1)
            reg = re.sub( '\{.+\}' , '(.+)' , reg )
            m = re.match(reg, truncate_path )
            if m:
                 path = m.group(1)
                 url = url.replace( '${'+name+'}' , path )

        url = url if url.find('?')!=-1 else (url + '?')
        response = urllib2.urlopen(url + query)
        contentType = response.info()['Content-Type']
        body = response.read()
        return (contentType,body)

    def pluginsProxy(self , plugins , params):
        try:
            pkg = __import__( plugins , globals() , locals() , ['main'] , -1 )
            return pkg.main(params)
        except:
            return ('text/html;charset=utf-8' , "Unexpected error:"+ str(sys.exc_info()))
        
    def log_request(self , code , message=None):#disable log
        return ''
    
    def do_GET(self):
        """
        
        Arguments:
        - `self`:
        """
        truncate_path = self.path.split('?')[0].split('#')[0]
        path_items = self.path.split('?')
        query = path_items[1] if len(path_items) > 1 else ''
        response = 200

        serverConfig = conf.getConfig()



        isInServerConfig = False
        if 'proxy' in serverConfig:
            for reg,target in serverConfig['proxy'].items():
                if re.search(re.sub( "\{.+\}$" , "" , reg )  , truncate_path):
                    isInServerConfig = True
                    if target.startswith('http'):#http url
                        contentType,body =self.urlProxy(target , query, reg , truncate_path)
                    elif target.startswith('plugins'):#local plugins
                        contentType , body = self.pluginsProxy(target , query)

        if not isInServerConfig:
            if truncate_path == '/':#default page
                body = mgr.getIndex()
                response,contentType,body = (200 , 'text/html' , body)
            elif truncate_path.endswith('.ut'):#为模版文件
                tplToken = truncate_path.replace('.ut'  , '') [1:]
                body = parser.parseTpl(tplToken)
                body = parser.compileCommon(body , 'local' , True)
                body = parser.compilePlugin(tplToken,body)

                if conf.getConfig().get('type') and conf.getConfig()['type'] == 'mobile':
                    body = body.replace('http://p0.123.sogou.com/u/js/mursa.js' , 'http://ufo.sogou-inc.com/cdn/js/mursa-debug.js')  #mobile project

                if len(body):
                    response,contentType = (200 , 'text/html')
                else:
                    response,contentType,body = (404 , 'text/html' , 'no template called ' + tplToken)
            elif truncate_path.endswith('.m'):#为模版管理
                tplToken = truncate_path.replace('.m' , '')[1:]
                tpl = parser.parseTpl(tplToken)
                if len(tpl):
                    body = mgr.getPage(tplToken)
                    response,contentType,body = (200,'text/html' , body)
                else:
                    response,contentType,body = (404,'text/html' , 'Error finding tpl file.')
            else:
                response, contentType, body = self.server_static(truncate_path) 
        self.sendResponseWithOutput(response , contentType , body)

    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        body = self.rfile.read(length)
        body = utils.queryToDict(body)
        tpl = body['tpl']
        try:
            data = json.loads(body['data'])
            mgr.setData( tpl , data )
            self.sendResponseWithOutput( 301 , 'text/html' , '/' + tpl + '.ut' )
        except ValueError:  
            self.sendResponseWithOutput( 200 , 'text/html' , 'Json format error' )
        except:
            raise
        
           
        

    def server_static(self,file_path):
        file_path = '.' + file_path
        if not os.path.exists(file_path):
            return (404, 'text/html', 'no such file.')
    
        if os.path.isfile(file_path):
            stat_result = os.stat(file_path)    
            mime_type, encoding = mimetypes.guess_type(file_path)

            if not mime_type or (mime_type.find('image')==0 or mime_type.find('flash')!=-1 or mime_type.find('audio')!=-1):
                f = open(file_path , 'rb')
                fcontent = f.read()
            else:
                f = codecs.open(file_path, "rb" , conf.getConfig()['encoding'])
                fcontent = parser.compileCommon(f.read() , 'local' , True)
            try:
                return (200, mime_type, fcontent)
            finally:
                f.close()
            
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
    try:
        httpd = BaseHTTPServer.HTTPServer(('', port), handler_class)
        log.success('server in http://localhost:' + str(port) )
        httpd.serve_forever()
    except (KeyboardInterrupt , SystemExit):
        log.log("^C received, shutting down")
        httpd.socket.close()
    except socket.error:
        log.error('Maybe port ' + str(port) + ' already in use')
        log.error('You can try another port by use "ursa start 8234"')
        raise
        sys.exit(1)
        


  
