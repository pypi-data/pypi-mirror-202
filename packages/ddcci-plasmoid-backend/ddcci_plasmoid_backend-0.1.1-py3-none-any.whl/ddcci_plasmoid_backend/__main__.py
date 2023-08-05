import asyncio
import json
import logging
import subprocess
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path
import os
from typing import NoReturn

import fasteners

from ddcci_plasmoid_backend import arguments
from ddcci_plasmoid_backend import ddcci

logger = logging.getLogger(__name__)


def handle_error(error: str | subprocess.CalledProcessError) -> NoReturn:
    if isinstance(error, subprocess.CalledProcessError):
        error = err.stderr.decode() if err.stderr else err.stdout.decode()
    print(json.dumps({
        'command': arguments['command'],
        'error': error.replace('\n', ' ')
    }))
    sys.exit(1)


if __name__ == '__main__':
    logger.debug(f'Command: {arguments["command"]}')

    if arguments['command'] == 'version':
        print(version('ddcci-plasmoid-backend'))
        sys.exit(0)

    # include the username in the lock file. Otherwise, if user A creates a lock, user B may not have the permissions
    # to access the lock file and this program will fail until the lock file is deleted.
    with fasteners.InterProcessLock(Path(tempfile.gettempdir()) / f'ddcci_plasmoid_backend-{os.getlogin()}.lock'):
        if arguments['command'] == 'detect':
            try:
                result = asyncio.run(ddcci.detect())
            except subprocess.CalledProcessError as err:
                handle_error(err)

            # Remove objects that are errors
            filtered_results = [report for report in result if isinstance(report, dict)]

            filtered_count = len(filtered_results)
            remaining_count = len(result) - filtered_count

            logger.debug(f'Detected {filtered_count} working monitor {"bus" if filtered_count == 1 else "busses"}, '
                         f'{remaining_count} non-working {"bus" if remaining_count == 1 else "busses"}.')

            print(json.dumps({
                'command': 'detect',
                'value': filtered_results
            }))
        elif arguments['command'] == 'set-brightness':
            bus_id = arguments['bus']
            brightness = arguments['brightness']
            if brightness < 0 or brightness > 100:
                handle_error(f'Illegal value {brightness} for `brightness`, must be between 0 and 100')

            try:
                ddcci.set_brightness(bus_id, brightness)
                print(json.dumps({
                    'command': 'set-brightness',
                    'value': {
                        'bus_id': bus_id,
                        'brightness': brightness
                    }
                }))
            except subprocess.CalledProcessError as err:
                handle_error(err)

    sys.exit(0)
