"""
Definitions of the Invoke tasks for the project
"""

import os
from invoke import task


@task
def run_app(contex):
    """
    Execute the application
    """
    contex.run("python app/main.py")


@task
def generate_ui(context):
    """
    Generate python files based on the UI templates
    """
    os.chdir(os.getcwd())
    for ui_file in os.listdir('./app/ui/forms'):
        if not ui_file.endswith('.ui'):
            continue
        py_file = ui_file.replace('.ui', '.py')
        print("convert {} to {}".format(ui_file, py_file))
        context.run("pipenv run pyside2-uic --from-imports app/ui/forms/{} -o app/ui/forms/{}".format(ui_file, py_file))

    for ui_file in os.listdir('./app/ui/forms'):
        if not ui_file.endswith('.qrc'):
            continue
        py_file = ui_file.replace('.qrc', '_rc.py')
        print("convert {} to {}".format(ui_file, py_file))
        context.run("pipenv run pyside2-rcc app/ui/forms/{} -o  app/ui/forms/{}".format(ui_file, py_file))

@task
def generate_exe(context):
    """
    Generate exe file based on the app/main.py
    """
    os.chdir(os.getcwd())
    context.run("pipenv run pyinstaller --onefile -w app/main.py --name {}".format("ShutdownPC"))
