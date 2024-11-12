import pytest
from pydantic import ValidationError
from extractor.schemas import BoreholeMetadata, StrataLayer

def test_valid_strata_layer():
    layer = StrataLayer(
        layer_number=1,
        depth_from_m=0.0,
        depth_to_m=2.5,
        thickness_m=2.5,
        uscs_group="CL",
        lithology_description="Stiff brown silty clay"
    )
    assert layer.thickness_m == 2.5
    assert layer.uscs_group == "CL"

def test_invalid_depth_order_raises():
    with pytest.raises(ValidationError):
        StrataLayer(
            layer_number=1,
            depth_from_m=5.0,
            depth_to_m=3.0,
            lithology_description="Invalid depth layer"
        )
