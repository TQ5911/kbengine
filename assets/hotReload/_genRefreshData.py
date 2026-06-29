import sys

gen_str = '''
import gameglobal
import gamerefresh
gamerefresh.refreshData(TAR_GET)
if gameglobal.isBootstrap:
    gameglobal.localBaseApp.notifyInterfaceDataReload(TAR_GET)
'''

if __name__ == '__main__':
    _args = sys.argv[1:]
    _strs = ["'{}'".format(i) for i in _args]
    _strs = ','.join(_strs)
    _strs = '[{}]'.format(_strs)
    final_str = gen_str.replace('TAR_GET', _strs)
    with open('._refreshData.py', 'w') as fw:
        fw.write(final_str)

