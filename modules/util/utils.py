from dragonfly import AppContext, Mouse, Clipboard, Dictation
import types

shell_context = AppContext(executable="cmd") | AppContext(executable="powershell")
normal_context = ~shell_context


def write_to_shell(text):
    clipboard = Clipboard()
    clipboard.set_text(text)
    clipboard.copy_to_system()
    Mouse("right").execute()


