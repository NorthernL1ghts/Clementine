import dearpygui.dearpygui as dpg

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
