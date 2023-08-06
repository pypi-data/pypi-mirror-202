"""

测试注释1

"""


# 单行注释1
# from dknovautils.commons import *
# from dknovautils.dkfiles import DkPyFiles
# from dknovautils.dkat import AT

from commons import *
from dkfiles import DkPyFiles
from dkat import AT

print("test01 start")

'''

测试注释2

'''

"""

测试注释3

"""


def ftest01():
    '''

    测试注释4

    '''

    assert 1 == 1, 'err5162'

    print(AT.VERSION)
    # AT.assert_(AT.VERSION >= '0.0.18','err5484')

    fp = r'F:\DIKI\DIKIETC\ADEV\learn\LearnPython\PythonBook\dknovautils\dknovautils\test_a.py'

    jsonstr = Path(fp).read_text(encoding='utf8')

    # 这是单行注释2
    fp2 = DkPyFiles.f_remove_comments_v1(jsonstr)
    # print(fp2)

    iprint_info(fp2)

    cstr = AT.sdf_logger_fomrat_datetime()
    print(cstr)


if __name__ == '__main__':
    ftest01()
