from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from extractor.pipeline.preprocessor import DocumentPreprocessor
from extractor.pipeline.inference import DonutInferenceEngine
from extractor.pipeline.postprocessor import GeotechnicalPostProcessor
from extractor.pipeline.exporters import DocumentExporter

app = typer.Typer(help="Automated Geotechnical Bore Log Extraction CLI")
console = Console()

@app.command("extract")
def extract_document(
    input_file: Path = typer.Option(..., "--input", "-i", help="Path to Bore Log PDF or Image"),
    output_dir: Path = typer.Option(Path("data/output"), "--output-dir", "-o", help="Target output folder"),
    mode: str = typer.Option("mock", "--mode", "-m", help="Inference mode: 'mock' or 'production'"),
):
    console.print(f"[bold cyan]Starting extraction on:[/bold cyan] {input_file} (Mode: {mode})")
    
    preprocessor = DocumentPreprocessor()
    images = preprocessor.load_document_images(input_file)
    
    engine = DonutInferenceEngine(mode=mode)
    raw_output = engine.infer(images[0])
    
    postprocessor = GeotechnicalPostProcessor()
    result = postprocessor.process_raw_tokens(input_file.name, raw_output)
    
    table = Table(title=f"Extracted Strata - {result.metadata.borehole_id}")
    table.add_column("Layer", style="cyan")
    table.add_column("Depth (m)", style="green")
    table.add_column("USCS", style="magenta")
    table.add_column("Lithology Description", style="white")
    
    for layer in result.strata:
        table.add_row(
            str(layer.layer_number),
            f"{layer.depth_from_m} - {layer.depth_to_m}",
            layer.uscs_group or "-",
            layer.lithology_description
        )
    console.print(table)
    
    saved = DocumentExporter.save_to_disk(result, output_dir, prefix=result.metadata.borehole_id)
    console.print(f"[bold green]✓ Outputs exported successfully to:[/bold green] {output_dir}")

@app.command("version")
def version():
    console.print("Bore Log Extractor Engine v1.0.0 (Python 3.11 + Donut Transformer)")

if __name__ == "__main__":
    app()
