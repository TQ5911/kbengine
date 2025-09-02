@echo off
cd /d "%~dp0"
@rem echo curdir:%CD%
@rem python --version
copy "hotReloadTemp.py" "..\scripts\server_common\hotReload.py"
python genhotfix.py %*
python genRunScript.py
@rem for /f "delims=" %%i in ('python -c "import sys; print(sys.executable)"') do set PYTHON_EXE=%%i
@rem echo %PYTHON_EXE%
@rem echo time1: %time%
.\runScripts.exe --config=config.yaml
@rem echo time2: %time%