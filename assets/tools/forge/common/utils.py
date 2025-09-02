


def get_upper_name(mod_name):
    """
    ModName -> MOD_NAME
    """

    # split 
    _list = []
    _tmp = ''
    for c in mod_name:
        if c.isupper():
            _list.append(_tmp)
            _tmp = ''

        _tmp += c

    _list.append(_tmp)
    _list = [x.upper() for x in _list if x]
    return '_'.join(_list)

