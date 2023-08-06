
from dknovautils.commons import *

DkAppVer = '0.0.18'
_unknow_err = '_unknow_err4035'


assert some_demo_d==1
print('debug8997 ok')

class AT(object):

    @staticmethod
    def fepochMillis() -> int:
        millisec = int(AT.fepochSecs() * 1000)
        return millisec

    @staticmethod
    def fepochSecs() -> float:
        return time.time()

    '''
        # dd/mm/YY H:M:S
    dts = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dts)

    # 20200101T120000
    dts = now.strftime("%Y%m%dT%H%M%S")
    print("date and time =", dts)
    
    
    '''

    @staticmethod
    def sdf_logger():
        pass

    @staticmethod
    def sdf_logger_fomrat_datetime(dt: int = None) -> str:
        # "yyyy-MM-dd HH:mm:ss"

        if dt is not None:
            dt = datetime.fromtimestamp(dt/1000, tz=None)
        else:
            dt = datetime.now()

        dts = dt.strftime("%Y-%m-%d %H:%M:%S")

        return dts

    @staticmethod
    def assert_(b: bool, s: str):
        # todo 改成完善的形式
        assert b, _unknow_err if s is None else s
        pass

    @staticmethod
    def astTrace(b: bool, s: str):
        '''在prod中完全不需要的'''
        AT.assert_(b, s)

    VERSION = DkAppVer
