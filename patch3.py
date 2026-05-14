import dataclasses
from pathlib import Path

path = Path("src/spektrafilm_gui/virtual_photo_paper_back.py")
content = path.read_text()

search = """def virtual_photo_paper_back(
    canvas_size=DEFAULT_CANVAS_SIZE,
    zoom=GRID_SCALE,
    angle=GLOBAL_ROTATION,
    overlap=OVERLAP_FRACTION,
    center_distance=DEFAULT_CENTER_DISTANCE,
    logo_rgb=DEFAULT_LOGO_RGB,
    background_rgb=DEFAULT_BACKGROUND_RGB,
    glare=DEFAULT_GLARE,
    rombic_grid_angle=ROMBIC_GRID_ANGLE,
    phase_horizontal=PHASE_HORIZONTAL,
    phase_vertical=PHASE_VERTICAL,
    seed=0,
    print_timing=False,
):
    canvas, centers, timings = render_virtual_photo_paper_back(
        canvas_size=canvas_size,
        zoom=zoom,
        angle=angle,
        overlap=overlap,
        center_distance=center_distance,
        logo_rgb=logo_rgb,
        background_rgb=background_rgb,
        glare=glare,
        rombic_grid_angle=rombic_grid_angle,
        phase_horizontal=phase_horizontal,
        phase_vertical=phase_vertical,
        seed=seed,
        measure_timing=print_timing,
    )"""

replace = """def virtual_photo_paper_back(
    config: VirtualPhotoPaperBackConfig | None = None,
    print_timing: bool = False,
    **kwargs,
):
    if config is None:
        config = VirtualPhotoPaperBackConfig(**kwargs)
    elif kwargs:
        config = dataclasses.replace(config, **kwargs)

    canvas, centers, timings = render_virtual_photo_paper_back(
        config=config, measure_timing=print_timing
    )"""

content = content.replace(search, replace, 1)

content = content.replace(
    "canvas_width, canvas_height = (canvas_size, canvas_size) if isinstance(canvas_size, int) else canvas_size",
    "canvas_width, canvas_height = (config.canvas_size, config.canvas_size) if isinstance(config.canvas_size, int) else config.canvas_size"
)

path.write_text(content)
