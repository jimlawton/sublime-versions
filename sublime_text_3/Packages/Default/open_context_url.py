import sublime, sublime_plugin
import webbrowser
import re

class OpenContextUrlCommand(sublime_plugin.TextCommand):
    def run(self, edit, event):
        url = self.find_url(event)
        webbrowser.open_new_tab(url)

    def is_visible(self, event):
        return self.find_url(event) != None

    def find_url(self, event):
        pt = self.view.window_to_text((event["x"], event["y"]))
        line = self.view.line(pt)

        line.a = max(line.a, pt - 1024)
        line.b = min(line.b, pt + 1024)

        text = self.view.substr(line)

        it = re.finditer(r"\bhttp(s)?://[^ \t]+", text)

        for match in it:
            if match.start() <= (pt - line.a) and match.end() >= (pt - line.a):
                return text[match.start():match.end()]

        return None

    def description(self, event):
        url = self.find_url(event)
        if len(url) > 64:
            url = url[0:64] + "..."
        return "Open " + url

    def want_event(self):
        return True
