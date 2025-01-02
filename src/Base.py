import platform

CT_VERSION = "1.0.0"
CT_ARCHITECTURE = "x64"
CT_DEBUG = True
CT_DIST = False
CT_RELEASE = False

CT_PLATFORM_WINDOWS = platform.system() == "Windows"
CT_PLATFORM_LINUX = platform.system() == "Linux"
CT_PLATFORM_MAC = platform.system() == "Darwin"
