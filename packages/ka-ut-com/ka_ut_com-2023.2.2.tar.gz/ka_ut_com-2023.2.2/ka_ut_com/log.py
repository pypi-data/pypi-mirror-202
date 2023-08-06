# coding=utf-8

from ka_ut_com.com import Com


class Eq:
    """ Manage Equate Class
    """
    @staticmethod
    def sh(key, value):
        """ Show Key, Value as Equate
        """
        return f"{key} = {value}"


class Log:
    """Logging Class
    """

    class Eq:
        @staticmethod
        def debug(key, value):
            Log.debug(Eq.sh(key, value), stacklevel=3)

        @staticmethod
        def error(key, value):
            Log.error(Eq.sh(key, value), stacklevel=3)

        @staticmethod
        def info(key, value):
            Log.info(Eq.sh(key, value), stacklevel=3)

        @staticmethod
        def warning(key, value):
            Log.warning(Eq.sh(key, value), stacklevel=3)

    @staticmethod
    def debug(*args, **kwargs):
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        Com.Log.debug(*args, **kwargs)

    @staticmethod
    def error(*args, **kwargs):
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        Com.Log.error(*args, **kwargs)

    @staticmethod
    def info(*args, **kwargs):
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        Com.Log.info(*args, **kwargs)

    @staticmethod
    def warning(*args, **kwargs):
        if kwargs is None:
            kwargs = {}
        kwargs['stacklevel'] = kwargs.get('stacklevel', 2)
        Com.Log.warning(*args, **kwargs)

    @staticmethod
    def finished(*args, **kwargs):
        Com.Log.info(
          Com.cfg.profs.msgs.finished)
        Com.Log.info(
          Com.cfg.profs.msgs.etime.format(etime=Com.ts_etime))
