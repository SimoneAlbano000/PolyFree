# PolyFree
 Tool for checking available classrooms in Politecnico di Torino
 
 The App is written in Python3 and compiled into an .apk using a tool called BeeWare: https://beeware.org/  
 (Only the Windows platform will be discussed here!)
 
# Compile the source code:  
 ## Dependencies:
   Required programs and packages:
   - Git
   - Python 3.8/3.>
   - pip  
   Some packages from pip:
     - briefcase
     - requests
     - bs4

 ## Activate the Python virtual enviroment:
   ```bash
    C:\...> cd Scripts
    C:\...\Scripts> activate.bat
   ```

   ## Install Briefcase (and other core packages) if not altready installed:
   ```bash
    (polyfree-venv) C:\...\Scripts> cd polyfree
    (polyfree-venv) C:\...\Scripts\polyfree> python -m pip install briefcase requests bs4
   ```

   ## Now it's time to compile the app into an apk package:
   If you have modified the configuration file (pyproject.toml), you will also need to update the project
   ```bash
    (polyfree-venv) C:\...\Scripts\polyfree> briefcase create android
    (polyfree-venv) C:\...\Scripts\polyfree> briefcase update android
    (polyfree-venv) C:\...\Scripts\polyfree> briefcase build android
   ```
   The first build will take a while to compile the application.  
   After the process is completed the build apk will be located at:
   ```bash
    ~\Scripts\polyfree\build\polyfree\android\gradle\app\build\outputs\apk\debug\app-debug.apk
   ```
   If you want to update/build/run the application at the same time:
   ```bash
    (polyfree-venv) C:\...\Scripts\polyfree> briefcase run android -u -r
   ```

   ## Run the newly compiled apk:
   You can choose to run the application in an Android emulator or executing it directly on your device:
   remember to activate the Debug USB in the Developer Options tab on your Android device, otherwise adb
   will not be able to install the application and the device id will not show up as an option.
   ```bash
    (polyfree-venv) C:\...\Scripts\polyfree> briefcase run android
   ```

   ## Modify the python code:
   The main Python code is located at:
   ```bash
    ~\Scripts\polyfree\src\polyfree\app.py
   ```
   The resources for all the splash images, Android app icons are located at:
   ```bash
    ~\Scripts\polyfree\src\polyfree\resources\
    ~\Scripts\polyfree\build\polyfree\android\gradle\app\src\main\res\
   ```
