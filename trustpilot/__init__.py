from importlib import metadata


try:
    VERSION = metadata.version("trustpilot")
except:
    VERSION = "unknown"
