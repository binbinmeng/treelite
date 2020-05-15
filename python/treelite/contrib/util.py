"""Utilities for contrib module"""
# coding: utf-8

from __future__ import absolute_import as _abs
import os
import subprocess
from sys import platform as _platform
from multiprocessing import cpu_count
from ..util import TreeliteError, lineno, log_info


def _is_windows():
    return _platform == 'win32'


def _toolchain_exist_check(toolchain):
    if toolchain != 'msvc':
        retcode = subprocess.call(f'{toolchain} --version', shell=True,
                                  stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL)
        if retcode != 0:
            raise ValueError(f'Toolchain {toolchain} not found. Ensure that it is installed and '
                             'that it is a variant of GCC or Clang.')


def _shell():
    if _is_windows():
        return 'cmd.exe'
    if 'SHELL' in os.environ:
        return os.environ['SHELL']
    return '/bin/sh'  # use POSIX-compliant shell if SHELL is not set


def _libext():
    if _platform == 'darwin':
        return '.dylib'
    if _platform in ('win32', 'cygwin'):
        return '.dll'
    return '.so'


def _create_log_cmd_unix(logfile):
    return f'true > {logfile}'


def _save_retcode_cmd_unix(logfile):
    if _shell().endswith('fish'):  # special handling for fish shell
        return f'echo $status >> {logfile}'
    return f'echo $? >> {logfile}'


def _create_log_cmd_windows(logfile):
    return f'type NUL > {logfile}'


def _save_retcode_cmd_windows(logfile):
    return f'echo %errorlevel% >> {logfile}'


def _enqueue(args):
    tid = args['tid']
    queue = args['queue']
    dirpath = args['dirpath']
    init_cmd = args['init_cmd']
    create_log_cmd = args['create_log_cmd']
    save_retcode_cmd = args['save_retcode_cmd']

    proc = subprocess.Popen(_shell(), shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    proc.stdin.write(init_cmd.encode('utf-8'))
    proc.stdin.write(f'cd {dirpath}\n'.encode('utf-8'))
    proc.stdin.write(create_log_cmd(f'retcode_cpu{tid}.txt\n').encode('utf-8'))
    for command in queue:
        proc.stdin.write((command + '\n').encode('utf-8'))
        proc.stdin.write((save_retcode_cmd(f'retcode_cpu{tid}.txt') + '\n').encode('utf-8'))
    proc.stdin.flush()

    return proc


def _wait(proc, args):
    tid = args['tid']
    dirpath = args['dirpath']
    stdout, _ = proc.communicate()
    with open(os.path.join(dirpath, f'retcode_cpu{tid}.txt'), 'r') as f:
        retcode = [int(line) for line in f]
    return {'stdout': stdout.decode('utf-8'), 'retcode': retcode}


# pylint: disable=R0914
def _create_shared_base(dirpath, recipe, nthread, verbose):
    # Fetch toolchain-specific commands
    obj_cmd = recipe['create_object_cmd']
    lib_cmd = recipe['create_library_cmd']
    create_log_cmd = _create_log_cmd_windows if _is_windows() else _create_log_cmd_unix
    save_retcode_cmd = _save_retcode_cmd_windows if _is_windows() else _save_retcode_cmd_unix

    # 1. Compile sources in parallel
    if verbose:
        log_info(__file__, lineno(),
                 f'Compiling sources files in directory {dirpath} into object files ' +
                 f'(*{recipe["object_ext"]})...')
    ncore = cpu_count()
    ncpu = min(ncore, nthread) if nthread is not None else ncore
    workqueue = [{
        'tid': tid,
        'queue': [],
        'dirpath': os.path.abspath(dirpath),
        'init_cmd': recipe['initial_cmd'],
        'create_log_cmd': create_log_cmd,
        'save_retcode_cmd': save_retcode_cmd
    } for tid in range(ncpu)]
    for i, source in enumerate(recipe['sources']):
        workqueue[i % ncpu]['queue'].append(obj_cmd(source['name']))
    proc = [_enqueue(workqueue[tid]) for tid in range(ncpu)]
    result = []
    for tid in range(ncpu):
        result.append(_wait(proc[tid], workqueue[tid]))

    for tid in range(ncpu):
        if not all(x == 0 for x in result[tid]['retcode']):
            with open(os.path.join(dirpath, f'log_cpu{tid}.txt'), 'w') as f:
                f.write(result[tid]['stdout'] + '\n')
            raise TreeliteError(f'Error occurred in worker #{tid}: ' + result[tid]['stdout'])

    # 2. Package objects into a dynamic shared library
    if verbose:
        slib = os.path.join(dirpath, recipe['target'] + recipe['library_ext'])
        log_info(__file__, lineno(), f'Generating dynamic shared library {slib}...')
    objects = ([x['name'] + recipe['object_ext'] for x in recipe['sources']] +
               recipe.get('extra', []))
    workqueue = {
        'tid': 0,
        'queue': [lib_cmd(objects, recipe['target'])],
        'dirpath': os.path.abspath(dirpath),
        'init_cmd': recipe['initial_cmd'],
        'create_log_cmd': create_log_cmd,
        'save_retcode_cmd': save_retcode_cmd
    }
    proc = _enqueue(workqueue)
    result = _wait(proc, workqueue)

    if result['retcode'][0] != 0:
        with open(os.path.join(dirpath, 'log_cpu0.txt'), 'w') as f:
            f.write(result['stdout'] + '\n')
        raise TreeliteError('Error occured while creating dynamic library: ' + result['stdout'])

    # 3. Clean up
    for tid in range(ncpu):
        os.remove(os.path.join(dirpath, f'retcode_cpu{tid}.txt'))

    # Return full path of shared library
    return os.path.join(os.path.abspath(dirpath), recipe['target'] + recipe['library_ext'])


__all__ = []
