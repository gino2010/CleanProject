import os
import shutil
import sys
import subprocess
import datetime


__author__ = 'Gino'

# setting
IGNORE_DIRECTORY = ('.idea', '.git', 'clean_deployment', '.gitignore', 'cleanServer.py')
KEEP_PYTHON_FILE = ['.py', '.pyc']
IS_COMPRESS_JS = True
IS_COMPRESS_CSS = True


# main function
def main(args):
    try:
        import yuicompressor

        jar_path = yuicompressor.get_jar_filename()
    except ImportError:
        jar_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'yuicompressor-2.4.8.jar')
        if not os.path.isfile(jar_path):
            print('You need yuicompressor jar or python lib.')
            sys.exit()
    if len(args) == 0:
        answer = raw_input('Do you want to deal with current path?(Y/N):')
        if answer.lower().startswith("y"):
            root = os.getcwd()
            clean_deployment = os.path.join(root, 'clean_deployment')
        else:
            sys.exit()
    elif len(args) == 1:
        if not os.path.isdir(args[0]):
            print('Please give a directory path.')
            sys.exit()
        else:
            root = args[0]
            clean_deployment = os.path.join(args[0], 'clean_deployment')
    else:
        print("You can't give tow or more args.")
        sys.exit()

    if os.path.isdir(clean_deployment):
        answer = raw_input('Do you want to recreate clean_deployment directory?(Y/N):')
        if answer.lower().startswith("y"):
            print('Remove old clean_deployment directory!')
            shutil.rmtree(clean_deployment)
        else:
            sys.exit()
    print('Copy project and create clean_deployment directory...')
    shutil.copytree(root, clean_deployment, ignore=shutil.ignore_patterns(*IGNORE_DIRECTORY))
    print('finished copy.')
    return clean_deployment, jar_path


# delete python file and collect js and css files
def delete_py_and_collect_jc(root):
    css_collect = []
    js_collect = []
    count = 0
    for root, subdir, files in os.walk(root):
        for f in files:
            full_path = os.path.join(root, f)
            file_name, file_ext = os.path.splitext(f)
            if file_ext == KEEP_PYTHON_FILE[0] and file_name + KEEP_PYTHON_FILE[1] in files and file_name != 'wsgi':
                try:
                    os.remove(full_path)
                    count += 1
                    print("File: %s is removed" % full_path)
                except OSError as e:
                    print("File: %s can't removed. Reason: %s" % (full_path, e.strerror))
            if IS_COMPRESS_CSS and file_ext == '.css' and 'min' not in file_name:
                css_collect.append(full_path)
            if IS_COMPRESS_JS and file_ext == '.js' and 'min' not in file_name:
                js_collect.append(full_path)
    if not count:
        print('No py file is removed.')
    return js_collect, css_collect


def readme(root):
    readme_file = os.path.join(root, 'README')
    if os.path.isfile(readme_file):
        f = open(readme_file, 'a')
    else:
        f = open(readme_file, 'w+')

    f.write('\nThis clean_deployment is created at {0:s}'.format(datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S")))
    f.close()


class Minify():
    def __init__(self, js_list, css_list, yui_path):
        self.js_list = js_list
        self.css_list = css_list
        self.yuicompressorpath = yui_path

    #compress js
    def compress_js(self):
        if len(self.js_list):
            for temp in self.js_list:
                cwd = '/'
                temp_split = temp.split(':')
                if len(temp_split) == 2:
                    cwd = temp_split[0] + ":/"
                    temp = temp_split[1][1:]

                command_args = ['java', '-jar', self.yuicompressorpath, temp,
                                '--type', 'js',
                                '-o', temp]
                try:
                    op = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
                    temp_str = op.communicate()[0]
                    if temp_str != '':
                        print(temp_str)
                    print("File: %s is compressed." % temp)
                except subprocess.CalledProcessError as e:
                    print("File: %s can't compressed. Reason: %s" % (temp, e.strerror))
        else:
            print('No JS file is compressed.')

    #compress css
    def compress_css(self):
        if len(self.css_list):
            for temp in self.css_list:
                cwd = '/'
                temp_split = temp.split(':')
                if len(temp_split) == 2:
                    cwd = temp_split[0] + ":/"
                    temp = temp_split[1][1:]

                command_args = ['java', '-jar', self.yuicompressorpath, temp,
                                '--type', 'css',
                                '-o', temp]
                try:
                    op = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)
                    temp_str = op.communicate()[0]
                    if temp_str != '':
                        print(temp_str)
                    print("File: %s is compressed." % temp)
                except subprocess.CalledProcessError as e:
                    print("File: %s can't compressed. Reason: %s" % (temp, e.message))
        else:
            print('No CSS file is compressed.')

# main
if __name__ == "__main__":
    pwd, path = main(sys.argv[1:])

    # directory handle and collect files
    print('Start to remove %s files ...' % KEEP_PYTHON_FILE[0])
    js, css = delete_py_and_collect_jc(pwd)

    #compress files
    minify = Minify(js, css, path)
    print('Start to compress js files ...')
    minify.compress_js()
    print('Start to compress css files ...')
    minify.compress_css()

    #create log write into README
    readme(pwd)
    print('finished all')
    sys.exit()