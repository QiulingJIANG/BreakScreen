import os
import webview


class BreakScreenAPI:
    def __init__(self):
        self.window = None
        self.is_fullscreen = False
        self.prev_size = None
        self.prev_pos = None

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
        # Save current geometry first so we can restore it on exit.
        try:
            self.prev_size = self.window.width, self.window.height
            self.prev_pos = self.window.x, self.window.y
        except Exception:
            self.prev_size = None
            self.prev_pos = None

        # Strategy 1: native fullscreen API (best UX if backend supports it).
        try:
            self.window.toggle_fullscreen()
            self.is_fullscreen = True
            return True
        except Exception:
            pass

        # Strategy 2: fallback to maximize + resize to primary screen.
        try:
            screens = webview.screens
            if screens:
                screen = screens[0]
                self.window.move(screen.x, screen.y)
                self.window.resize(screen.width, screen.height)
            self.window.maximize()
            self.is_fullscreen = True
            return True
        except Exception:
            return False

    def exit_fullscreen(self):
        if not self.window or not self.is_fullscreen:
            return False
        # Strategy 1: native fullscreen toggle out.
        try:
            self.window.toggle_fullscreen()
            self.is_fullscreen = False
            return True
        except Exception:
            return False    

        # Strategy 2: restore previous geometry from fallback mode.
        try:
            if self.prev_size:
                width, height = self.prev_size
                self.window.resize(width, height)
            if self.prev_pos:
                x, y = self.prev_pos
                self.window.move(x, y)
            self.window.restore()
            self.is_fullscreen = False
            return True
        except Exception:
            return False


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
