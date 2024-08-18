from backgroundprovider.base import BackgroundProvider


class FastAPIBackgroundProvider(BackgroundProvider):
    def __init__(self, app):
        self.app = app

    def add_task(self, function, *args, **kwargs):

        return self.app.add_task(function, *args, **kwargs)
