#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import configparser
import os.path

def readcfg(list):
    config = configparser.ConfigParser()
    config.read('client_config.ini')
    for item in list:
        config = config[item]
    return str(config)

def connect(host, port):
    try :
        connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connexion_avec_serveur.connect((host, int(port)))
        return connexion_avec_serveur
    except:
        return "err1"


def send(msg_a_envoyer,connexion_avec_serveur ):
    msg_a_envoyer = msg_a_envoyer.encode('utf-8')
    connexion_avec_serveur.send(msg_a_envoyer)

def recv(connexion_avec_serveur):
    msg_recu = connexion_avec_serveur.recv(1024)
    stringdata = msg_recu.decode('utf-8')
    return stringdata

def disconnect(connexion_avec_serveur):
    connexion_avec_serveur.close()

def login(username, password):
    connexion_avec_serveur = connect(readcfg(['SOCKET','host']), readcfg(['SOCKET','port']))
    if connexion_avec_serveur == "err1":
        return "err1"
    else:
        msg_a_envoyer = '"' + 'login' + '"' + '-' + '"' + username + '"' + '-' + '"' + password + '"'
        send(msg_a_envoyer,connexion_avec_serveur)
        stringdata = recv(connexion_avec_serveur)
        disconnect(connexion_avec_serveur)
        if stringdata == "logs ok":
            return True
        else:
            return stringdata
def register(username, password, first_name, last_name, email):
    connexion_avec_serveur = connect(readcfg(['SOCKET','host']), readcfg(['SOCKET','port']))
    if connexion_avec_serveur == "err1":
        return "err1"
    else:
        msg_a_envoyer = '"' + 'register' + '"' + '-' + '"' + username + '"' + '-' + '"' + password + '"' + '-' + '"' + first_name + '"' + '-' + '"' + last_name + '"' + '-' + '"' + email + '"'
        send(msg_a_envoyer,connexion_avec_serveur)
        stringdata = recv(connexion_avec_serveur)
        disconnect(connexion_avec_serveur)
        if stringdata == "reg ok":
            return True
        else:
            return stringdata


def check_cfg():
    if os.path.exists("client_config.ini") == False:
        config = configparser.ConfigParser()
        config.read('client_config.ini')
        config['SOCKET'] = {'host': 'localhost',
                            'port': '1111'}
        with open('client_config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        config = configparser.ConfigParser()
        config.read('client_config.ini')
        if ('SOCKET' in config) == False:
            os.remove("client_config.ini")
            config['SOCKET'] = {'host': 'localhost',
                                'port': '1111'}
            with open('client_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('host' in config['SOCKET']) == False:
            config['SOCKET']['host'] = 'localhost'
            with open('client_config.ini', 'w') as configfile:
                config.write(configfile)
        if ('port' in config['SOCKET']) == False:
            config['SOCKET']['port'] = '1111'
            with open('client_config.ini', 'w') as configfile:
                config.write(configfile)
