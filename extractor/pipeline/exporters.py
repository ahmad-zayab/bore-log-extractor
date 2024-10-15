import csv
import io
from pathlib import Path
from typing import Dict, Union
from extractor.schemas import ExtractionResult

class DocumentExporter:
    @staticmethod
    def to_json(result: ExtractionResult, indent: int = 2) -> str:
        return result.model_dump_json(indent=indent) if hasattr(result, model_dump_json) else result.json(indent=indent)

    @staticmethod
    def to_csv(result: ExtractionResult) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(["# Borehole ID", result.metadata.borehole_id])
        writer.writerow(["# Project", result.metadata.project_name])
        writer.writerow(["# Total Depth (m)", result.metadata.total_depth_m])
        writer.writerow([])
        
        writer.writerow(["Layer", "Depth_From_m", "Depth_To_m", "Thickness_m", "USCS", "Lithology_Description", "Consistency_Density"])
        for layer in result.strata:
            writer.writerow([
                layer.layer_number,
                layer.depth_from_m,
                layer.depth_to_m,
                layer.thickness_m,
                layer.uscs_group or "",
                layer.lithology_description,
                layer.consistency_or_density or "",
            ])
            
        return output.getvalue()

    @staticmethod
    def save_to_disk(result: ExtractionResult, output_dir: Union[str, Path], prefix: str = None) -> Dict[str, Path]:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        base_name = prefix or result.metadata.borehole_id.replace(" ", "_")
        
        json_file = out_path / f"{base_name}_extracted.json"
        csv_file = out_path / f"{base_name}_strata.csv"
        
        json_file.write_text(DocumentExporter.to_json(result), encoding="utf-8")
        csv_file.write_text(DocumentExporter.to_csv(result), encoding="utf-8")
        
        return {"json": json_file, "csv": csv_file}
