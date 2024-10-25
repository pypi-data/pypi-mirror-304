import os
import subprocess
import typing as t

import lk_logger
from argsense import args_2_cargs
from lk_utils import fs
from lk_utils import run_cmd_args

from ... import paths
from ...manifest import get_last_installed_version
from ...manifest import load_manifest
from ...manifest import parse_script_info
from ...platform import sysinfo


def run_app(
    appid: str = None,
    *args,
    _caller_location: str = None,
    _version: str = None,
    _blocking: bool = True,
    **kwargs
) -> t.Optional[subprocess.Popen]:
    """
    a general launcher to start an installed app.
    """
    if appid is None:
        assert (
            _caller_location and _caller_location.endswith(('.exe', '.bat'))
        ), _caller_location
        # related:
        #   depsland.api.user_api.install._create_launchers
        #   build/exe/depsland-runapp.bat
        #   build/exe/depsland-runapp-debug.bat
        #   build/build.py : [code] if __name__ == '__main__' : [comment]
        caller_dir = fs.parent(_caller_location)
        _, appid, _version = caller_dir.rsplit('/', 2)
        print(_caller_location, appid, _version)
    
    version = _version or get_last_installed_version(appid)
    if not version:
        print(':v4', f'cannot find installed version of {appid}')
        return
    else:
        print(
            ':r', '[magenta dim]launching [cyan]{}[/] [green]v{}[/][/]'
            .format(appid, version)
        )
    
    manifest = load_manifest('{}/{}/{}/manifest.pkl'.format(
        paths.project.apps, appid, version
    ))
    assert manifest['version'] == version
    command, args0, kwargs0 = parse_script_info(manifest)
    # print(command, args0, kwargs0, ':l')
    os.environ['DEPSLAND'] = paths.project.root
    sep = ';' if sysinfo.IS_WINDOWS else ':'
    os.environ['PYTHONPATH'] = sep.join((
        '.',  # "current" dir
        'lib',  # frequently used dir
        'src',  # frequently used dir
        manifest['start_directory'],  # app_dir
        paths.apps.get_packages(appid, version),  # pkg_dir
    ))
    # print(
    #     os.environ['PYTHONPATH'].split(sep),
    #     os.environ['PATH'].split(sep), ':lv'
    # )
    
    if not manifest['launcher']['show_console']:
        if sysinfo.IS_WINDOWS:
            _toast_notification(
                'Depsland is launching "{} (v{})"'.format(appid, version)
            )
    
    print(':vs', ' '.join(
        (*command, *args_2_cargs(*args, *args0, **kwargs, **kwargs0))
    ))
    # lk_logger.unload()
    try:
        # TODO: use '--' to separate different args/kwargs groups.
        return run_cmd_args(
            command, args_2_cargs(*args, *args0, **kwargs, **kwargs0),
            cwd=manifest['start_directory'],
            blocking=_blocking,
            shell=True,
            verbose=True,
            # verbose=False,
        )
        # subprocess.run(
        #     (*command, *args_2_cargs(*args, *args0, **kwargs, **kwargs0)),
        #     check=True,
        #     cwd=manifest['start_directory'],
        #     stderr=subprocess.PIPE,
        #     text=True,
        # )
    except subprocess.CalledProcessError as e:
        lk_logger.enable()
        print(':v4f', '\n' + (e.stderr or '').replace('\r', ''))
        if manifest['launcher']['show_console']:
            # raise e
            input('press ENTER to exit... ')
        else:
            _popup_error(
                'Exception occurred at "{}"!'.format(manifest['name'])
            )


def _popup_error(msg: str) -> None:
    """ use tkinter popup to show error message. """
    import tkinter
    from tkinter import messagebox
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showerror('Error', msg)
    root.destroy()


# windows only  # DELETE: the toast sound is annoying for user.
def _toast_notification(text: str) -> None:
    try:
        from windows_toasts import Toast
        from windows_toasts import WindowsToaster
    except ImportError:
        # raise ImportError('pip install windows-toasts')
        print('module not found: windows-toasts', ':v3p')
        return
    toaster = WindowsToaster('Depsland Launcher')
    toast = Toast()
    toast.text_fields = [text]
    toaster.show_toast(toast)
