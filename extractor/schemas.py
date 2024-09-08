from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field
try:
    from pydantic import field_validator
except ImportError:
    from pydantic import validator as field_validator

class BoreholeMetadata(BaseModel):
    borehole_id: str = Field(..., description="Unique Borehole Identifier, e.g., BH-01", examples=["BH-01"])
    project_name: str = Field(..., description="Name of the infrastructure project")
    location: Optional[str] = Field(None, description="Drill site location or coordinates")
    drilling_method: Optional[str] = Field("Hollow Stem Auger", description="Equipment method used")
    elevation_m: Optional[float] = Field(None, description="Ground surface elevation in meters")
    water_table_depth_m: Optional[float] = Field(None, description="Measured groundwater level in meters")
    total_depth_m: float = Field(..., description="Total drilled termination depth in meters")
    logged_date: Optional[date] = Field(None, description="Date of logging completion")

class StrataLayer(BaseModel):
    layer_number: int = Field(..., ge=1)
    depth_from_m: float = Field(..., ge=0.0)
    depth_to_m: float = Field(..., gt=0.0)
    thickness_m: Optional[float] = Field(None)
    uscs_group: Optional[str] = Field(None, description="Unified Soil Classification System code (e.g. SP, CL)")
    lithology_description: str = Field(..., description="Field geological description of strata")
    consistency_or_density: Optional[str] = Field(None, description="e.g. Very Stiff, Dense, Medium")

    def validate_depth(self):
        if self.depth_to_m <= self.depth_from_m:
            raise ValueError(f"depth_to_m ({self.depth_to_m}) must be greater than depth_from_m ({self.depth_from_m})")

class SPTRecord(BaseModel):
    sample_id: str
    depth_m: float
    blow_counts: List[int] = Field(default_factory=list, description="3-interval blow counts (e.g. [4, 6, 8])")
    n_value: int = Field(..., description="Standard Penetration Test N-value (blows/ft)")
    recovery_percent: Optional[float] = Field(None, ge=0.0, le=100.0)

class ExtractionResult(BaseModel):
    document_name: str
    status: str = "COMPLETED"
    processing_time_ms: float
    confidence_score: float = Field(ge=0.0, le=1.0)
    metadata: BoreholeMetadata
    strata: List[StrataLayer]
    spt_records: List[SPTRecord]
    notes: List[str] = Field(default_factory=list)
