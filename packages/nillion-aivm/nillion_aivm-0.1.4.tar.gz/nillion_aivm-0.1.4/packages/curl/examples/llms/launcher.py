#!/usr/bin/env python3

"""
python examples/llms/launcher.py --world_size 2 --tensor_size 1000,10 --multiprocess
"""

import argparse
import logging
import os

import curl
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

    parser = argparse.ArgumentParser(description="Curl LLM Inference")
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
        "--no-cmp",
        default=False,
        action="store_true",
        help="Use LUTs for bounded functions without comparisons",
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
        "--not-full",
        default=False,
        action="store_true",
        help="Skip embeddings and softmax",
    )
    models = ["GPT2", "GPTNeo", "BertTiny", "BertBase", "BertLarge", "all"]
    parser.add_argument(
        "--model",
        choices=models,
        required=True,
        help="Choose a model to run from the following options: {}".format(models),
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
    elif args.no_cmp:
        logging.info("Using config with LUTs without comparisons:")
        cfg_file = cfg_file.replace("default", "llm_config")
    else:
        logging.info("Using LUTs Config:")
    return cfg_file


def _run_experiment(args):
    # only import here to initialize curl within the subprocesses
    from examples.llms.llm import run_llm

    # Only Rank 0 will display logs.
    level = logging.INFO
    if "RANK" in os.environ and os.environ["RANK"] != "0":
        level = logging.CRITICAL
    logging.getLogger().setLevel(level)

    cfg_file = get_config(args)
    run_llm(
        cfg_file,
        args.tensor_size,
        args.model,
        args.with_cache,
        args.communication,
        not args.not_full,
        args.device,
    )

    print("Done")


def main():
    args = get_args()
    cfg_file = get_config(args)
    curl.cfg.load_config(cfg_file)

    if args.communication and cfg.mpc.provider == "TTP":
        raise ValueError("Communication statistics are not available for TTP provider")

    if args.multiprocess:
        launcher = MultiProcessLauncher(
            args.world_size, _run_experiment, args, cfg_file
        )
        launcher.start()
        launcher.join()
        launcher.terminate()
    else:
        _run_experiment(args)


if __name__ == "__main__":
    main()
