import os
import shutil

__author__ = 'Gino'

# setting
REMOVE_DIRECTORY = ['.test1', '.test2']
KEEP_PYTHON_FILE = ['.tx', '.txt']
IS_COMPRESS_JS = True
IS_COMPRESS_CSS = True


# delete directory
def delete_directory(root):
    for d in REMOVE_DIRECTORY:
        try:
            full_path = os.path.join(root, d)
            shutil.rmtree(full_path)
            print("Directory: %s is removed" % full_path)
        except WindowsError as e:
            print("Directory: %s can't removed. Reason: %s" % (full_path, e.strerror))


# delete python file and collect js and css files
def delete_py_and_collect_jc(root):
    css_collect = []
    js_collect = []
    count = 0
    for root, subdir, files in os.walk(root):
        for f in files:
            full_path = os.path.join(root, f)
            file_name, file_ext = os.path.splitext(f)
            if file_ext == KEEP_PYTHON_FILE[0] and file_name + KEEP_PYTHON_FILE[1] in files:
                try:
                    os.remove(full_path)
                    count += 1
                    print("File: %s is removed" % full_path)
                except WindowsError as e:
                    print("File: %s can't removed. Reason: %s" % (full_path, e.strerror))
            if IS_COMPRESS_CSS and file_ext == '.css' and min not in file_name:
                css_collect.append(full_path)
            if IS_COMPRESS_JS and file_ext == '.js' and min not in file_name:
                js_collect.append(full_path)
    if not count:
        print('No py file is removed.')
    return js_collect, css_collect


#compress js
def compress_js(js_list):
    if len(js_list):
        print('')
    else:
        print('No JS file is compressed.')


#compress css
def compress_css(css_list):
    if len(css_list):
        print('')
    else:
        print('No CSS file is compressed.')

# main
if __name__ == "__main__":
    pwd = os.path.dirname(os.path.realpath(__file__))
    # delete_directory(pwd)
    js, css = delete_py_and_collect_jc(pwd)
    compress_js(js)
    compress_css(css)