from pathlib import Path
from typing import Dict, List, NamedTuple, Union

import lxml.etree as ET

XML = ET._Element

def read_all_workflow_files(build_dir: Path) -> List[XML]:
    result = []
    for x in build_dir.glob('workflow/*.xml'):
        result.append(ET.parse(x))
    return result
