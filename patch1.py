import dataclasses
from pathlib import Path

path = Path("src/spektrafilm_gui/virtual_photo_paper_back.py")
content = path.read_text()

import_dataclasses = "import dataclasses\nfrom functools import lru_cache\n"
content = content.replace("from functools import lru_cache\n", import_dataclasses, 1)

dataclass_def = """

@dataclasses.dataclass(frozen=True, slots=True)
class VirtualPhotoPaperBackConfig:
    canvas_size: tuple[int, int] | int = DEFAULT_CANVAS_SIZE
    zoom: float = GRID_SCALE
    angle: float = GLOBAL_ROTATION
    overlap: float = OVERLAP_FRACTION
    center_distance: float | None = DEFAULT_CENTER_DISTANCE
    logo_rgb: np.ndarray | None = dataclasses.field(default_factory=lambda: DEFAULT_LOGO_RGB)
    background_rgb: np.ndarray = dataclasses.field(default_factory=lambda: DEFAULT_BACKGROUND_RGB)
    glare: float = DEFAULT_GLARE
    rombic_grid_angle: float = ROMBIC_GRID_ANGLE
    phase_horizontal: float = PHASE_HORIZONTAL
    phase_vertical: float = PHASE_VERTICAL
    seed: int | None = 0


@lru_cache(maxsize=1)"""

content = content.replace("\n\n@lru_cache(maxsize=1)", dataclass_def, 1)

path.write_text(content)
