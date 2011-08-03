#-------------------------------------------------------------------------------
# Application Name:         JefeRemoto
# Module Name:              ServerMain
# Purpose:                  This file puts it all together for double click fun
# Author:                   Guillermo Siliceo Trueba
#
# Created:                  23/04/2011
# Licence:
'''
   Copyright 2011 Guillermo Siliceo Trueba

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
#
#-------------------------------------------------------------------------------
from server import View

# hack to get a nice icon on the Windows
import ctypes
myappid = 'jefeRemoto' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
# #####################################

def main():
    app = QApplication(sys.argv)
    window=view.MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()