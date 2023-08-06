from json import loads, dumps
import ast
import argparse
from io import open

from abml.abml_dataclass import Abml_Cae
from abml.abml_helpers import exit_handler, cprint
from yaml import load as yload
from yaml import Loader
import os

import logging


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif value.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--cae", type=str, default=None)
group.add_argument("--file", type=str, default=None)
parser.add_argument("--name", type=str, default=None)
parser.add_argument("--input_type", type=str, default=None)
parser.add_argument("--input_folder", type=str, default="inputs")
parser.add_argument("--test", type=str_to_bool, default=False)

args, _ = parser.parse_known_args()

if args.cae is not None:
    args_string = args.cae.replace("'", '"')
    cae = ast.literal_eval(dumps(loads(args.cae.replace("'", '"'), encoding="utf-8")))
elif args.file is not None:
    with open(args.file, mode="r", encoding="utf-8") as f:
        cae = yload(f, Loader=Loader)


if __name__ == "__main__":
    logger = logging.getLogger()

    if args.test:
        logger.setLevel(logging.INFO)

    fh = logging.FileHandler(
        filename="{}.abml.log".format(args.name),
        mode="w",
        encoding="utf-8",
    )
    formatter = logging.Formatter("%(levelname)s - %(module)s - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    if "cae" in globals():
        cae = Abml_Cae(cae, test=args.test)
        exit_handler()

        cprint(args.test)
        if not args.test:
            cprint(args.test)
            cae.save_cae("{}.cae".format(args.name))

            if args.input_type == "copy":
                if not os.path.isdir(args.input_folder):
                    os.mkdir(args.input_folder)
                for model in cae.models:
                    if hasattr(cae.models[model], "jobs"):
                        for job in cae.models[model].jobs:
                            cae.models[model].jobs[job].write_and_copy_input_to_path(args.input_folder)

            elif args.input_type == "move":
                if not os.path.isdir(args.input_folder):
                    os.mkdir(args.input_folder)
                for model in cae.models:
                    if hasattr(cae.models[model], "jobs"):
                        for job in cae.models[model].jobs:
                            cae.models[model].jobs[job].write_and_move_input_to_path(args.input_folder)
