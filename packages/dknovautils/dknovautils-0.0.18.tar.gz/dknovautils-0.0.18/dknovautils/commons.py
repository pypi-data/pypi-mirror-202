from dknovautils.dk_imports import *
# import dknovautils as dku


some_demo_d=1

def write_async():
    pass


def dtprint(s: str):
    print(s)


def iprint(obj):
    iprint_info(obj)


def iprint_trace(obj):
    print("[%s+08:00][TRACE][%s]" % (
        datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%dT%H:%M:%S.%f")[0:23],
        obj

    ))


def iprint_info(obj):
    print("[%s+08:00][INFO][%s]" % (
        datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%dT%H:%M:%S.%f")[0:23],
        obj

    ))


def iprint_warn(obj):
    print("[%s+08:00][WARNING][%s]" % (
        datetime.fromtimestamp(time.time()).strftime(
            "%Y-%m-%dT%H:%M:%S.%f")[0:23],
        obj

    ))


# _myCntInfos = {}

'''

class NoteItem(val ctime: Long, val msg: String?, val cnt: Long, val useTime: Long?) {

  val ctimeStr get() = AT.sdf_logger().format(Date(ctime))
}

class MyCntInfo(val title: String) {
  var cnt: Long = 0
  var items: LinkedList<NoteItem> = LinkedList()
  var utime: Long = 0

  val utimeStr get() = AT.sdf_logger().format(Date(utime))

}

'''


@dataclass
class NoteItem:
    ctime: int
    cnt: int
    msg: str = None   # 这个字段是没有缺省值的
    useTime: int = None

    def ctimeStr(self) -> str:

        return 0 * 0


class DkCntInfoUtils(object):

    @staticmethod
    def recordCnt(_key, _cnt=1, _msg: str = None, _useTime: int = None):
        pass

    pass
