#!/usr/bin/env python3

"""
python examples/benches/launcher.py --world_size 2 --tensor_size 1000,10 --multiprocess
"""

import argparse
import logging
import os

import curl
import torch
from curl.config import cfg
from examples.multiprocess_launcher import MultiProcessLauncher


def get_args():
    def tuple_type(s):
        try:
            # Split the string into integers
            elements = tuple(map(int, s.split(",")))
            return elements
        except ValueError:
            # Raise an error if parsing fails
            raise argparse.ArgumentTypeError(
                "Tuple format must be integers separated by commas"
            )

    parser = argparse.ArgumentParser(description="Curl Non-Linear Functions")
    parser.add_argument(
        "--world_size",
        type=int,
        default=2,
        help="The number of parties to launch. Each party acts as its own process",
    )
    parser.add_argument(
        "-s",
        "--tensor_size",
        type=tuple_type,
        default=(10, 10),
        help="The size of the tensors as a tuple of integers separated by commas (e.g., '100,100,50')",
    )
    parser.add_argument(
        "--multiprocess",
        default=False,
        action="store_true",
        help="Run example in multiprocess mode",
    )
    parser.add_argument(
        "--approximations",
        default=False,
        action="store_true",
        help="Use approximations for non-linear functions",
    )
    parser.add_argument(
        "--lut_only",
        default=False,
        action="store_true",
        help="Use lut only for bounded functions",
    )
    parser.add_argument(
        "--communication",
        default=False,
        action="store_true",
        help="Print communication statistics",
    )
    parser.add_argument(
        "--with-cache",
        default=False,
        action="store_true",
        help="Populate the cache and run with it",
    )
    parser.add_argument(
        "--device",
        "-d",
        required=False,
        default="cpu",
        help="the device to run the benchmarks",
    )
    parser.add_argument(
        "--multi-gpu",
        "-mg",
        required=False,
        default=False,
        action="store_true",
        help="use different gpu for each party. Will override --device if selected",
    )
    args = parser.parse_args()
    return args


def get_config(args):
    cfg_file = curl.cfg.get_default_config_path()
    if args.approximations:
        logging.info("Using Approximation Config:")
        cfg_file = cfg_file.replace("default", "approximations")
    elif args.lut_only:
        logging.info("Using LUT-only Config:")
        cfg_file = cfg_file.replace("default", "lut_only")
    else:
        logging.info("Using LUTs Config:")
    return cfg_file


def _run_experiment(args):
    # only import here to initialize curl within the subprocesses
    from examples.benches.benches import run_benches

    # Only Rank 0 will display logs.
    level = logging.INFO
    if "RANK" in os.environ and os.environ["RANK"] != "0":
        level = logging.CRITICAL
    logging.getLogger().setLevel(level)

    cfg_file = get_config(args)
    run_benches(
        cfg_file, args.tensor_size, args.with_cache, args.communication, args.device
    )

    print("Done")


def main(run_experiment):
    args = get_args()
    cfg_file = get_config(args)
    curl.cfg.load_config(cfg_file)

    if args.communication and cfg.mpc.provider == "TTP":
        raise ValueError("Communication statistics are not available for TTP provider")

    if args.multiprocess:
        launcher = MultiProcessLauncher(args.world_size, run_experiment, args, cfg_file)
        launcher.start()
        launcher.join()
        launcher.terminate()
    else:
        run_experiment(args)


if __name__ == "__main__":
    main(_run_experiment)
