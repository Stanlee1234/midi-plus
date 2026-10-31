#!/usr/bin/env python3
"""
MIDI+ Synthesizer - Precision Parametric 3D Case Generator
Built with build123d / OpenCASCADE for high-fidelity mechanical manufacturing.

Features:
- Two-part precision clamshell enclosure (Top Shell & Bottom Shell)
- Ergonomic 3.95-degree studio console incline for wrist comfort and visibility
- Unified 3-switch bar cutout (eliminates fragile divider bridges between switches)
- Sculpted capacitive touch keyboard aperture with 45-degree chamfered bezel
- 1x EC11 Rotary Encoder mount with recessed counterbored collar
- 2x Large ergonomic slide potentiometer openings for full travel, finger access, and fader cap clearance
- Raspberry Pi Pico / RP2040 display window with rear USB port relief tunnel
- Perimeter support shelf and internal clamping ribs (zero screws through PCB!)
- Tongue-and-groove interlocking perimeter lip
- 4x M3 brass heat-set insert corner bosses + bottom countersunk screw bores
- 4x Underside anti-slip rubber foot pockets + passive cooling convection slots
"""

import os
import math
import build123d as bd

# ---------------------------------------------------------------------------
# Global Parameters & Tolerances (all dimensions in millimeters)
# ---------------------------------------------------------------------------

# PCB Specifications (from KiCad design)
PCB_W = 176.75
PCB_D = 114.25
PCB_T = 1.60
PCB_CLEARANCE_XY = 0.40  # 0.4mm engineering clearance per side

# Enclosure Overall Envelope
CASE_W = 189.0
CASE_D = 126.0
CORNER_R = 4.5

# Z-Axis Elevation Stackup
Z_BOTTOM_FLOOR = -6.40     # Outer bottom surface
Z_CAVITY_FLOOR = -4.00     # Internal floor under PCB (2.4mm floor thickness)
Z_PCB_SEAT     = 0.00      # PCB underside resting plane (4.0mm component clearance)
Z_PARTING_LINE = 1.60      # Interface between Bottom Shell and Top Shell (= top of PCB)
Z_FRONT_TOP    = 4.80      # Top shell height at front edge (3.2mm above PCB)
Z_REAR_TOP     = 13.50     # Top shell height at rear edge (11.9mm above PCB, ~4.0 deg slope)

# Fastener Bosses (4 corners, M3 heat-set brass inserts)
SCREW_X = 90.0
SCREW_Y = 58.0
SCREW_LOCATIONS = [
    (-SCREW_X, -SCREW_Y),
    (SCREW_X, -SCREW_Y),
    (-SCREW_X, SCREW_Y),
    (SCREW_X, SCREW_Y)
]
M3_INSERT_HOLE_DIA = 4.00
M3_INSERT_DEPTH = 5.50
M3_BOSS_DIA = 6.80
M3_SCREW_HOLE_DIA = 3.40
M3_HEAD_BORE_DIA = 6.40
M3_HEAD_BORE_DEPTH = 3.20

# Component Positions in CAD coordinates (centered at PCB center X=0, Y=0)
SW_BAR_CENTER = (-48.125, 22.175)  # Center of the 3 switches (SW1, SW2, SW3)
SW_BAR_W_BOT = 51.0               # Continuous span for all 3 switches
SW_BAR_H_BOT = 15.6
SW_BAR_W_TOP = 53.0               # Chamfered top rim
SW_BAR_H_TOP = 17.6

ENC_POS = (-47.875, 41.875)

# Slider Positions & Enlarged Cutout Dimensions
RV1_POS = (-4.825, 23.475)
RV2_POS = (8.775, 23.475)
# Enlarged slider cutouts:
# Base width: 8.2mm, length: 26.5mm (generous clearance for full 15mm stroke + lever/knob)
# Top rim with smooth 45-degree chamfer: width: 10.4mm, length: 28.7mm
SLIDER_W_BOT = 8.20
SLIDER_L_BOT = 26.50
SLIDER_W_TOP = 10.40
SLIDER_L_TOP = 28.70

