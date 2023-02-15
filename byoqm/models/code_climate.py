from pathlib import Path
from typing import Dict
from pathlib import Path

SRC_ROOT = [Path()]


#'byoqm/metric'
def getDesc() -> Dict:
    model = {
        "maintainability": maintainability,
        "duplication": duplication,
        "lines of code": file_length,
    }
    return model


def maintainability():
    return 7 + duplication()


def duplication() -> int | float:
    return identical_blocks_of_code() + similar_blocks_of_code()


def cognitive_complexity():
    pass


def cyclomatic_complexity():
    pass


def argument_count():
    pass


def complex_logic():
    pass


def file_length():
    src_files = list(SRC_ROOT[0].glob("**/*.py"))
    count = 0
    for file in src_files:
        loc = sum(1 for line in open(file))
        if loc > 250:
            count += 1
    return count


def identical_blocks_of_code() -> int | float:
    return 2


def method_complexity():
    pass


def method_count():
    pass


def method_length():
    pass


def nested_control_flow():
    pass


def return_statements():
    pass


def similar_blocks_of_code() -> int | float:
    return 3
