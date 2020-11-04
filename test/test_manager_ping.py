#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:

import asterisk.manager

manager = asterisk.manager.Manager()
manager.connect("172.25.0.101")
manager.login('pyst2', '5kcn4MCVTk6qCrdq')

assert manager.connected()
assert manager.ping()
