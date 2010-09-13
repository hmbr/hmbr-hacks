#!/usr/bin/env python
from claro_urls import *
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import os.path
import logging
import ConfigParser
import getopt
import sys

__author__ = "Helder Maximo Botter Ribas"
__copyright__ = "Copyright 2010"
__credits__ = ["Helder Ribas"]
__license__ = "GPL"
__version__ = "0.1"

logger = logging.getLogger("claro_web")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

class web:
    """
    classe para acessar a conta da claro da web utilizando python
    """
    def __init__(self):
        self.history = False
        self.logado = False
        cookieProcessor = urllib2.HTTPCookieProcessor();
        self.opener = urllib2.build_opener(cookieProcessor);
    
    def useHistory(self,value):
        self.history = value
        
    def login(self,ddd,telefone,password):
        """
        define o usuario no site
        """
        self.ddd = ddd
        self.telefone = telefone
        self.senha = password
        self.ntc = '%s%s' % (self.ddd,self.telefone)
    
    def loging(self):
        """
        log no site
        """
        logger.info("logando no site")
        
        #precisa realizar um primeiro acesso
        first = urllib.urlencode( { 'nct': self.ntc} )
        self.opener.open(CLARO_URL+CLARO_SITE, first)
        login =urllib.urlencode( { 'userVO.accessType': 'ADMINISTRADOR',
                           'DDD':self.ddd,
                           'celNumber':self.telefone,
                           'userVO.password':self.senha
                           } )
        
        #realiza o login
        self.opener.open(CLARO_URL+CLARO_LOGON, login)
	self.logado = True

    def getRawPage(self,site,params=None):
        if self.history:
            fname = "/tmp/" + site.replace("/","_")
            if os.path.isfile(fname):
                logger.info("reaproveitando historico")
                f = open(fname)
                retorno = f.read()
                f.close()
        if not('retorno' in locals()):   
            if (self.logado == False):
                self.loging()
        
            if params == None:
                page = self.opener.open(CLARO_URL+site)
            else:
                page = self.opener.open(CLARO_URL+site,params)
            retorno = page.read()
            retorno = retorno.decode('iso8859').encode("utf8")

        if self.history:
            f = open(fname,'w')
            f.write(retorno)
            f.close
        return retorno

    def getRawFile(self,site,params=None):
        if self.history:
            fname = "/tmp/" + site.replace("/","_")
            if os.path.isfile(fname):
                logger.info("reaproveitando historico")
                f = open(fname)
                retorno = f.read()
                f.close()
        if not('retorno' in locals()):   
            if (self.logado == False):
                self.loging()
        
            if params == None:
                page = self.opener.open(CLARO_URL+site)
            else:
                page = self.opener.open(CLARO_URL+site,params)
            retorno = page.read()
        
        if self.history:
            f = open(fname,'w')
            f.write(retorno)
            f.close
        return retorno


    def callSoup(self,html):
        return BeautifulSoup(html,convertEntities=BeautifulSoup.XML_ENTITIES)
        
    def getGerenciamentoUltimasFaturasDue(self):
        """
        lista as datas disponiveis dos boletos antigos
        """
        soup = self.callSoup(self.getRawPage(CLARO_GERENCIAMENTO_ULTIMAS_FATURAS))
        dues = []
        select = soup.find('select',{'name':'billDueDate'}).parent
        for due in select.findAll("option"):
            dues.append(due['value'])
        return dues
    
    def getFaturaPdf(self,due):
        param = urllib.urlencode( { 'billDueDate': due,'name':'downloadPDFForm'})
        return self.getRawFile(CLARO_GERENCIAMENTO_PDF,param)
    
    def getUltimaFaturaPdf(self):
        return self.getFaturaPdf(self.getGerenciamentoUltimasFaturasDue()[0])

def help():
    print """
    Usage : script [OPTIONS]
    [-h | --help] display this message
    [-c | --conf] file.cfg configuration file
    """

if __name__ == '__main__':
    config_file = "user.cfg"
    try:
		 opts,args = getopt.getopt(sys.argv[1:],"hc:",["help","conf="])
    except getopt.GetoptError, err:
	print str(err)

    for o, a in opts:
        if o in ("-c", "--conf"):
	     config_file = a
        if o in ("-h", "--help"):
	     help();
             sys.exit()
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    web = web() 
    web.login(config.get("claro","ddd"),
		    config.get("claro","telefone"),
		    config.get("claro","senha"))
    f = open("fatura.pdf",'w')
    f.write(web.getUltimaFaturaPdf())
    f.close


