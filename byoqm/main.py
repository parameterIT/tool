from pathlib import Path
from metric import Metric
from qm_parser import YMLParser

parser = YMLParser()
path = Path('yml_test_file.yml')
parser.parse(path.resolve())
