import cwip

class Figure():
    def __init__(self):
        cwip.wipinit()

    def __del__(self):
        # This is an alias to cpgend(), possibly update in the future to this?
        cwip.wipclose()

    def device(self, device='/xw'):
        cwip.wipdevice(device)

    def box(self, xvars='bcnst', yvars='bcnst'):
        values = cwip.wipgetick()
        cwip.cpgtbox(xvars, values[0], values[1], yvars, values[2], values[3])
        return

    def erase(self):
        cwip.cpgpage()

