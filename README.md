# midi-plus

A capacitive touch MIDI keyboard featuring 12 chromatic keys, low-profile mechanical switches, slide potentiometers, rotary encoder navigation, and a bespoke high-precision mechanical enclosure.

---

## ✨ Features

- **12 Capacitive Touch Keys**: Full 1-octave chromatic piano layout (7 naturals + 5 accidentals) etched into the PCB surface for lightning-fast touch sensing.
- **3 Kailh Choc Low-Profile Switches**: Tactile buttons (`SW1`, `SW2`, `SW3`) with reverse-mount SK6812 RGB LED backlighting for mode switching, octave transposition, or preset selection.
- **EC11 Rotary Encoder**: Multi-turn rotary encoder with integrated push button (`SW4`) for parameter scrubbing and menu selection.
- **Dual Bourns Slide Potentiometers**: 15mm stroke faders (`RV1`, `RV2`) for pitch bend, modulation, filter cutoff, or volume control.
- **Raspberry Pi Pico (RP2040)**: Core microcontroller providing USB-MIDI connectivity and capacitive sensing via an onboard resistor ladder network (`R1`–`R12`).
- **Precision 3D Enclosure**: Custom two-piece clamshell console enclosure engineered in CAD (`build123d` / OpenCASCADE) with an ergonomic 3.95° incline, zero-screw PCB clamping, and tongue-and-groove alignment.

---

## 🎛️ 3D Enclosure STEP Files

The enclosure CAD models are located in [`Case3D/`](Case3D/):

- **[Case + PCB Master Assembly (`midi_plus_case_assembled.step`)](Case3D/midi_plus_case_assembled.step)**: Full assembly with the KiCad PCB seated inside the enclosure.
- **[Complete Case (`midi_plus_case.step`)](Case3D/midi_plus_case.step)**: Top Shell and Bottom Shell mated together.
- **[Top Console Shell (`midi_plus_top_shell.step`)](Case3D/midi_plus_top_shell.step)**: Upper faceplate with ergonomic console slope, capacitive key window, switch wells, and slider slots.
- **[Bottom Base Shell (`midi_plus_bottom_shell.step`)](Case3D/midi_plus_bottom_shell.step)**: Lower enclosure with internal PCB support shelf, countersunk screw bores, and non-slip foot pockets.
- **[Enclosure Documentation (`Case3D/README.md`)](Case3D/README.md)**: Mechanical tolerances, stackup specifications, and assembly instructions.

---

## 📂 Repository Structure

```
midi-plus/
├── BOM.csv                       # Bill of materials
├── JOURNAL.md                    # Hardware development log
├── README.md                     # Project overview and specifications
├── KiCad/                        # KiCad PCB and schematic files
│   ├── KiCad.kicad_pcb           # PCB layout
│   ├── KiCad.kicad_sch           # Schematic
│   ├── pcb.step                  # KiCad exported PCB 3D STEP model
│   └── ModelsAndSymbols/         # 3D component STEP models (Bourns, EC11)
└── Case3D/                       # Precision Mechanical Enclosure
    ├── README.md                 # Enclosure specifications and assembly guide
    ├── generate_case.py          # Parametric CAD generator (build123d)
    ├── midi_plus_case_assembled.step  # Master assembly (Case + PCB)
    ├── midi_plus_case.step            # Complete two-piece case
    ├── midi_plus_top_shell.step       # Top console shell
    └── midi_plus_bottom_shell.step    # Bottom base shell
```
