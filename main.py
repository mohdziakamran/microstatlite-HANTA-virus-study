

import shutil
import os


if not os.path.exists('src/chromedriver.exe'):
    print('~~~~~# COPYING CHROME DRIVER IN /SRC #~~~~~')
    shutil.copyfile('chromedriver.exe','src/chromedriver.exe')