PICO_POS = (74.985, 30.265)
USB_X = 74.985

# Capacitive Keys Opening
KEYS_W = 173.5
KEYS_D = 58.5
KEYS_CENTER_Y = -27.25

print("Configuring MIDI+ Enclosure Model (Enlarged Slider Gaps)...")


# ---------------------------------------------------------------------------
# Part 1: Bottom Shell
# ---------------------------------------------------------------------------
def build_bottom_shell():
    print("Building Bottom Shell...")
    pocket_w = PCB_W + 2 * PCB_CLEARANCE_XY
    pocket_d = PCB_D + 2 * PCB_CLEARANCE_XY
    
    with bd.BuildPart() as bottom:
        # 1. Base solid block
        with bd.BuildSketch() as s_outer:
            bd.RectangleRounded(CASE_W, CASE_D, CORNER_R)
        bd.extrude(amount=Z_PARTING_LINE - Z_BOTTOM_FLOOR)
        bottom.part = bottom.part.translate((0, 0, Z_BOTTOM_FLOOR))
        
        # 2. Main internal cavity for PCB underside solder leads / RGB LEDs
        cavity_w = pocket_w - 4.0
        cavity_d = pocket_d - 4.0
        with bd.BuildSketch(bd.Plane.XY.offset(Z_CAVITY_FLOOR)) as s_cavity:
            bd.RectangleRounded(cavity_w, cavity_d, CORNER_R)
        bd.extrude(amount=Z_PARTING_LINE - Z_CAVITY_FLOOR + 2.0, mode=bd.Mode.SUBTRACT)
        
        # 3. PCB seating pocket (leaves continuous 2.0mm support ledge at Z_PCB_SEAT)
        with bd.BuildSketch(bd.Plane.XY.offset(Z_PCB_SEAT)) as s_pocket:
            bd.Rectangle(pocket_w, pocket_d)
        bd.extrude(amount=Z_PARTING_LINE - Z_PCB_SEAT + 1.0, mode=bd.Mode.SUBTRACT)
        
        # 4. Alignment / Interlocking Lip (Tongue)
        with bd.BuildSketch(bd.Plane.XY.offset(Z_PARTING_LINE)) as s_lip:
            bd.RectangleRounded(CASE_W, CASE_D, CORNER_R)
            bd.RectangleRounded(CASE_W - 2.4, CASE_D - 2.4, max(0.5, CORNER_R - 1.2), mode=bd.Mode.SUBTRACT)
        bd.extrude(amount=1.4, mode=bd.Mode.ADD)
        
        # 5. 4x M3 Countersunk Screw Holes in Corners
        for loc in SCREW_LOCATIONS:
            with bd.BuildSketch(bd.Plane.XY.offset(Z_BOTTOM_FLOOR - 0.5)) as s_screw:
                with bd.Locations([loc]):
                    bd.Circle(M3_SCREW_HOLE_DIA / 2)
            bd.extrude(amount=Z_PARTING_LINE - Z_BOTTOM_FLOOR + 3.0, mode=bd.Mode.SUBTRACT)
            
            with bd.BuildSketch(bd.Plane.XY.offset(Z_BOTTOM_FLOOR - 0.5)) as s_cbore:
                with bd.Locations([loc]):
                    bd.Circle(M3_HEAD_BORE_DIA / 2)
            bd.extrude(amount=M3_HEAD_BORE_DEPTH + 0.5, mode=bd.Mode.SUBTRACT)
            
        # 6. 4x Underside Rubber Feet Pockets (Ø10mm x 1.2mm deep)
        foot_x = 76.0
        foot_y = 45.0
        foot_locs = [(-foot_x, -foot_y), (foot_x, -foot_y), (-foot_x, foot_y), (foot_x, foot_y)]
        for loc in foot_locs:
            with bd.BuildSketch(bd.Plane.XY.offset(Z_BOTTOM_FLOOR - 0.1)) as s_foot:
                with bd.Locations([loc]):
                    bd.Circle(10.0 / 2)
            bd.extrude(amount=1.2, mode=bd.Mode.SUBTRACT)
            
        # 7. Underside Passive Cooling Slots
        grille_x_start = 45.0
        for i in range(5):
            gx = grille_x_start + i * 7.5
            with bd.BuildSketch(bd.Plane.XY.offset(Z_BOTTOM_FLOOR - 0.5)) as s_vent:
                with bd.Locations([(gx, 25.0)]):
                    bd.SlotOverall(width=28.0, height=2.4, rotation=90)
            bd.extrude(amount=Z_CAVITY_FLOOR - Z_BOTTOM_FLOOR + 1.0, mode=bd.Mode.SUBTRACT)
            
        # 8. Bottom Edge Fillet
        bottom_faces = [f for f in bottom.part.faces() if abs(f.center().Z - Z_BOTTOM_FLOOR) < 0.2]
        if bottom_faces:
            outer_bottom_edges = [e for e in bottom_faces[0].edges() if e.length > 50.0]
            try:
                bottom.part = bd.fillet(outer_bottom_edges, 1.2)
            except Exception as e:
                print(f"Note: Bottom edge fillet skipped: {e}")

    print(f"Bottom Shell complete. Volume: {bottom.part.volume:.1f} mm³")
    return bottom.part


