from PIL import Image
import pluggy

from dinky import hookspecs
from dinky.display_configuration import DisplayConfiguration
from dinky.layouts.layout_configuration import BaseLayoutConfiguration

class DashboardManager():
    def __init__(self, layout_configuration: BaseLayoutConfiguration):
        self.pm = pluggy.PluginManager("dinky")
        self.pm.add_hookspecs(hookspecs)
        self.display_configuration: DisplayConfiguration = DisplayConfiguration()
        self.layout_configuration: BaseLayoutConfiguration = layout_configuration

    def register(self, plugin: object, name: str):
        self.pm.register(plugin, name=name)

    def draw_dashboard(self):
        im = Image.new("RGB", (self.display_configuration.width, self.display_configuration.height), (255, 255, 255))
        for plugin in self.pm.get_plugins():
            zone = next(filter(lambda zone: zone.id == self.pm.get_name(plugin), self.layout_configuration.zones))
            draw = plugin.dinky_draw_zone(zone=zone)
            im.paste(draw, (zone.x, zone.y))
        im.save("dashboard.jpg")