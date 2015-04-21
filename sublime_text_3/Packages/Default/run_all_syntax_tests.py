import sublime
import sublime_plugin
import sublime_api
import os

class RunAllSyntaxTestsCommand(sublime_plugin.WindowCommand):
    def run(self,
        file_regex = "",
        line_regex = "",
        working_dir = "",
        quiet = False,
        word_wrap = True,
        syntax = "Packages/Text/Plain text.tmLanguage",
        **kwargs):

        if not hasattr(self, 'output_view'):
            # Try not to call get_output_panel until the regexes are assigned
            self.output_view = self.window.create_output_panel("exec")

        # Default the to the current files directory if no working directory was given
        if (working_dir == "" and self.window.active_view()
                        and self.window.active_view().file_name()):
            working_dir = os.path.dirname(self.window.active_view().file_name())

        self.output_view.settings().set("result_file_regex", file_regex)
        self.output_view.settings().set("result_line_regex", line_regex)
        self.output_view.settings().set("result_base_dir", working_dir)
        self.output_view.settings().set("word_wrap", word_wrap)
        self.output_view.settings().set("line_numbers", False)
        self.output_view.settings().set("gutter", False)
        self.output_view.settings().set("scroll_past_end", False)
        self.output_view.assign_syntax(syntax)

        # Call create_output_panel a second time after assigning the above
        # settings, so that it'll be picked up as a result buffer
        self.window.create_output_panel("exec")

        show_panel_on_build = sublime.load_settings("Preferences.sublime-settings").get("show_panel_on_build", True)
        if show_panel_on_build:
            self.window.run_command("show_panel", {"panel": "output.exec"})

        # Change to the working dir, rather than spawning the process with it,
        # so that emitted working dir relative path names make sense
        if working_dir != "":
            os.chdir(working_dir)

        output = ""
        tests = sublime.find_resources("syntax_test*")
        num_failed = 0
        for t in tests:
            test_output = sublime_api.run_syntax_test(t)
            if len(test_output) > 0:
                num_failed += 1
                output += test_output + "\n"

        self.append_string(output)

        if num_failed > 0:
            self.append_string("FAILED: %d of %d tests failed\n" % (num_failed, len(tests)))
        else:
            self.append_string("Success: %d tests passed\n" % len(tests))

        self.append_string("[Finished]")

    def append_string(self, str):
        self.output_view.run_command('append', {'characters': str, 'force': True, 'scroll_to_end': True})
