from orbnext import set_color, colors
from will import settings
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

class GadetsPlugin(WillPlugin):

    @respond_to('^set rawblight (?P<color>\w+)')
    def set_light_color(self, message, color):
        """ set rawblight ____ : set light to a color (or off) """
        try:
            if set_color(color):
                self.reply('I have set the light on rawbs desk to {}.'.format(color))
                self.save('rawblight.color', color)
            else:
                self.reply('Something went wrong setting the light to {}'.format(color))
        except Exception as e:
            self.reply('Error sending command: {}'.format(e))

    @respond_to('rawblight status')
    def get_light_color(self, message):
        """ rawblight status : get the current state of the light on robs desk. """
        color = self.load('rawblight.color')
        if color is not None:
            self.reply('The light is currently {}.'.format(color))
        else:
            self.reply('I don\'t know the current status, try setting the color and I will remember.')
