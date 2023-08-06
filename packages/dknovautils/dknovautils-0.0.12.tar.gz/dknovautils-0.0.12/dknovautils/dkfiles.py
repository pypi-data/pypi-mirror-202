
from commons import *


_debug = False


class DkPyFiles(object):

    @staticmethod
    def f_remove_comments_v1(py: str) -> str:
        assert py is not None, 'err5242'

        # 注意ln已经有末尾的回车符 最好替换成\n方便后续处理 rstrip 将去掉末尾的回车符

        lns = '\n'.join(ln.rstrip() for ln in py.splitlines())

        if _debug:
            print(lns)
            print("=====")

        fr_single_a = r'\n\s*#.*'
        pattern = re.compile(fr_single_a)
        lns = re.sub(pattern, "", lns)  # 查找匹配 然后替换            

        # 首行开始的文本不会被替换掉，因为前方没有回车符
        fr_multi = r'(?s)""".*?"""'
        pattern = re.compile(fr_multi)
        lns = re.sub(pattern, "", lns)  # 查找匹配 然后替换

        _removeAst = True
        if _removeAst:
            fr_single_a = r'\n\s*assert\s.+'
            pattern = re.compile(fr_single_a)
            lns = re.sub(pattern, "", lns)             

        if _debug:
            print(lns)

        return lns
