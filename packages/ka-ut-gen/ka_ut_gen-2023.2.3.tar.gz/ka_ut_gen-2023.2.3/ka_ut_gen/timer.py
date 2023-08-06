# coding=utf-8

from datetime import datetime
# import pendulum

from typing import Any

from ka_ut_com.com import Com
from ka_ut_com.log import Log

from ka_ut_obj.dic import Dic
from ka_ut_obj.arr import Arr


class Timestamp:

    @staticmethod
    def sh_elapse_time_sec(
            end: Any,
            start: None | Any) -> None | Any:
        if start is None:
            return None
        return end.timestamp()-start.timestamp()


class Timer:
    """ Timer Management
    """
    @staticmethod
    def sh_task_id(
            class_id: str, function_id: None | str) -> None | str:
        """ start Timer
        """
        package = Com.pacmod_curr['package']
        module = Com.pacmod_curr['module']
        return Arr.join_filter_none(
            [package, module, class_id, function_id], '.')

    @classmethod
    def start(
            cls, class_id: str, function_id: None | str) -> None:
        """ start Timer
        """
        task_id = cls.sh_task_id(class_id, function_id)
        Dic.set(Com.d_timer, task_id, datetime.now())
        # Dic.set(Com.d_timer, keys, pendulum.now())

    @classmethod
    def end(cls, class_id: str, function_id: None | str) -> None:
        """ end Timer
        """
        task_id = cls.sh_task_id(class_id, function_id)
        start = Dic.get(Com.d_timer, task_id)
        end = datetime.now()

        # end = pendulum.now()
        # elapse_time = end-start
        elapse_time_sec = Timestamp.sh_elapse_time_sec(end, start)
        # elapse_time_sec = end.diff(start).in_words()

        msg = f"{task_id} elapse time [sec] = {elapse_time_sec}"

        Log.info(msg, stacklevel=2)
