import dataclasses
from pathlib import Path

path = Path("src/spektrafilm_gui/virtual_photo_paper_back.py")
content = path.read_text()

search = """def render_virtual_photo_paper_back(
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
    measure_timing=False,
):
    t0 = perf_counter() if measure_timing else 0.0
    canvas_width, canvas_height = (canvas_size, canvas_size) if isinstance(canvas_size, int) else canvas_size"""

replace = """def render_virtual_photo_paper_back(
    config: VirtualPhotoPaperBackConfig | None = None,
    measure_timing: bool = False,
    **kwargs,
):
    if config is None:
        config = VirtualPhotoPaperBackConfig(**kwargs)
    elif kwargs:
        config = dataclasses.replace(config, **kwargs)

    t0 = perf_counter() if measure_timing else 0.0
    canvas_width, canvas_height = (config.canvas_size, config.canvas_size) if isinstance(config.canvas_size, int) else config.canvas_size"""

content = content.replace(search, replace, 1)

content = content.replace(
    "background = np.asarray(background_rgb, dtype=np.float32)",
    "background = np.asarray(config.background_rgb, dtype=np.float32)"
)
content = content.replace(
    "logo = np.asarray(DEFAULT_LOGO_RGB if logo_rgb is None else logo_rgb, dtype=np.float32)",
    "logo = np.asarray(DEFAULT_LOGO_RGB if config.logo_rgb is None else config.logo_rgb, dtype=np.float32)"
)
content = content.replace(
    "tile_scale = float(zoom) * canvas_long_edge / float(max(source_alpha.shape))",
    "tile_scale = float(config.zoom) * canvas_long_edge / float(max(source_alpha.shape))"
)
content = content.replace(
    "tile_alpha, inverse_alpha, scaled_width = prepare_tile_stamp(tile_scale, float(angle))",
    "tile_alpha, inverse_alpha, scaled_width = prepare_tile_stamp(tile_scale, float(config.angle))"
)
content = content.replace(
    "spacing = None if center_distance is None else float(center_distance) * canvas_long_edge",
    "spacing = None if config.center_distance is None else float(config.center_distance) * canvas_long_edge"
)
content = content.replace(
    "basis = build_rhombic_basis(scaled_width, overlap, rombic_grid_angle, angle, spacing)",
    "basis = build_rhombic_basis(scaled_width, config.overlap, config.rombic_grid_angle, config.angle, spacing)"
)
content = content.replace(
    "float(phase_horizontal) * canvas_long_edge",
    "float(config.phase_horizontal) * canvas_long_edge"
)
content = content.replace(
    "float(phase_vertical) * canvas_long_edge",
    "float(config.phase_vertical) * canvas_long_edge"
)
content = content.replace(
    "glare_map = build_glare_map(canvas_shape, glare, seed)",
    "glare_map = build_glare_map(canvas_shape, config.glare, config.seed)"
)
content = content.replace(
    "variation *= 0.07 * glare",
    "variation *= 0.07 * config.glare"
)
content = content.replace(
    "lift *= 0.42 * glare",
    "lift *= 0.42 * config.glare"
)

path.write_text(content)