# ---------------------------------------------------------------------------
# Part 2: Top Shell (Console Faceplate with Enlarged Slider Gaps)
# ---------------------------------------------------------------------------
def build_top_shell():
    print("Building Top Shell...")
    pocket_w = PCB_W + 2 * PCB_CLEARANCE_XY
    pocket_d = PCB_D + 2 * PCB_CLEARANCE_XY

    with bd.BuildPart() as top:
        # 1. Base solid block
        with bd.BuildSketch(bd.Plane.XY.offset(Z_PARTING_LINE)) as s_base:
            bd.RectangleRounded(CASE_W, CASE_D, CORNER_R)
        bd.extrude(amount=(Z_REAR_TOP + 4.0) - Z_PARTING_LINE)
        
        # 2. Slice top surface at 3.95° ergonomic incline
        slope = (Z_REAR_TOP - Z_FRONT_TOP) / CASE_D
        angle_rad = math.atan(slope)
        z_mid = (Z_FRONT_TOP + Z_REAR_TOP) / 2
        top_plane = bd.Plane(
            origin=(0, 0, z_mid),
            x_dir=(1, 0, 0),
            z_dir=(0, -math.sin(angle_rad), math.cos(angle_rad))
        )
        top.part = top.part.split(top_plane, bd.Keep.BOTTOM)
        
        # 3. Interlocking Groove (Rebate for Bottom Shell Lip)
        with bd.BuildSketch(bd.Plane.XY.offset(Z_PARTING_LINE - 0.1)) as s_groove:
            bd.RectangleRounded(CASE_W + 0.1, CASE_D + 0.1, CORNER_R)
            bd.RectangleRounded(CASE_W - 2.8, CASE_D - 2.8, max(0.5, CORNER_R - 1.4), mode=bd.Mode.SUBTRACT)
        bd.extrude(amount=1.6, mode=bd.Mode.SUBTRACT)

        # 4. Internal cavity for PCB upper components (resistors, switches, Pico)
        with bd.BuildSketch(bd.Plane.XY.offset(Z_PARTING_LINE - 0.1)) as s_upper_cav:
            with bd.Locations([(0, 28.5)]):
                bd.RectangleRounded(pocket_w - 2.0, 57.0, CORNER_R)
        bd.extrude(amount=7.0, mode=bd.Mode.SUBTRACT)

        # 5. Capacitive Touch Keyboard Playing Window with 45° Chamfered Bezel
        with bd.BuildSketch(bd.Plane.XY.offset(Z_PARTING_LINE - 0.2)) as s_keys_bot:
            with bd.Locations([(0, KEYS_CENTER_Y)]):
                bd.RectangleRounded(KEYS_W, KEYS_D, 2.0)
        with bd.BuildSketch(bd.Plane.XY.offset(Z_FRONT_TOP + 3.0)) as s_keys_top:
            with bd.Locations([(0, KEYS_CENTER_Y)]):
                bd.RectangleRounded(KEYS_W + 3.0, KEYS_D + 3.0, 3.5)
        bd.loft(sections=[s_keys_bot.sketch, s_keys_top.sketch], mode=bd.Mode.SUBTRACT)

        # 6. UNIFIED SWITCH BAR CUTOUT (Continuous bar for SW1, SW2, SW3)
        with bd.BuildSketch(bd.Plane.XY.offset(Z_PARTING_LINE - 0.5)) as s_bar_bot:
            with bd.Locations([SW_BAR_CENTER]):
                bd.RectangleRounded(SW_BAR_W_BOT, SW_BAR_H_BOT, 1.5)
        with bd.BuildSketch(bd.Plane.XY.offset(Z_FRONT_TOP + 4.5)) as s_bar_top:
            with bd.Locations([SW_BAR_CENTER]):
                bd.RectangleRounded(SW_BAR_W_TOP, SW_BAR_H_TOP, 2.0)
        bd.loft(sections=[s_bar_bot.sketch, s_bar_top.sketch], mode=bd.Mode.SUBTRACT)

        # 7. EC11 Rotary Encoder Cutout & Recessed Counterbore Well
        with bd.BuildSketch(bd.Plane.XY.offset(Z_PARTING_LINE - 1.0)) as s_enc:
            with bd.Locations([ENC_POS]):
                bd.Circle(8.5 / 2)
        bd.extrude(amount=20.0, mode=bd.Mode.SUBTRACT)
        
        with bd.BuildSketch(bd.Plane.XY.offset(Z_REAR_TOP - 4.5)) as s_enc_well:
            with bd.Locations([ENC_POS]):
                bd.Circle(20.0 / 2)
        bd.extrude(amount=10.0, mode=bd.Mode.SUBTRACT)

        # 8. ENLARGED SLIDER GAPS (Bourns PTA1543 Slide Potentiometer Cutouts)
        # Generously sized openings with smooth 45° chamfer for full 15mm stroke,
        # fader cap clearance, and comfortable finger operation.
        for rv in [RV1_POS, RV2_POS]:
            with bd.BuildSketch(bd.Plane.XY.offset(Z_PARTING_LINE - 0.5)) as s_slot_bot:
                with bd.Locations([rv]):
                    bd.RectangleRounded(SLIDER_W_BOT, SLIDER_L_BOT, 2.0)
            with bd.BuildSketch(bd.Plane.XY.offset(Z_REAR_TOP + 2.0)) as s_slot_top:
                with bd.Locations([rv]):
                    bd.RectangleRounded(SLIDER_W_TOP, SLIDER_L_TOP, 2.5)
            bd.loft(sections=[s_slot_bot.sketch, s_slot_top.sketch], mode=bd.Mode.SUBTRACT)

        # 9. Raspberry Pi Pico Showcase Window with Chamfered Frame
        with bd.BuildSketch(bd.Plane.XY.offset(Z_PARTING_LINE - 0.5)) as s_pico_bot:
            with bd.Locations([PICO_POS]):
                bd.RectangleRounded(22.5, 48.0, 2.0)
        with bd.BuildSketch(bd.Plane.XY.offset(Z_REAR_TOP + 2.0)) as s_pico_top:
            with bd.Locations([PICO_POS]):
                bd.RectangleRounded(25.5, 51.0, 3.2)
        bd.loft(sections=[s_pico_bot.sketch, s_pico_top.sketch], mode=bd.Mode.SUBTRACT)

        # 10. REAR USB Port Tunnel on REAR face (Y = +CASE_D / 2)
        rear_usb_plane = bd.Plane(origin=(0, CASE_D / 2 + 1.0, 0), x_dir=(1, 0, 0), y_dir=(0, 0, 1))
        with bd.BuildSketch(rear_usb_plane) as s_usb:
            with bd.Locations([(USB_X, 5.5)]):
                bd.RectangleRounded(14.5, 8.0, 2.2)
        bd.extrude(amount=14.0, mode=bd.Mode.SUBTRACT)

        # 11. 4x M3 Brass Heat-Set Insert Bosses in Corners (Blind from top)
        for loc in SCREW_LOCATIONS:
            with bd.BuildSketch(bd.Plane.XY.offset(Z_PARTING_LINE)) as s_boss:
                with bd.Locations([loc]):
                    bd.Circle(M3_BOSS_DIA / 2)
            bd.extrude(amount=5.5, mode=bd.Mode.ADD)
            
            with bd.BuildSketch(bd.Plane.XY.offset(Z_PARTING_LINE - 0.2)) as s_insert:
                with bd.Locations([loc]):
                    bd.Circle(M3_INSERT_HOLE_DIA / 2)
            bd.extrude(amount=M3_INSERT_DEPTH + 0.2, mode=bd.Mode.SUBTRACT)

        # 12. Internal Perimeter PCB Clamping Ribs
        with bd.BuildSketch(bd.Plane.XY.offset(Z_PARTING_LINE)) as s_clamp_l:
            with bd.Locations([(-PCB_W / 2 + 0.5, 0)]):
                bd.Rectangle(1.8, 35.0)
        bd.extrude(amount=2.5, mode=bd.Mode.ADD)

        with bd.BuildSketch(bd.Plane.XY.offset(Z_PARTING_LINE)) as s_clamp_r:
            with bd.Locations([(PCB_W / 2 - 0.5, -25.0)]):
                bd.Rectangle(1.8, 30.0)
        bd.extrude(amount=2.5, mode=bd.Mode.ADD)

        # 13. Debossed "MIDI+" Logo on Top Faceplate
        with bd.BuildSketch(bd.Plane.XY.offset(Z_REAR_TOP - 4.0)) as s_logo:
            with bd.Locations([(-72.0, 48.0)]):
                bd.Text("MIDI+", font_size=6.5, font_style=bd.FontStyle.BOLD)
        bd.extrude(amount=5.0, mode=bd.Mode.SUBTRACT)

    print(f"Top Shell complete. Volume: {top.part.volume:.1f} mm³")
    return top.part


