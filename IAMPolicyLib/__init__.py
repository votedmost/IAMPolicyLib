#!/usr/bin/env python

import sys
import os
import json
from collections import namedtuple

# TODO - add constructors so that PolicyStatement can take instance of bucket,
#        queue, etc instead of relying on full ARN

DEFAULT_DEFINITION_PATH = "~/.virtualenvs/_default/lib/python2.7/site-packages/botocore/data/aws/"

class Policy(object):
    def __init__(self, *args):
        self.statements = args
    def __str__(self):
        return json.dumps({ 'Statements' : [ '%s' ] },indent=2) % \
                          ','.join([str(s) for s in self.statements ])

class PolicyStatement(object):
    def __init__(self, resource, actions, effect='Allow'):
        self.effect = effect
        self.resource = resource
        self.actions = actions
        # TODO - how to validate actions is list?
    
    def __str__(self):
        return json.dumps({ k.title(): v for k,v in self.__dict__.iteritems()}, indent=4)

def build_actions():
    definition_path = os.environ.get("DEFINITION_PATH",DEFAULT_DEFINITION_PATH)
    topdir = os.path.expanduser(definition_path)
    gen = os.walk(topdir)
    gen.next()
    actionDict = {}
    for thing in gen:
        filename = os.path.join(thing[0],thing[2][0])
        service_name = os.path.split(thing[0])[1]
        service = json.load(open(filename))
        actionDict[service_name] = service['operations'].keys()
    Actions = namedtuple('Actions',actionDict.keys())
    for k, v in actionDict.iteritems():
        setattr(Actions,k,namedtuple('%s_actions'%k,v))
        for action_name in v:
            setattr(getattr(Actions,k),action_name,"%s:%s" % (k,action_name))
        
    return Actions

Actions = build_actions()

