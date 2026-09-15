from __future__ import annotations

from pathlib import Path
import pandas as pd


ELEMENTS = [
    "Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon", "Nitrogen", "Oxygen", "Fluorine", "Neon",
    "Sodium", "Magnesium", "Aluminum", "Silicon", "Phosphorus", "Sulfur", "Chlorine", "Argon", "Potassium", "Calcium",
    "Scandium", "Titanium", "Vanadium", "Chromium", "Manganese", "Iron", "Cobalt", "Nickel", "Copper", "Zinc",
    "Gallium", "Germanium", "Arsenic", "Selenium", "Bromine", "Krypton", "Rubidium", "Strontium", "Yttrium", "Zirconium",
    "Niobium", "Molybdenum", "Technetium", "Ruthenium", "Rhodium", "Palladium", "Silver", "Cadmium", "Indium", "Tin",
    "Antimony", "Tellurium", "Iodine", "Xenon", "Cesium", "Barium", "Lanthanum", "Cerium", "Praseodymium", "Neodymium",
    "Promethium", "Samarium", "Europium", "Gadolinium", "Terbium", "Dysprosium", "Holmium", "Erbium", "Thulium", "Ytterbium",
    "Lutetium", "Hafnium", "Tantalum", "Tungsten", "Rhenium", "Osmium", "Iridium", "Platinum", "Gold", "Mercury",
    "Thallium", "Lead", "Bismuth", "Polonium", "Astatine", "Radon", "Francium", "Radium", "Actinium", "Thorium",
    "Protactinium", "Uranium", "Neptunium", "Plutonium", "Americium", "Curium", "Berkelium", "Californium", "Einsteinium", "Fermium",
]


def build_questions() -> pd.DataFrame:
    rows = []
    for atomic_number, element in enumerate(ELEMENTS, start=1):
        rows.append(
            {
                "question_id": f"Q{atomic_number:03d}",
                "domain": "chemistry",
                "difficulty": "easy" if atomic_number <= 20 else "moderate",
                "question": f"What is the atomic number of {element}?",
                "gold_answer": str(atomic_number),
                "clean_context": f"According to the periodic table, {element} has atomic number {atomic_number}.",
                "source": "IUPAC periodic table",
            }
        )
    return pd.DataFrame(rows)


def save_questions(path: Path) -> pd.DataFrame:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = build_questions()
    frame.to_csv(path, index=False)
    return frame
