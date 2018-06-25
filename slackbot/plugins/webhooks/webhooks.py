from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import settings


class WebhookPlugin(WillPlugin):

    @route("/healthz")
    def homepage_listener(self):
        return 'OK'

    @route('/say', method='POST')
    def repeat_after_me(self):
        api_key = getattr(settings, 'SLACKBOT_API_KEY', None)
        if api_key is not None:
            if self.request.headers.get('Auth') == api_key:
                payload = self.request.json
                words = str(self.request.json.get('words'))
                self.say(words)

    @respond_to("(what is|what's) your (website|url)")
    def what_is_website(self, message):
        """ whats your website: retrive the external URL for the webhook server """
        self.reply("It's %s" % settings.PUBLIC_URL)
