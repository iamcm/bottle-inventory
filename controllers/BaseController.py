import bottle
import datetime

class BaseController:
    """
    Base Controller to allow for sharing common data and tasks among views
    """
    #def __init__(self):
    #    self.viewdata = {
    #        'date':datetime.datetime.now().strftime('%Y'),
    #    }

    #def _template(self, template):
    #    return bottle.template(template, vd=self.viewdata)