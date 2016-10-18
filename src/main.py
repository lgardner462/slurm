#!/usr/bin/python

########################################################################################################
########################################################################################################
########################################################################################################

### PACKAGES ###########################################################################################

import os
import sys

from src.bottle import route, get, post, request, response, static_file, SimpleTemplate, url, template, redirect

from config.dirs import ROOT_DIR

from scripts.states_iterator import *

### APACHE #############################################################################################

os.chdir(os.path.dirname(__file__))
sys.path.insert(1, os.path.dirname(__file__))

### RUNNING AS MAIN ####################################################################################

if __name__ == "__main__":
    print("Run app through wrapper.")
    print("Exiting...")
    exit()

### DEV MODE ###########################################################################################

devMode = False

def setDevMode(d):
    global devMode
    if type(d) is bool:
        devMode = d
    print("###############")
    print("DEV MODE ACTIVE")
    print("###############")


def getDevMode():
    global devMode
    return devMode

### FOR CSS READING IN TEMPLATES #######################################################################

SimpleTemplate.defaults["url"] = url

### DIRECTORY ##########################################################################################

# dir = "foo"
# if the directory doesn't exist, create it
# if not os.path.exists(dir):
#     os.makedirs(dir)

### SMTP ###############################################################################################

# receivers = []
#
# def smtpInit(mailTo='', mailFrom='root'):
#     # this is called from the wrapper file
#     # sets the sender and receiver for emails
#     global receivers
#     global sender
#
#     receivers = [mailTo]
#     sender = mailFrom

### STATIC ROUTING ########################################################################################

# CSS
@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    # print("IN STYLESHEETS():", filename)
    return static_file(filename, root='../static/css')

# JAVASCRIPT
@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    # print("IN JAVASCRIPTS():", filename)
    return static_file(filename, root='../static/js')

# IMAGES
@get('/img/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    # print("IN IMAGES():", filename)
    return static_file(filename, root='../static/img')

# FONTS
@get('/fonts/<filename:re:.*\.(eot|ttf|woff|woff2|svg)>')
def fonts(filename):
    # print("IN FONTS():", filename)
    return static_file(filename, root='../static/fonts')

### COOKIE GETTERS/SETTERS #############################################################################

# def getCookie(request):
#     return request.get_cookie("foo") or ""
#
# def setCookie(response, value):
#     response.set_cookie("foo", value)

### ANCHOR ######################################################
def getAnchorCookie(req):
    return req.get_cookie("anchor") or "-1"

def setAnchorCookie(res, anchor):
    res.set_cookie("anchor", str(anchor))

def deleteAnchorCookie(res):
    res.delete_cookie("anchor")

### REQUESTED NODE ##############################################

def getRequestedCookie(req):
    return req.get_cookie("requested") or "-1"

def setRequestedCookie(res, requested):
    res.set_cookie("requested", str(requested))

def deleteRequestedCookie(res):
    res.delete_cookie("requested")

### HELPER METHODS #####################################################################################

def getFileName(scriptName):
    scriptDir = os.path.join(ROOT_DIR, "scripts/")
    return scriptDir + scriptName

def getHostParam(request):
    return request.query.host or None

def getHTMLHeader():
    return '<body style="font-family: Monospace;">'

def getHTMLFooter():
    return '</body>'

def getHTMLWrapper(html):
    return getHTMLHeader() + str(html) + getHTMLFooter()

def hostNotSuppliedMsg():
    return "Please enter the query parameter: 'host'"

########################################################################################################
########################################################################################################
########################################################################################################

#
#
#
# ^^^ FUNCTIONS, SETTINGS ^^^
#
# vvv ROUTES vvv
#
#
#

########################################################################################################
###################################### NODE ROUTES START ###############################################
########################################################################################################

# @route('/reinstall')
# def reinstall_node():
#     host = getHostParam(request)
#
#     cmd = "{0} {1}".format(getFileName("reinstall"), host)
#
#     if host:
#         result = getHTMLWrapper(commands.getstatusoutput(cmd)[1])
#         return result
#
#     return hostNotSuppliedMsg()


########################################################################################################
########################################################################################################

# @route('/default')
# def default_node():
#     host = getHostParam(request)
#
#     cmd = "{0} {1}".format(getFileName("default"), host)
#
#     if host:
#         result = getHTMLWrapper(commands.getstatusoutput(cmd)[1])
#
#         return result
#
#     return hostNotSuppliedMsg()


########################################################################################################
########################################################################################################

@route('/slurm')
def slurm_nodes():

    outputs = {}
    scontrol_result = ""

    anchor = getAnchorCookie(request)
    deleteAnchorCookie(response)

    requested = getRequestedCookie(request)
    deleteRequestedCookie(response)

    if getDevMode():
        from pickle import load

        if requested:
            nodelist_file = scontrol_file = None
            try:
                nodelist_file = open(os.path.join(ROOT_DIR, "local_example.p"), 'rb')
                scontrol_file = open(os.path.join(ROOT_DIR, "local_scontrol.p"), 'rb')
            except IOError:
                pass

            if nodelist_file:
                outputs = load(nodelist_file) or {}
                nodelist_file.close()

            if scontrol_file:
                scontrol_result = load(scontrol_file) or "File not read"
                scontrol_file.close()

    else:
        if requested:
            outputs = getOutputsDict()
            scontrol_result = getScontrol(requested)


    return template('slurm', outputs=outputs, anchor=anchor, requested=requested, scontrol_result=scontrol_result)

########################################################################################################
########################################################################################################

@post('/node')
def scontrol_show_node():

    anchor = request.forms.get('anchor') or -1
    setAnchorCookie(response, anchor)

    requested = request.forms.get('node') or -1
    setRequestedCookie(response, requested)

    redirect('/slurm#' + anchor)

########################################################################################################
###################################### NODE ROUTES END #################################################
########################################################################################################




########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################