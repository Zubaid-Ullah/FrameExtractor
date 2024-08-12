Application interface pics:
1.png 2.png 3.png 4.png 

Files intro:
*  Run.py is first file to be loaded when app starts, and it asks for password "Pass".
*  when you click enter, it loads another windows which is mainwindow and there user can select video,
   output directory to store/save extracted frames in png form, and how many frames to be skipped.
*   there are two other ui files which are used for interface: Password.ui & PicExtractor.ui

Buidlding App:
*   git clone https://github.com/Zubaid-Ullah/FrameExtractor.git
*   go to Directory where you downloaded my code.
*   setup.py is the impoartant file while building macOS App
*   just go to terminal where virtual environment is activated and run python3 setup.py py2app

Happy Coding...

Note:
    py2app is only used for MacOS
