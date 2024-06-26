# -*- coding: utf-8 -*-
import csv
import io
import typing

import slugify


class Plant(typing.NamedTuple):
    slug: str
    pid: str
    display_pid: str
    alias: str
    image: str
    floral_language: str
    origin: str
    production: str
    category: str
    blooming: str
    color: str
    size: str
    soil: str
    sunlight: str
    watering: str
    fertilization: str
    pruning: str
    max_light_mmol: int
    min_light_mmol: int
    max_light_lux: int
    min_light_lux: int
    max_temp: int
    min_temp: int
    max_env_humid: int
    min_env_humid: int
    max_soil_moist: int
    min_soil_moist: int
    max_soil_ec: int
    min_soil_ec: int


def read_db_from_fp(file: io.TextIOBase) -> typing.Iterable[Plant]:
    reader = csv.DictReader(file)
    for row in reader:
        data = row.copy()
        data["slug"] = slugify.slugify(row["pid"])
        for key, value in row.items():
            if not (key.startswith("min_") or key.startswith("max_")):
                continue
            data[key] = int(value)

        yield Plant(**data)
