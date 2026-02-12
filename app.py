import os
import webview


class BreakScreenAPI:
    def __init__(self):
        self.window = None
        self.is_fullscreen = False

    def set_window(self, window):
        self.window = window

    def bring_to_front(self):
        if not self.window:
            return False
        self.window.restore()
        self.window.show()
        self.window.minimize()
        self.window.restore()
        self.window.on_top = True
        self.window.on_top = False
        return True

    def enter_fullscreen(self):
        if not self.window or self.is_fullscreen:
            return False
        self.window.toggle_fullscreen()
        self.is_fullscreen = True
        return True

    def exit_fullscreen(self):
        if not self.window or not self.is_fullscreen:
            return False
        self.window.toggle_fullscreen()
        self.is_fullscreen = False
        return True


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(base_dir, "index.html")

    api = BreakScreenAPI()
    window = webview.create_window(
        title="BreakScreen",
        url=index_path,
        js_api=api,
        width=800,
        height=600,
        resizable=True,
    )
    api.set_window(window)

    webview.start(debug=False)


if __name__ == "__main__":
    main()
