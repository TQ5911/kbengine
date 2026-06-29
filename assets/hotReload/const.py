# -*- coding: utf-8 -*-
_SCRIPTS = '../scripts'


CELL_PATH = [
    f'{_SCRIPTS}/common', 
    f'{_SCRIPTS}/common/Lib', 
    f'{_SCRIPTS}/data', 
    f'{_SCRIPTS}/user_type', 
    f'{_SCRIPTS}/server_common',
    f'{_SCRIPTS}/cell', 
    f'{_SCRIPTS}/cell/interfaces', 
    f'{_SCRIPTS}/cell/components', 
    f'../../kbe/res/scripts',
    f'../../kbe/res/scripts/common', 
    f'../../kbe/res/scripts/common/lib-dynload', 
    f'../../kbe/res/scripts/common/DLLs',
    f'../../kbe/res/scripts/common/Lib', 
    f'../../kbe/res/scripts/common/Lib/site-packages',
    f'../../kbe/res/scripts/common/Lib/dist-packages',
]

BASE_PATH = [
    f'{_SCRIPTS}/common', 
    f'{_SCRIPTS}/common/Lib', 
    f'{_SCRIPTS}/data', 
    f'{_SCRIPTS}/user_type', 
    f'{_SCRIPTS}/server_common',
    f'{_SCRIPTS}/base', 
    f'{_SCRIPTS}/base/interfaces', 
    f'{_SCRIPTS}/base/components', 
    f'../../kbe/res/scripts',
    f'../../kbe/res/scripts/common', 
    f'../../kbe/res/scripts/common/lib-dynload', 
    f'../../kbe/res/scripts/common/DLLs',
    f'../../kbe/res/scripts/common/Lib', 
    f'../../kbe/res/scripts/common/Lib/site-packages', 
    f'../../kbe/res/scripts/common/Lib/dist-packages']

INTERFACE_PATH = [
    f'{_SCRIPTS}/common', 
    f'{_SCRIPTS}/common/Lib', 
    f'{_SCRIPTS}/data', 
    f'{_SCRIPTS}/user_type', 
    f'{_SCRIPTS}/server_common',
    f'{_SCRIPTS}/interface', 
    f'../../kbe/res/scripts',
    f'../../kbe/res/scripts/common', 
    f'../../kbe/res/scripts/common/lib-dynload', 
    f'../../kbe/res/scripts/common/DLLs',
    f'../../kbe/res/scripts/common/Lib', 
    f'../../kbe/res/scripts/common/Lib/site-packages',
    f'../../kbe/res/scripts/common/Lib/dist-packages']

CELLAPP = 'cellapp'
BASEAPP = 'baseapp'
INTERFACE = 'interface'

if __name__ == '__main__':
    print(CELL_PATH)
