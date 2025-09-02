import os
from common import utils


__TEMP__ = """
    <{0}_DATA_INFO> FIXED_DICT
        <implementedBy>     {1}Info.{1}Instance    </implementedBy>
        <Properties>
            <tmp>
                <Type>  ARRAY <of>  UINT8 </of>   </Type>
            </tmp>
        </Properties>
    </{0}_DATA_INFO>
"""


class PyModTypesXmlGen(object):
    def __init__(self, mod_name):
        self.mod_name = mod_name

    def get_xml_path(self):
        return os.path.join(os.environ['KBE_ASSETS'], 'scripts', 'entity_defs', 'types.xml')

    def get_upper_name(self):
        """
        ModName -> MOD_NAME
        """
        return utils.get_upper_name(self.mod_name)

    def gen_xml(self):
        _path = self.get_xml_path()
        _tmp_path = _path + '.tmp'
        with open(_path) as fr, open(_tmp_path, 'w') as fw:
            _lines = fr.readlines()

            _root_line = -1
            for i, line in enumerate(_lines):
                if '</root>' in line:
                    _root_line = i

            _UPPER = self.get_upper_name()
            _insert_content = __TEMP__.format(_UPPER, self.mod_name)
            _lines.insert(_root_line, _insert_content)
            _write_content = ''.join(_lines)

            fw.write(_write_content)

        os.rename(_tmp_path, _path)
        
