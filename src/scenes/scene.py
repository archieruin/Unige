from src.events_listener import EventsListener


class Scene(object):

    def draw(self, screen):
        raise NotImplementedError

    def update(self, dt):
        raise NotImplementedError

    def handle_events(self):
        raise NotImplementedError