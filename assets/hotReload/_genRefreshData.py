import sys

gen_str = '''
import gameglobal
import gamerefresh
gamerefresh.refreshData(TAR_GET)
if gameglobal.isBootstrap:
    gameglobal.localBaseApp.notifyInterfaceDataReload(TAR_GET)
'''

if __name__ == '__main__':
    args = sys.argv[1:]
    strs = ["'{}'".format(i) for i in args]
    strs = ','.join(strs)
    strs = '[{}]'.format(strs)
    final_str = gen_str.replace('TAR_GET', strs)
    with open('._refreshData.py', 'w') as fw:
        fw.write(final_str)

