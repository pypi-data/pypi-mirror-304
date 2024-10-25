import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

class LatexPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "assets")
        toolkit.add_resource("assets", "latex")
