REM Edt Configuration here #####################################################
SET PY_VER=Python37-32
REM ############################################################################
@ECHO.
@ECHO.
@ECHO --------------------------------------------------------------------------
@ECHO Due to sometimes Windows Environment Variables are not set properly
@ECHO For Python, pip etc... this is why it is recommended to run pip:
@ECHO invoking python.exe (python -m pip install requests) for instance
@ECHO --------------------------------------------------------------------------
@ECHO Requirements before starting the process...
@ECHO Make sure to have the AWS access Key and the security key
@ECHO --------------------------------------------------------------------------
pause

SET APP_DIR=%~dp0
SET _PY_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\python.exe"
SET _PIP_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\pip.exe"
SET _ACTIVATE="%APP_DIR%\flask-prod\Scripts\activate.bat"
SET _VIRTUALENV="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\virtualenv.exe"

%_PY_EXE% -m pip install virtualenv
RMDIR /Q /S "%APP_DIR%\flask-prod"
%_PY_EXE% -m venv "%APP_DIR%\flask-prod"
cd %APP_DIR%

%_VIRTUALENV% flask-prod
@ECHO --------------------------------------------------------------------------
@ECHO Type "deploy" to deploy to AWS Elastic Beanstalk
@ECHO --------------------------------------------------------------------------
@ECHO OFF

%_ACTIVATE%
