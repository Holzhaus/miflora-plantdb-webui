# -*- coding: utf-8 -*-
import argparse
import json
import pathlib

import jinja2

from . import db


def main(argv: list[str] | None = None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        help="MifloraDB CSV file",
        type=argparse.FileType("r", encoding="gb18030"),
    )
    parser.add_argument(
        "-o", "--output-dir", help="Output Directory", type=pathlib.Path, required=True
    )
    parser.add_argument("-u", "--base-url", help="Base URL", default="")
    args = parser.parse_args(argv)

    plants = list(db.read_db_from_fp(args.file))

    env = jinja2.Environment(
        loader=jinja2.PackageLoader(__package__, "templates"),
        autoescape=jinja2.select_autoescape(["html", "xml"]),
    )

    plant_template = env.get_template("plant.html")
    plant_directory = args.output_dir.joinpath("plant")
    plant_directory.mkdir(exist_ok=True, parents=True)
    for plant in plants:
        markup = plant_template.render(plant=plant, base_url=args.base_url)
        with plant_directory.joinpath(f"{plant.slug}.html").open("w") as fp:
            fp.write(markup)
        with plant_directory.joinpath(f"{plant.slug}.json").open("w") as fp:
            json.dump(plant._asdict(), fp)

    plant_template = env.get_template("index.html")
    markup = plant_template.render(plants=plants, base_url=args.base_url)
    with args.output_dir.joinpath(f"index.html").open("w") as fp:
        fp.write(markup)
    with args.output_dir.joinpath(f"index.json").open("w") as fp:
        json.dump(
            {plant.display_pid: f"{args.base_url}plant/{plant.slug}.json" for plant in plants}, fp
        )
