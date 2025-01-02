# Enhanced Interactive mode

This supports Windows only.

```bat
@goto BAT

import enhanced_interactive_mode

enhanced_interactive_mode.init(completion_highlight_color="cyan")

"""
:BAT
@echo off
cd /d "%~dp0"
python -x -i "%~f0"
exit /b %ERRORLEVEL%
"""
```
