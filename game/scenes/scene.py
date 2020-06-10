
class Scene(object):

    def __init__(self, gsm):
        self._gsm = gsm

    def draw(self, screen):
        raise NotImplementedError

    def update(self, dt):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError
