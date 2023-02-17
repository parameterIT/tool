from pathlib import Path
import sys
from byoqm.models.code_climate import CodeClimate
from byoqm.qualitymodel.qualitymodel import QualityModel


def parse_src_root() -> Path:
    if len(sys.argv) == 1:
        print("Make sure to provide the path to source code")
        exit(1)

    path_to_src = Path(sys.argv[1])
    if not path_to_src.exists():
        print(f"The source code at {path_to_src.resolve()} does not exist")
        exit(1)

    return path_to_src


if __name__ == "__main__":
    src_root: Path = parse_src_root()

    qm: QualityModel = CodeClimate()
    qm.set_src_root(src_root)
    print(qm.getDesc()["lines of code"]())
    print(qm.getDesc()["method length"]())
