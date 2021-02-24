"""Config file"""

# ----- Kiosk
# ----------------------
KIOSK_URL = "url"
KIOSK_KEEP_DATA = "keep_data"
KIOSK_USER_DIR = "/.config/chromium/Default"
KIOSK_USER_DIR_ARG = "--user-data-dir="
KIOSK_LAUNCH_ARGUMENTS = [
    "--no-first-run",
    "--no-sandbox",
    "--enable-file-cookies",
    "--disable-web-security",
    "--ignore-certificate-errors",
    "--kiosk",
    "--noerrdialogs",
    "--enable-features=OverlayScrollbar",
    "--disable-password-manager-reauthentication",
    "--display=:0"
]


# ----- Config file
# ----------------------
CONF_FILE = "conf.json"
INDENT = 2

# JSON attributes
TOKEN = 'token'
CUSTOM_ENDPOINT = 'custom_endpoint'
PORT = "port"

# SERVICES
SERVICES = "services"
KIOSK = "webkiosk"
SUSPEND = "suspend"
SHUTDOWN = "shutdown"
REBOOT = "reboot"


# ----- Commands
# ----------------------
SYSTEM_INFO = "system_info"
SYSTEM_BATTERY_CAPACITY = "system_battery"
SYSTEM_BATTERY_STATUS = "system_status"

# COMMANDS
FEDORA_COMMANDS = {
    SYSTEM_INFO: "uname -a",
    SYSTEM_BATTERY_CAPACITY: "cat /sys/class/power_supply/BATC/capacity",
    SYSTEM_BATTERY_STATUS: "at /sys/class/power_supply/BATC/status",
    REBOOT: 'systemctl reboot',
    SHUTDOWN: 'halt',
    SUSPEND: 'systemctl suspend'
}


# ----- Default config file
# ----------------------
DEFAULT_CONFIG = {
    PORT: 5000,
    SERVICES: [
        REBOOT,
        SHUTDOWN,
        KIOSK
    ],
    KIOSK: {
        KIOSK_URL: 'http://example.com/',
        KIOSK_KEEP_DATA: True
    }
}


# ----- Rest api
# ----------------------
ROOT = "/"
HOMEPAGE = '/PyKiosk'
REST_ENDPOINT = '/rest'

# HEADERS
HEADER = {
    'ContentType': 'application/json'
}

# PRE-MADE RESPONSES
RESPONSE_FAILED = {
    'success': False,
    'message': 'Webkiosk error'
}
ERROR_NOT_ENABLED = {
    'success': False,
    'error': 'NotEnabled',
    'message': 'Service not enabled in config file.'
}
ERROR_MISSING_CONFIG = {
    'success': False,
    'error': 'MissingConfig',
    'message': 'Missing config, make sure your config contains "port", "services", "webkiosk" and "url" in webkiosk. Config was not saved.'
}
RESPONSE_SUCCESS = {
    'success': True
}