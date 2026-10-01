# Replace the placeholder before pasting into a Rhino 8 Python 3 Script component.
SOURCE_PATH = r"<absolute workspace path to the component .py>"
with open(SOURCE_PATH, "r", encoding="utf-8") as source_file:
    source = source_file.read()
exec(compile(source, SOURCE_PATH, "exec"), globals(), globals())
