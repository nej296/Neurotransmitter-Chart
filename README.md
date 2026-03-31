# Neurotransmitter Wheel Chart

An interactive circular wheel chart that maps **108 human neurotransmitters** across multiple concentric data rings — inspired by the mRNA codon wheel used in molecular biology, adapted for neurotransmitter classification and function.

![Screenshot](screenshot.png)

## Features

- **Interactive wheel** with 5 concentric rings: Category, NT Name, Postsynaptic Effect, Precursor, Brain Region
- **108 neurotransmitters** with complete data across all rings
- **Postsynaptic Effect classification** — color-coded ring showing Excitatory (red), Inhibitory (blue), Modulatory (purple), Mixed (gold)
- **Hover interactions** — highlight radial slices, floating tooltips
- **Click detail panel** — full encyclopedia-style entry for each NT with receptors, disorders, drugs
- **Search** — real-time find-and-highlight
- **Filters** — toggle by category and postsynaptic effect, stackable
- **Stats dashboard** — live counts by effect type and category
- **Dark/Light theme** — bioluminescent neural aesthetic by default
- **Animated intro** — wheel builds outward from center on load

## Neurotransmitter Categories

| # | Category | Color | Count |
|---|----------|-------|-------|
| 1 | Monoamines — Catecholamines | Electric Blue | 3 |
| 2 | Monoamines — Indoleamines & Trace Amines | Deep Magenta | 8 |
| 3 | Amino Acids | Emerald Green | 13 |
| 4 | Acetylcholine | Warm Amber | 1 |
| 5 | Neuropeptides — Opioid Peptides | Crimson Red | 7 |
| 6 | Neuropeptides — Non-Opioid Peptides | Coral/Salmon | 57 |
| 7 | Purines | Cyan/Teal | 5 |
| 8 | Gasotransmitters & Lipids | Lime/Chartreuse | 14 |

## Tech Stack

- **Python 3.10+**
- **Flask** — web server and templating
- **D3.js v7** — SVG wheel rendering and interactions (loaded from CDN)
- **Google Fonts (Inter)** — typography

## Installation

```bash
git clone https://github.com/nej296/Neurotransmitter-Chart.git
cd Neurotransmitter-Chart
pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000** in your browser.

## Usage

- **Hover** over any segment to highlight the full radial slice and see a tooltip
- **Click** a segment to open the detail panel with complete NT information
- **Click a category** in the center ring to filter to that category
- **Search** by name or abbreviation in the search bar
- **Filter** by category or postsynaptic effect using the sidebar toggles
- **Toggle theme** with the button in the header

## Data Sources

Neurotransmitter data was compiled from neuroscience literature including:
- StatPearls (NCBI)
- Purves et al., *Neuroscience* (6th Edition)
- Stahl, *Stahl's Essential Psychopharmacology* (5th Edition)
- Kandel et al., *Principles of Neural Science*
- Primary literature and review articles

## Running Tests

```bash
python test_app.py
# or
pytest test_app.py -v
```

The test suite validates data integrity (108 entries, all fields populated), category structure, postsynaptic effect distribution, color assignments, Flask app launch, search, filtering, and effect-to-color mapping.

## License

MIT

## Author

**Nicholas Johnson** — Computational Neuroscience, George Mason University
