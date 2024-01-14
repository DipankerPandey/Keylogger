import os
import stat
import ctypes

def hide_file_windows(file_path):
    try:
        # Set the hidden attribute
        attributes = os.stat(file_path).st_file_attributes | stat.FILE_ATTRIBUTE_HIDDEN
        os.chmod(file_path, attributes)
    except:
        pass



