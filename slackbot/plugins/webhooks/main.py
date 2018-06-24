from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import settings


class HomePagePlugin(WillPlugin):

    @route("/healthz")
    def homepage_listener(self):
        return 'OK'

    @respond_to("(what is|what's) your (website|url)")
    def what_is_website(self, message):
        self.reply("It's %s" % settings.PUBLIC_URL)
