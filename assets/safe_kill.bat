set uid=xxx
if defined KBE_ROOT (python %KBE_ROOT%/kbe\tools\server\pycluster\cluster_controller.py stop %uid%) else (python ..\kbe\tools\server\pycluster\cluster_controller.py stop %uid%)
