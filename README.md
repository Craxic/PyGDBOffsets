To use (run this in your GDB prompt or add to `.gdbinit`):
```
python import sys
python sys.path.append('/path/to/offsets.py')
python import offsets
offsets-of Whatever
```

If you're making changes to it, the following might be more useful:
```
python import sys
python sys.path.append('/path/to/offsets.py')
python import offsets
python import imp
```
Then every time you make a change:
```
python imp.reload(offsets)
offsets-of Whatever
```
