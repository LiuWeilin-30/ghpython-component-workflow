"""Read-only catalog probe. Run INSIDE Rhino with Grasshopper loaded, not plain Python.
Prints bounded JSON. Does not create a document, add components, or change a canvas.
Run once per Rhino/component runtime, save the output in project diagnostics, and
reuse it. Entries are offered hint identities, not all Grasshopper/plugin data types.
"""
import json
import Rhino
from RhinoCodePluginGH.Parameters import ScriptVariableParam


def catalog():
    param = ScriptVariableParam('HintProbe')
    entries = []
    for hint in param.TypeHints:
        if hint is None or 'Separator' in str(hint.GetType().Name):
            continue
        entries.append({'Name': str(hint.TypeName), 'Id': str(hint.HintID),
                        'Class': str(hint.GetType().FullName)})
    return {'Rhino': str(Rhino.RhinoApp.Version),
            'ParameterAssembly': str(param.GetType().Assembly.GetName().Version),
            'Count': len(entries), 'Hints': entries}


if __name__ == '__main__':
    print(json.dumps(catalog(), ensure_ascii=False, indent=2))
