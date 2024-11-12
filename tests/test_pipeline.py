from PIL import Image
from extractor.pipeline.inference import DonutInferenceEngine
from extractor.pipeline.postprocessor import GeotechnicalPostProcessor

def test_mock_inference_and_postprocessing():
    engine = DonutInferenceEngine(mode="mock")
    dummy_img = Image.new("RGB", (600, 800), color=(255, 255, 255))
    
    raw = engine.infer(dummy_img)
    assert "parsed" in raw
    assert raw["confidence"] > 0.9
    
    post = GeotechnicalPostProcessor()
    result = post.process_raw_tokens("test.pdf", raw)
    assert result.metadata.borehole_id == "BH-01"
    assert len(result.strata) >= 1
    assert result.status == "COMPLETED"
