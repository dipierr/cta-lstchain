#!/usr/bin/env python3

"""
Pipeline to calibrate and compute image parameters at single telescope 
level for real data.
- Inputs are a protozfits input file and a drs4 pedestal/calibration/time
calibration files
- Output is a dataframe with dl1 data

Usage: 

$> python lstchain_data_r0_to_dl1.py arg1 arg2 ...

"""

import argparse
from lstchain.reco import r0_to_dl1
from lstchain.io.config import read_configuration_file
import sys
import logging
import os

log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="R0 to DL1")

# Required arguments
parser.add_argument('--input_file', '-f', type=str,
                    dest='input_file',
                    help='Path to the .fits.fz file with the raw events',
                    default=None, required=True)

parser.add_argument('--output_dir', '-o', action='store', type=str,
                    dest='output_dir',
                    help='Path where to store the reco dl1 events',
                    default='./dl1_data/')

parser.add_argument('--pedestal_file', '-pedestal', action='store', type=str,
                    dest='pedestal_file',
                    help='Path to a pedestal file',
                    default=None, required=True
                    )

parser.add_argument('--calibration_file', '-calib', action='store', type=str,
                    dest='calibration_file',
                    help='Path to a calibration file',
                    default=None, required=True
                    )

parser.add_argument('--time_calibration_file', '-time_calib', action='store', type=str,
                    dest='time_calibration_file',
                    help='Path to a calibration file for pulse time correction',
                    default=None, required=True
                    )

# Optional arguments
parser.add_argument('--config_file', '-conf', action='store', type=str,
                    dest='config_file',
                    help='Path to a configuration file. If none is given, a standard configuration is applied',
                    default=None
                    )

parser.add_argument('--pointing_file_file', '-pointing', action='store', type=str,
                    dest='pointing_file_file',
                    help='Path to the Drive log file with the pointing information.',
                    default=None
                    )

parser.add_argument('--ucts_t0_dragon', action='store', type=float,
                    dest='ucts_t0_dragon',
                    help='UCTS timestamp in nsecs, unix format and TAI scale of the \
                          first event of the run with valid timestamp. If none is \
                          passed, the start-of-the-run timestamp is provided, hence \
                          Dragon timestmap is not reliable.',
                    default="NaN"
                    )

parser.add_argument('--dragon_counter0', action='store', type=float,
                    dest='dragon_counter0',
                    help='Dragon counter (pps + 10MHz) in nsecs corresponding \
                          to the first reliable UCTS of the run. To be provided \
                          along with ucts_t0_dragon.',
                    default="NaN"
                    )

parser.add_argument('--ucts_t0_tib', action='store', type=float,
                    dest='ucts_t0_tib',
                    help='UCTS timestamp in nsecs, unix format and TAI scale of the \
                          first event of the run with valid timestamp. If none is \
                          passed, the start-of-the-run timestamp is provided, hence \
                          TIB timestmap is not reliable.',
                    default="NaN"
                    )

parser.add_argument('--tib_counter0', action='store', type=float,
                    dest='tib_counter0',
                    help='First valid TIB counter (pps + 10MHz) in nsecs corresponding \
                          to the first reliable UCTS of the run when TIB is available. \
                          To be provided along with ucts_t0_tib.',
                    default="NaN"
                    )

parser.add_argument('--max_events', '-maxevts', action='store', type=int,
                    dest='max_events',
                    help='Maximum number of events to be processed.',
                    default=int(1e15)
                    )

args = parser.parse_args()


def main():
    os.makedirs(args.output_dir, exist_ok=True)

    r0_to_dl1.allowed_tels = {1, 2, 3, 4}
    output_filename = os.path.join(
        args.output_dir,
        'dl1_' + os.path.basename(args.input_file).rsplit('.', 1)[0] + '.h5'
    )

    config = {}
    if args.config_file is not None:
        try:
            config = read_configuration_file(args.config_file)
        except Exception as e:
            log.error(f'Configuration file could not be read: {e}')
            sys.exit(1)

    config["max_events"] = args.max_events

    r0_to_dl1.r0_to_dl1(
        args.input_file,
        output_filename=output_filename,
        custom_config=config,
        pedestal_path=args.pedestal_file,
        calibration_path=args.calibration_file,
        time_calibration_path=args.time_calibration_file,
        pointing_file_path=args.pointing_file_file,
        ucts_t0_dragon=args.ucts_t0_dragon,
        dragon_counter0=args.dragon_counter0,
        ucts_t0_tib=args.ucts_t0_tib,
        tib_counter0=args.tib_counter0
    )


if __name__ == '__main__':
    main()
