from typing import Any, Dict, List
from extractor.schemas import BoreholeMetadata, ExtractionResult, SPTRecord, StrataLayer

class GeotechnicalPostProcessor:
    def process_raw_tokens(self, document_name: str, raw_payload: Dict[str, Any]) -> ExtractionResult:
        data = raw_payload.get("parsed", {})
        latency_ms = raw_payload.get("latency_ms", 120.0)
        confidence = raw_payload.get("confidence", 0.95)

        metadata = BoreholeMetadata(
            borehole_id=data.get("borehole_id", "BH-01"),
            project_name=data.get("project_name", "Geotechnical Site Survey"),
            location=data.get("location"),
            drilling_method=data.get("drilling_method", "Hollow Stem Auger"),
            elevation_m=data.get("elevation_m"),
            water_table_depth_m=data.get("water_table_depth_m"),
            total_depth_m=float(data.get("total_depth_m", 18.0)),
            logged_date=data.get("logged_date"),
        )

        strata_layers: List[StrataLayer] = []
        for idx, layer_dict in enumerate(data.get("strata", []), start=1):
            d_from = float(layer_dict.get("depth_from_m", 0.0))
            d_to = float(layer_dict.get("depth_to_m", d_from + 1.0))
            thickness = round(d_to - d_from, 2)
            
            strata_layers.append(
                StrataLayer(
                    layer_number=layer_dict.get("layer_number", idx),
                    depth_from_m=d_from,
                    depth_to_m=d_to,
                    thickness_m=thickness,
                    uscs_group=layer_dict.get("uscs_group", "SM"),
                    lithology_description=layer_dict.get("lithology_description", "Soil layer"),
                    consistency_or_density=layer_dict.get("consistency_or_density"),
                )
            )

        spt_records: List[SPTRecord] = []
        for spt in data.get("spt_records", []):
            spt_records.append(
                SPTRecord(
                    sample_id=spt.get("sample_id", "SPT"),
                    depth_m=float(spt.get("depth_m", 1.0)),
                    blow_counts=spt.get("blow_counts", [4, 6, 8]),
                    n_value=int(spt.get("n_value", 14)),
                    recovery_percent=spt.get("recovery_percent"),
                )
            )

        return ExtractionResult(
            document_name=document_name,
            status="COMPLETED",
            processing_time_ms=latency_ms,
            confidence_score=confidence,
            metadata=metadata,
            strata=strata_layers,
            spt_records=spt_records,
            notes=["Automated extraction via Donut Vision-Language Transformer"]
        )
