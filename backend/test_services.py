from ... import services

def test_get_pest_alerts_success():
    """Tests that a valid pest alert is returned for a known crop and stage."""
    crop = "rice"
    stage = "vegetative"
    expected_alert = "Stem Borer Alert!"
    assert services._get_pest_alerts(crop, stage) == expected_alert

def test_get_pest_alerts_fallback():
    """Tests that a fallback message is returned for an unknown stage."""
    crop = "rice"
    stage = "unknown_stage"
    expected_fallback = "No specific pest alerts for this stage."
    assert services._get_pest_alerts(crop, stage) == expected_fallback