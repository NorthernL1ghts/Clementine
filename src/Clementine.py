import sys
import threading
import time
import platform
import dearpygui.dearpygui as dpg

CT_VERSION = "1.0.0"
CT_ARCHITECTURE = "x64"
CT_DEBUG = True
CT_DIST = False
CT_RELEASE = False

CT_PLATFORM_WINDOWS = platform.system() == "Windows"
CT_PLATFORM_LINUX = platform.system() == "Linux"
CT_PLATFORM_MAC = platform.system() == "Darwin"

def CT_ASSERT(condition, message):
    assert condition, message

def CT_CORE_ASSERT(condition, message):
    assert condition, message

class ApplicationCommandLineArgs:
    def __init__(self, count=0, args=None):
        self.Count = count
        self.Args = args if args is not None else []

    def __getitem__(self, index):
        CT_CORE_ASSERT(index < self.Count, "Index out of range")
        return self.Args[index]

class ApplicationSpecification:
    def __init__(self, Name="Clementine", Version=CT_VERSION, Width=800, Height=600, Author="NorthernL1ghts", Contact="bizn0rth3rnl1ghts@gmail.com", WorkingDirectory="", CommandLineArgs=None):
        self.Name = Name
        self.Version = Version
        self.Width = Width
        self.Height = Height
        self.Author = Author
        self.Contact = Contact
        self.WorkingDirectory = WorkingDirectory
        self.CommandLineArgs = CommandLineArgs if CommandLineArgs is not None else ApplicationCommandLineArgs()

    def DisplayInfo(self):
        return (f"Application Name: {self.Name}\n"
                f"Version: {self.Version}\n"
                f"Width: {self.Width}\n"
                f"Height: {self.Height}\n"
                f"Author: {self.Author}\n"
                f"Contact: {self.Contact}")

class PerformanceTimers:
    def __init__(self):
        self.m_MainThreadWorkTime = 0.0
        self.m_MainThreadWaitTime = 0.0

    def GetTime(self):
        return time.time()

class DearImGuiLayer:
    def __init__(self):
        self.m_ContextCreated = False

    def CreateContext(self):
        if not self.m_ContextCreated:
            dpg.create_context()
            self.m_ContextCreated = True

    def DestroyContext(self):
        if self.m_ContextCreated:
            dpg.destroy_context()
            self.m_ContextCreated = False

    def CreateViewport(self, title, width, height):
        dpg.create_viewport(title=title, width=width, height=height)

    def Setup(self):
        dpg.setup_dearpygui()

    def ShowViewport(self):
        dpg.show_viewport()

    def Render(self):
        dpg.render_dearpygui_frame()

    def AddMainWindow(self, callback):
        with dpg.window(label="Main Window"):
            dpg.add_text("Hello, Clementine!")
            dpg.add_button(label="Close", callback=callback)

class Application:
    s_Instance = None
    s_MainThread = None
    s_MainThreadID = None
    s_IsRuntime = False

    def __init__(self, specification):
        CT_CORE_ASSERT(Application.s_Instance is None, "Application already exists!")
        self.m_Running = True
        self.m_Specification = specification
        self.m_MainThreadQueue = []
        self.m_MainThreadQueueMutex = threading.Lock()
        self.m_DearImGuiLayer = DearImGuiLayer()
        Application.s_Instance = self
        Application.s_MainThreadID = threading.get_ident()

        if self.m_Specification.WorkingDirectory:
            self.SetCurrentPath(self.m_Specification.WorkingDirectory)

    @staticmethod
    def CreateApplication(args):
        return Application(ApplicationSpecification(CommandLineArgs=ApplicationCommandLineArgs(len(args), args)))

    def GetSpecification(self):
        return self.m_Specification

    def GetSystemConfiguration(self):
        return "System configuration details"

    def GetSystemArch(self):
        return CT_ARCHITECTURE

    def Run(self):
        global g_ApplicationRunning
        g_ApplicationRunning = True

        self.m_DearImGuiLayer.CreateContext()
        self.m_DearImGuiLayer.CreateViewport(self.m_Specification.Name, self.m_Specification.Width, self.m_Specification.Height)
        self.m_DearImGuiLayer.Setup()
        self.m_DearImGuiLayer.ShowViewport()
        self.m_DearImGuiLayer.AddMainWindow(self.Close)

        while self.m_Running:
            self.m_DearImGuiLayer.Render()
            self.ExecuteMainThreadQueue()

        self.m_DearImGuiLayer.DestroyContext()

    def Close(self):
        self.m_Running = False

    def SubmitToMainThread(self, function):
        with self.m_MainThreadQueueMutex:
            self.m_MainThreadQueue.append(function)

    def ExecuteMainThreadQueue(self):
        with self.m_MainThreadQueueMutex:
            for func in self.m_MainThreadQueue:
                func()
            self.m_MainThreadQueue.clear()

    @staticmethod
    def Get():
        return Application.s_Instance

    @staticmethod
    def SetCurrentPath(path):
        import os
        os.chdir(path)

    @staticmethod
    def GetMainThreadID():
        return Application.s_MainThreadID

    @staticmethod
    def IsMainThread():
        return threading.get_ident() == Application.s_MainThreadID

    @staticmethod
    def GetConfigurationName():
        return "DEBUG" if CT_DEBUG else "RELEASE"

    @staticmethod
    def GetPlatformName():
        if CT_PLATFORM_WINDOWS:
            return "Windows"
        elif CT_PLATFORM_LINUX:
            return "Linux"
        elif CT_PLATFORM_MAC:
            return "Mac"
        else:
            return "Unknown"

    def TerminateHotKey(self, key):
        import keyboard
        def on_key_press(event):
            if event.name == key:
                print(f"Key '{key}' pressed. Terminating...")
                self.Close()
                sys.exit()

        keyboard.on_press(on_key_press)

class EntryPoint:
    @staticmethod
    def Main(args):
        while g_ApplicationRunning:
            EntryPoint.InitialiseCore()
            app = Application.CreateApplication(args)
            CT_CORE_ASSERT(app is not None, "Client Application is null!")
            app.TerminateHotKey('esc')  # Set the key you want to use for termination
            app.Run()
            del app
            EntryPoint.ShutdownCore()
        return 0

    @staticmethod
    def InitialiseCore():
        # Core initialization logic
        print("Core initialization complete")

    @staticmethod
    def ShutdownCore():
        # Core shutdown logic
        print("Shutting down core")
        sys.exit()

if __name__ == "__main__":
    g_ApplicationRunning = True
    EntryPoint.Main(sys.argv)
