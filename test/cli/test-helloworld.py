
# python -m pytest test-helloworld.py

import os
import re
from testutils import create_gui_project_file, cppcheck

# Run Cppcheck from project path
def cppcheck_local(args):
    cwd = os.getcwd()
    os.chdir('1-helloworld')
    ret, stdout, stderr = cppcheck(args)
    os.chdir(cwd)
    return (ret, stdout, stderr)

def getRelativeProjectPath():
    return '1-helloworld'

def getAbsoluteProjectPath():
    return os.path.join(os.getcwd(), '1-helloworld')

# Get Visual Studio configurations checking a file
# Checking {file} {config}...
def getVsConfigs(stdout, filename):
    ret = []
    for line in stdout.split('\n'):
        if not line.startswith('Checking %s ' % (filename)):
            continue
        if not line.endswith('...'):
            continue
        res = re.match(r'.* ([A-Za-z0-9|]+)...', line)
        if res:
            ret.append(res.group(1))
    ret.sort()
    return ' '.join(ret)

def test_relative_path():
    ret, stdout, stderr = cppcheck('1-helloworld')
    filename = os.path.join('1-helloworld', 'main.c')
    assert ret == 0
    assert stdout == 'Checking %s ...\n' % (filename)
    assert stderr == '[%s:5]: (error) Division by zero.\n' % (filename)


def test_local_path():
    ret, stdout, stderr = cppcheck_local('.')
    assert ret == 0
    assert stdout == 'Checking main.c ...\n'
    assert stderr == '[main.c:5]: (error) Division by zero.\n'

def test_absolute_path():
    prjpath = getAbsoluteProjectPath()
    ret, stdout, stderr = cppcheck(prjpath)
    filename = os.path.join(prjpath, 'main.c')
    assert ret == 0
    assert stdout == 'Checking %s ...\n' % (filename)
    assert stderr == '[%s:5]: (error) Division by zero.\n' % (filename)

def test_addon_local_path():
    ret, stdout, stderr = cppcheck_local('--addon=misra .')
    assert ret == 0
    assert stdout == 'Checking main.c ...\n'
    assert stderr == ('[main.c:5]: (error) Division by zero.\n'
                      '[main.c:1]: (style) misra violation (use --rule-texts=<file> to get proper output)\n')

def test_addon_absolute_path():
    prjpath = getAbsoluteProjectPath()
    ret, stdout, stderr = cppcheck('--addon=misra %s' % (prjpath))
    filename = os.path.join(prjpath, 'main.c')
    assert ret == 0
    assert stdout == 'Checking %s ...\n' % (filename)
    assert stderr == ('[%s:5]: (error) Division by zero.\n'
                      '[%s:1]: (style) misra violation (use --rule-texts=<file> to get proper output)\n' % (filename, filename))

def test_addon_relative_path():
    prjpath = getRelativeProjectPath()
    ret, stdout, stderr = cppcheck('--addon=misra %s' % (prjpath))
    filename = os.path.join(prjpath, 'main.c')
    assert ret == 0
    assert stdout == 'Checking %s ...\n' % (filename)
    assert stderr == ('[%s:5]: (error) Division by zero.\n'
                      '[%s:1]: (style) misra violation (use --rule-texts=<file> to get proper output)\n' % (filename, filename))

def test_addon_relative_path():
    project_file = '1-helloworld/test.cppcheck'
    create_gui_project_file(project_file, paths=['.'], addon='misra')
    ret, stdout, stderr = cppcheck('--project=%s' % (project_file))
    filename = os.path.join('1-helloworld', 'main.c')
    assert ret == 0
    assert stdout == 'Checking %s ...\n' % (filename)
    assert stderr == ('[%s:5]: (error) Division by zero.\n'
                      '[%s:1]: (style) misra violation (use --rule-texts=<file> to get proper output)\n' % (filename, filename))

def test_basepath_relative_path():
    prjpath = getRelativeProjectPath()
    ret, stdout, stderr = cppcheck('%s -rp=%s' % (prjpath, prjpath))
    filename = os.path.join(prjpath, 'main.c')
    assert ret == 0
    assert stdout == 'Checking %s ...\n' % (filename)
    assert stderr == '[main.c:5]: (error) Division by zero.\n'

