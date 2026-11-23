import sys,platform,json,hashlib,tkinter as tk,_tkinter
import numpy,matplotlib,scipy,pytest
r=tk.Tk();r.withdraw();out={'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'Tcl':r.tk.call('info','patchlevel'),'Tk':r.tk.call('package','provide','Tk'),'tkinter_extension':_tkinter.__file__,'tkinter_sha256':hashlib.sha256(open(_tkinter.__file__,'rb').read()).hexdigest(),'NumPy':numpy.__version__,'Matplotlib':matplotlib.__version__,'SciPy':scipy.__version__,'pytest':pytest.__version__};r.destroy();print(json.dumps(out,indent=2))
