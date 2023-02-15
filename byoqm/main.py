from pathlib import Path
import sys
from byoqm.models.code_climate import getDesc
from models import code_climate

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Make sure to provide the path to source code")
        exit(1)

    path_to_src = Path(sys.argv[1])
    if not path_to_src.exists():
        print(f"The source code at {path_to_src.resolve()} does not exist")
        exit(1)

    code_climate.SRC_ROOT[0] = path_to_src
