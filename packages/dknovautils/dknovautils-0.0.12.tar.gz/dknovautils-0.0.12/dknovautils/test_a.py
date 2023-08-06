"""

测试注释1

"""


# 单行注释1
from commons import *
from dkfiles import DkPyFiles

dtprint("abc")

"""

测试注释2

"""

"""

测试注释3

"""


def ftest01():
    """

    测试注释4

    """

    assert 1 == 1, 'err5162'
    fp = r'F:\DIKI\DIKIETC\ADEV\learn\LearnPython\PythonBook\dknovautils\dknovautils\test_a.py'

    jsonstr = Path(fp).read_text(encoding='utf8')

    # 这是单行注释2
    fp2 = DkPyFiles.f_remove_comments_v1(jsonstr)
    print(fp2)


ftest01()
