#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:

import coverage

cov = coverage.Coverage(config_file='/home/ec2-user/pyst2/.coveragerc.asterisk')
cov.start()

from asterisk.agi import *

agi = AGI()
#agi.verbose(cov.current())
#agi.verbose(foo)
agi.answer()
agi.appexec('DumpChan')

#data = cov.get_data()

agi.set_variable('AGI_TABLE', 'Nothing to See')
agi.set_variable('AGI_RECORD', '234209384092384')
agi.verbose('This is a test!')
#agi.verbose(data)

#agi.hangup()


#manager = asterisk.manager.Manager()
#manager.connect("172.25.0.101")
#manager.login('pyst2', '5kcn4MCVTk6qCrdq')

#response = manager.originate('Local/2000@internal', 3000, application='AGI', data='')
#assert response
#print(response)
#print manager.status()

cov.stop()
foo = cov.save()
print(foo)
