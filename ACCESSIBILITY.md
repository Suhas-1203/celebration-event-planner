# Accessibility Statement (WCAG 2.1 Compliance)

This application is designed to be inclusive and accessible, following the Web Content Accessibility Guidelines (WCAG) 2.1 Level AA standards.

## Implemented Features:
- **Semantic Landmarks:** The main application is wrapped in a `<main>` landmark with an explicit `aria-label`.
- **Keyboard Navigation:** Custom CSS ensures all interactive elements (buttons, inputs, checkboxes) have a highly visible `:focus` outline for users who rely on keyboard navigation.
- **High Contrast:** Text and interactive elements utilize high-contrast colors (e.g., `#FAFAFA` on dark backgrounds) to ensure readability for users with low vision.
- **Screen Reader Support:** All major sections include explicit `aria-label` attributes. Form fields include descriptive `help` text.
- **Language Declaration:** The document language is explicitly set to English (`lang="en"`).
- **Accessible Forms:** Every input field has a visible label, and placeholders are used only for supplementary examples, never as primary labels.

## Testing Accessibility
To test the accessibility of this Streamlit app locally:
1. Use the `Tab` key to navigate through the form. Verify that a red outline appears on every focused element.
2. Use a screen reader (e.g., NVDA on Windows, VoiceOver on macOS) to navigate the page and verify that headings and form labels are read correctly.