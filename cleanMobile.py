import os
import shutil
import subprocess
import sys
import datetime

__author__ = 'gino'

IGNORE_DIRECTORY = ('.idea', '.git', 'clean_mobile', '.gitignore', 'cleanMobile.py',
                    '.iml', '.class', 'gen', 'out', '.apk')

WWW = 'assets/www/'
NGMIN = 'assets/www/js/'

IS_COMPRESS_JS = True
IS_COMPRESS_CSS = True


# main function
def main(args):
    # check ngmin
    try:
        command_args = ['ngmin', '--version']
        op = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='/')
        output = op.communicate()[0]
        if command_args[0] in output:
            print("You need install ngmin before using.")
            sys.exit()
        else:
            print("ngmin version: %s." % output)
    except subprocess.CalledProcessError as e:
        print("Call Error: %s" % e.message)
        sys.exit()
    #check yuicompressor
    try:
        import yuicompressor

        jar_path = yuicompressor.get_jar_filename()
    except ImportError:
        jar_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'yuicompressor-2.4.8.jar')
        if not os.path.isfile(jar_path):
            print('You need yuicompressor jar or python lib.')
            sys.exit()
    print('System check over, start to deal with proejct......')
    if len(args) == 0:
        answer = raw_input('Do you want to deal with current path?(Y/N):')
        if answer.lower().startswith("y"):
            root = os.getcwd()
            clean_mobile = os.path.join(root, 'clean_mobile')
        else:
            sys.exit()
    elif len(args) == 1:
        if not os.path.isdir(args[0]):
            print('Please give a directory path.')
            sys.exit()
        else:
            root = args[0]
            clean_mobile = os.path.join(args[0], 'clean_mobile')
    else:
        print("You can't give tow or more args.")
        sys.exit()

    if os.path.isdir(clean_mobile):
        answer = raw_input('Do you want to recreate clean_mobile directory?(Y/N):')
        if answer.lower().startswith("y"):
            print('Remove old clean_mobile directory!')
            shutil.rmtree(clean_mobile)
        else:
            sys.exit()
    print('Copy project and create clean_mobile directory...')
    shutil.copytree(root, clean_mobile, ignore=shutil.ignore_patterns(*IGNORE_DIRECTORY))
    print('finished copy.')
    return clean_mobile, jar_path


def ngmin_compress_js(root):
    for root, subdir, files in os.walk(root):
        for f in files:
            full_path = os.path.join(root, f)
            # ngmin file
            command_min = ['ngmin', full_path, full_path]
            try:
                op = subprocess.Popen(command_min, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='/')
                temp_str = op.communicate()[0]
                if temp_str != '':
                    print(temp_str)
                print("File: %s is ngmined." % full_path)
            except subprocess.CalledProcessError as e:
                print("File: %s can't be ngmined. Reason: %s" % (full_path, e.message))

            command_min = ['java', '-jar', path, full_path,
                           '--type', 'js',
                           '-o', full_path]
            try:
                op = subprocess.Popen(command_min, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='/')
                temp_str = op.communicate()[0]
                if temp_str != '':
                    print(temp_str)
                print("File: %s is compressed." % full_path)
            except subprocess.CalledProcessError as e:
                print("File: %s can't compressed. Reason: %s" % (full_path, e.message))


# delete python file and collect js and css files
def collect_js_css(root):
    css_collect = []
    js_collect = []
    for root, subdir, files in os.walk(root):
        for f in files:
            full_path = os.path.join(root, f)
            file_name, file_ext = os.path.splitext(f)
            if IS_COMPRESS_CSS and file_ext == '.css' and 'min' not in file_name:
                css_collect.append(full_path)
            if IS_COMPRESS_JS and file_ext == '.js' and 'min' not in file_name:
                js_collect.append(full_path)
    return js_collect, css_collect


def readme(root):
    readme_file = os.path.join(root, 'README')
    if os.path.isfile(readme_file):
        f = open(readme_file, 'a')
    else:
        f = open(readme_file, 'w+')

    f.write('This clean_Mobile is created at {0:s}'.format(datetime.datetime.now().strftime("%Y.%m.%d.%H.%M.%S")))
    f.close()


# main
if __name__ == "__main__":
    pwd, path = main(sys.argv[1:])

    print('Start to deal with js files ...')
    # ngmin js
    ngmin_compress_js(os.path.join(pwd, NGMIN))

    #create log write into README
    readme(pwd)
    print('finished all')
    sys.exit()