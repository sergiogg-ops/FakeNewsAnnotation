# FakeNewsAnnotation
**¿Have you ever tested your skills at distinguising Fake from Real news?** With this app you can finally find if you can detect when an article is not being honest. Using data from the [Fake News Net](https://github.com/KaiDMML/FakeNewsNet) dataset we have gathered a smaller corpus that you will annotate. For each article you will be asked to provide one label: real or fake. When all the articles have been annotated your statistics will be showed.

# Installation guide
1. Download the .zip file with the content of this git.
2. Extract the .zip file and place it in a directory that you will remember.
3. Go to the directory in which you have placed the content of the .zip file.
4. Depending on your OS download the corresponding executable file [clicking here]()

# Any trouble?
If you cannot run the corresponding executable file of the 4th step try the following:
- If the `data.json` file isn't located in the directory of the executable file, the program won't be able to find it. If this is the problem that you are experiencing, a warning window will be displayed. Please, place the `data.json` file in the directory that contains the executable file.
- The executable files were built with Windows 11 and Ubuntu 24 OS. Maybe the executable files don't match your current Windows or Linux distribution. If this is the case, you can try to run the source code. For this you will need to install python in your device if you don't have it yet. You may need to install some libraries also; for that open a terminal, go to the directori in which you extracte the .zip file and run the command `pip install -r requirements.txt`. Then, you should be able to execute the `main.py` file.