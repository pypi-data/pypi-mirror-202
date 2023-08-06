import PyInstaller.__main__



def flixy2app_convert (script_file, output_dir):

    # Specify the Python script you want to convert to .exe
    script_file = script_file

    # Specify the output directory where the .exe file will be generated
    output_dir = output_dir

    # Specify additional packages to be included
    hidden_imports = ['flixy', 'PyInstaller', "flet"]

    # Use PyInstaller to convert the script to .exe, including additional packages
    PyInstaller.__main__.run([
        script_file,
        '--onefile',  # Specify to generate a single .exe file
        '--noconsole',  # Specify to create a GUI application without a console window
        f'--distpath={output_dir}',  # Specify the output directory for the .exe file
        *[f'--hidden-import={pkg}' for pkg in hidden_imports]  # Specify additional packages to be included
    ])

    return True