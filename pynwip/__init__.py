import wip as _wip

class Figure():
    def __init__(self):
        _wip.wipinit()

    def __del__(self):
        # This is an alias to cpgend(), possibly update in the future to this?
        _wip.wipclose()
