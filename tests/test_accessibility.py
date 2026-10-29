"""Unit tests to ensure accessibility standards are maintained."""

def test_app_contains_aria_landmarks():
    """Verify that the main app code includes semantic HTML landmarks."""
    with open("app.py", "r", encoding="utf-8") as f:
        code = f.read()
    
    # Check for main landmark
    assert '<main aria-label="' in code
    # Check for focus CSS
    assert 'outline: 3px solid' in code
    # Check for help texts on forms
    assert 'help="Enter the expected number of attendees."' in code

def test_accessibility_documentation_exists():
    """Verify that the WCAG compliance document is present in the repo."""
    import os
    assert os.path.exists("ACCESSIBILITY.md"), "ACCESSIBILITY.md is missing"