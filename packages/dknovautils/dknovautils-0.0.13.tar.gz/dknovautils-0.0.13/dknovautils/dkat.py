

_unknow_err = '_unknow_err4035'


_version = "0.0.13"


class AT(object):

    @staticmethod
    def assert_(b: bool, s: str):
        # todo 改成完善的形式
        assert b, _unknow_err if s is None else s
        pass

    @staticmethod
    def astTrace(b: bool, s: str):
        '''在prod中完全不需要的'''
        AT.assert_(b, s)

    VERSION = _version
