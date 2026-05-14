from pathlib import Path

path = Path("src/spektrafilm_gui/controller_layers.py")
content = path.read_text()

search = """def virtual_photo_paper_back(*args, **kwargs):
    return import_module('spektrafilm_gui.virtual_photo_paper_back').virtual_photo_paper_back(*args, **kwargs)"""

replace = """def virtual_photo_paper_back(*args, **kwargs):
    # Pass everything as kwargs to support the new Config-based signature while maintaining backward compatibility.
    # Note: args are deliberately ignored since the new signature doesn't use positional arguments.
    return import_module('spektrafilm_gui.virtual_photo_paper_back').virtual_photo_paper_back(**kwargs)"""

content = content.replace(search, replace, 1)

path.write_text(content)