def test_basepath_absolute_path():
    prjpath = getAbsoluteProjectPath()
    ret, stdout, stderr = cppcheck('%s -rp=%s' % (prjpath, prjpath))
    filename = os.path.join(prjpath, 'main.c')
    assert ret == 0
    assert stdout == 'Checking %s ...\n' % (filename)
    assert stderr == '[main.c:5]: (error) Division by zero.\n'

def test_vs_project_local_path():
    ret, stdout, stderr = cppcheck_local('--project=helloworld.vcxproj')
    assert ret == 0
    assert getVsConfigs(stdout, 'main.c') == 'Debug|Win32 Debug|x64 Release|Win32 Release|x64'
    assert stderr == '[main.c:5]: (error) Division by zero.\n'

def test_vs_project_relative_path():
    prjpath = getRelativeProjectPath()
    ret, stdout, stderr = cppcheck('--project=%s' % (os.path.join(prjpath, 'helloworld.vcxproj')))
    filename = os.path.join(prjpath, 'main.c')
    assert ret == 0
    assert getVsConfigs(stdout, filename) == 'Debug|Win32 Debug|x64 Release|Win32 Release|x64'
    assert stderr == '[%s:5]: (error) Division by zero.\n' % (filename)

def test_vs_project_absolute_path():
    prjpath = getAbsoluteProjectPath()
    ret, stdout, stderr = cppcheck('--project=%s' % (os.path.join(prjpath, 'helloworld.vcxproj')))
    filename = os.path.join(prjpath, 'main.c')
    assert ret == 0
    assert getVsConfigs(stdout, filename) == 'Debug|Win32 Debug|x64 Release|Win32 Release|x64'
    assert stderr == '[%s:5]: (error) Division by zero.\n' % (filename)

def test_cppcheck_project_local_path():
    ret, stdout, stderr = cppcheck_local('--platform=win64 --project=helloworld.cppcheck')
    assert ret == 0
    assert getVsConfigs(stdout, 'main.c') == 'Debug|x64'
    assert stderr == '[main.c:5]: (error) Division by zero.\n'

def test_cppcheck_project_relative_path():
    prjpath = getRelativeProjectPath()
    ret, stdout, stderr = cppcheck('--platform=win64 --project=%s' % (os.path.join(prjpath, 'helloworld.cppcheck')))
    filename = os.path.join(prjpath, 'main.c')
    assert ret == 0
    assert getVsConfigs(stdout, filename) == 'Debug|x64'
    assert stderr == '[%s:5]: (error) Division by zero.\n' % (filename)

def test_cppcheck_project_absolute_path():
    prjpath = getAbsoluteProjectPath()
    ret, stdout, stderr = cppcheck('--platform=win64 --project=%s' % (os.path.join(prjpath, 'helloworld.cppcheck')))
    filename = os.path.join(prjpath, 'main.c')
    assert ret == 0
    assert getVsConfigs(stdout, filename) == 'Debug|x64'
    assert stderr == '[%s:5]: (error) Division by zero.\n' % (filename)

def test_suppress_command_line():
    prjpath = getRelativeProjectPath()
    ret, stdout, stderr = cppcheck('--suppress=zerodiv:%s %s' % (os.path.join(prjpath, 'main.c'), prjpath))
    assert ret == 0
    assert stderr == ''

    prjpath = getAbsoluteProjectPath()
    ret, stdout, stderr = cppcheck('--suppress=zerodiv:%s %s' % (os.path.join(prjpath, 'main.c'), prjpath))
    assert ret == 0
    assert stderr == ''

def test_suppress_project():
    project_file = os.path.join('1-helloworld', 'test.cppcheck')
    create_gui_project_file(project_file,
                            paths=['.'],
                            suppressions=[{'fileName':'main.c', 'id':'zerodiv'}])

    # Relative path
    ret, stdout, stderr = cppcheck('--project=%s' % (project_file))
    assert ret == 0
    assert stderr == ''

    # Absolute path
    ret, stdout, stderr = cppcheck('--project=%s' % (os.path.join(os.getcwd(), '1-helloworld', 'test.cppcheck')))
    assert ret == 0
    assert stderr == ''

