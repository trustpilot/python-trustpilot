import pkg_resources

try:
    VERSION = pkg_resources.get_distribution("trustpilot").version
except:
    VERSION = "unknown"
