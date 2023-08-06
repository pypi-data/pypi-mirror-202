"""Utilities for performing fun math on healpix pixels"""

from .healpix_pixel import HealpixPixel
from .hipscat_id import compute_hipscat_id, hipscat_id_to_healpix
from .partition_stats import (
    empty_histogram,
    generate_alignment,
    generate_destination_pixel_map,
    generate_histogram,
    compute_pixel_map,
)
from .pixel_margins import (get_edge, get_margin, pixel_is_polar,
                            get_truncated_margin_pixels)
from .margin_bounding import (get_margin_scale, get_margin_bounds_and_wcs,
                              check_margin_bounds, check_polar_margin_bounds)
