import uvicorn

from . import settings

__version__ = "0.9.0"


def run():
    uvicorn.run(
        "ldap_ui.app:app",
        log_level="info",
        host="127.0.0.1" if settings.DEBUG else None,
        port=5000,
    )
