import asterisk.config
import sys
from inspect import getmembers
from pprint import pprint

try:
  config = asterisk.config.Config('test/support/etc/asterisk/manager.conf')
except asterisk.config.ParseError as e:
  print("Parse Error line: %s: %s" % (e.line, e.strerror))
  sys.exit(1)
except IOError as e:
  print("Error opening file: %s" % e.strerror)
  sys.exit(1)

# print our parsed output
#for category in config.categories:
#  print('[%s]' % category.name)   # print the current category
#  for item in category.items:
#    print('   %s = %s' % (item.name, item.value))
#foo = Category(config)
#pprint(getmembers(config.categories))
section = config.Category(8888)