# ---------------------------------------------------------------------------
# Main Execution & STEP Export
# ---------------------------------------------------------------------------
def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))

    bottom = build_bottom_shell()
    top = build_top_shell()

    # 1. Export Individual Shells
    top_path = os.path.join(out_dir, "midi_plus_top_shell.step")
    bot_path = os.path.join(out_dir, "midi_plus_bottom_shell.step")
    bd.export_step(top, top_path)
    bd.export_step(bottom, bot_path)
    print(f"  ✓ Exported: {top_path}")
    print(f"  ✓ Exported: {bot_path}")

    # 2. Export Assembled Case (Top Shell + Bottom Shell)
    case_compound = bd.Compound([bottom, top])
    case_path = os.path.join(out_dir, "midi_plus_case.step")
    bd.export_step(case_compound, case_path)
    print(f"  ✓ Exported Case STEP: {case_path}")

    # 3. Export Assembled Case with KiCad PCB inside
    pcb_step_path = os.path.join(out_dir, "..", "KiCad", "pcb.step")
    if os.path.exists(pcb_step_path):
        print("  Importing KiCad PCB model...")
        try:
            pcb = bd.import_step(pcb_step_path)
            pcb_centered = pcb.translate((-132.875, 106.625, 0))
            case_assembled = bd.Compound([bottom, top, pcb_centered])
            assembled_path = os.path.join(out_dir, "midi_plus_case_assembled.step")
            bd.export_step(case_assembled, assembled_path)
            print(f"  ✓ Exported Assembled Case + PCB STEP: {assembled_path}")
        except Exception as e:
            print(f"  Note on PCB merge: {e}")
            assembled_path = os.path.join(out_dir, "midi_plus_case_assembled.step")
            bd.export_step(case_compound, assembled_path)
    else:
        assembled_path = os.path.join(out_dir, "midi_plus_case_assembled.step")
        bd.export_step(case_compound, assembled_path)

    print("\n✅ Case and assembled STEP files successfully generated with enlarged slider gaps!")


if __name__ == "__main__":
    main()
