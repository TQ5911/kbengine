import sys
import os
from common import utils
from classes import py_mod_gen, py_mod_types_xml_gen, py_interface_gen


def gen_user_type(mod_name):
    if mod_name[0].islower():
        print('ModName must start with a capital letter')
        sys.exit(1)

    _pmg = py_mod_gen.PyModGen(mod_name)
    _pmg.gen()

    _pmtxg = py_mod_types_xml_gen.PyModTypesXmlGen(mod_name)
    _pmtxg.gen_xml()


def gen_interface(mod_name):
    _pig = py_interface_gen.PyInterfaceGen(mod_name)
    _pig.gen()


def main():
    print('Hello, world!')
    print(sys.argv)
    if len(sys.argv) < 3:
        print('Usage: forge.py <type> <ModName>')
        sys.exit(1)

    print(os.environ['KBE_ASSETS'])
    _mod_name = sys.argv[2]
    _type = sys.argv[1]
    if _type == 'user_type':
        gen_user_type(_mod_name)

    elif _type == 'interface':
        gen_interface(_mod_name)


if __name__ == '__main__':
    main()


