from pathlib import Path
from sqlalchemy.orm import Query
from threedi_schema import models
from threedi_schema import ThreediDatabase
from typing import Dict
from typing import Optional


RASTERS = [
    "dem_file",
    "frict_coef_file",
    "interception_file",
    # Interflow
    "porosity_file",
    "hydraulic_conductivity_file",
    # Simple infiltration
    "infiltration_rate_file",
    "max_infiltration_capacity_file",
    # Groundwater
    "initial_infiltration_rate_file",
    "equilibrium_infiltration_rate_file",
    "infiltration_decay_period_file",
    "phreatic_storage_capacity_file",
    "groundwater_impervious_layer_level_file",
    "groundwater_hydro_connectivity_file",
    # Initials
    "initial_waterlevel_file",
    "initial_groundwater_level_file",
    # Vegetation
    "vegetation_height_file",
    "vegetation_drag_coefficient_file",
    "vegetation_stem_count_file",
    "vegetation_stem_diameter_file",
]


__all__ = ["ModelDB"]


MIN_SQLITE_VERSION = 227


class ModelDB:
    """Interface to sqlite of a model."""

    def __init__(
        self,
        sqlite_path: Path,
        global_settings_id: Optional[int] = None,
        upgrade: bool = False,
    ):
        if not sqlite_path.exists():
            raise ValueError(f"Sqlite path {sqlite_path} does not exist.")

        self.sqlite_path = sqlite_path
        self.database = ThreediDatabase(self.sqlite_path.as_posix())

        version = self.get_version()
        if version < MIN_SQLITE_VERSION:
            if upgrade:
                self.upgrade()
            else:
                raise ValueError(f"Too old sqlite version {version}.")

        if global_settings_id:
            self.global_settings_id = global_settings_id

        try:
            session = self.database.get_session()
            self.model_settings = (
                session.query(models.ModelSettings).order_by("id").first()
            )
            self.global_settings_name = ""
        finally:
            session.close()

    def get_version(self) -> int:
        # check version
        return self.database.schema.get_version()

    def upgrade(self) -> None:
        self.database.schema.upgrade()

    def get_raster_filepaths(self, base_path: Path) -> Dict:
        raster_filepaths = {}
        for raster in RASTERS:
            raster_path = getattr(self.model_settings, raster, None)
            if raster_path:
                raster_filepaths[raster] = base_path / Path(
                    raster_path.replace("\\", "/")
                )
        return raster_filepaths

    def initial_waterlevels(self):
        try:
            session = self.database.get_session()
            initial_conditions = (
                Query(models.InitialConditions).with_session(session).first()
            )
            initial_waterlevel = (
                initial_conditions.initial_groundwater_level_aggregation,
                initial_conditions.initial_water_level,
            )
            initial_groundwater_level = (
                initial_conditions.initial_groundwater_level_aggregation,
                initial_conditions.initial_groundwater_level,
            )
        finally:
            session.close()
        return initial_waterlevel, initial_groundwater_level