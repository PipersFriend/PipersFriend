# The Piper's Friend

A desktop **bagpipe sheet-music editor and player** for Great Highland Bagpipe
(GHB) and Practice Chanter tunes. Write tunes on a two-stave, Letter-sized page,
hear them back with real instrument samples, and export or print the result.

Built with **Python + Tkinter** (UI) and **Pillow** (rendering). Audio uses the
Windows `winsound` module.

---

## Features

- **Score editor** on a US-Letter-proportioned page with title / composer /
  tune-type header and a page number.
- **Two independent staves** with a G-clef (spiral on the G line) and a
  full-height time signature centred on the B line.
- **Notes** from whole down to hemidemisemiquaver, with **dots** and **ties**
  (ties force matching pitch).
- **Bagpipe beaming** — sub-crotchet notes are barred by beat with correct beam
  counts and partial beams; no loose flags.
- **Gracenotes & embellishments** — single gracenotes plus **Doubling**,
  **Throw on D**, **Birl**, and **High G Birl**, with placement rules
  (birls only on Low A, throw-on-D only on D, doublings tied to the note they
  attach to). Barred gracenotes always beam at the top of the stave.
- **Bar styles** — set each bar's start/end to Normal, Repeat, or Part
  (Start/End) barlines.
- **Translucent hover preview** of the note/gracenote about to be placed.
- **Zoom & scroll**, draggable barlines (independent per stave), drag-to-resize
  with a lightweight preview.
- **Playback** — gapless, continuous audio (notes ring until the next note;
  gracenotes play as 1/64 with no cooldown), with the playing note highlighted.
  Choose **Bagpipe** or **Practice Chanter**.
- **Save/Open** `.pipe` files, **Export to PDF**, and **Print**.
- **Global settings** (theme, app font, volume, defaults, …) persisted to
  `settings.json`, plus per-tune settings.

---

## Requirements

- **Windows** (audio uses `winsound`; header text uses Windows fonts).
- **Python 3.8+** (uses the walrus operator; developed on 3.13).
- **Pillow**:
  ```
  pip install pillow
  ```
  Tkinter ships with the standard Python installer.

---

## Running

From the project folder:

```
python main.py
```

`main.py` is a thin launcher; all the code lives in the `src/` package.

---

## Project structure

```
Pipers Friend/
├── main.py                 # launcher  ->  from src.app import main
├── README.md
├── src/
│   ├── __init__.py
│   ├── constants.py        # constants, settings load/save, themes, fonts, maps
│   ├── model.py            # BagpipeScore: the document + .pipe (de)serialization
│   ├── dialogs.py          # UnifiedSetupDialog (new-tune wizard)
│   └── app.py              # PipersFriendApp: UI, rendering, audio, events
├── Assets/
│   ├── notes/              # whole.png … gracenote.png, tie.png
│   ├── bar/                # clef.png, start/<normal|repeat|start>.png,
│   │                       #           end/<normal|repeat|end>.png
│   ├── time_sigs/          # 4_4.png, 6_8.png, common.png, cut.png, …
│   ├── audio/
│   │   ├── GHB/            # higha, highg, f, e, d, c, b, lowa, lowg (.wav/.mp3)
│   │   └── chanter/        # same set for the practice chanter
│   └── menu/settings.png
└── user_data/
    ├── user_scores/        # saved *.pipe tunes
    └── user_settings/settings.json
```

---

## Using the app

### Dashboard
- **New Score Layout** — wizard for name, composer, type, and time signature
  (pre-filled from your defaults).
- **Open Existing Score** — file picker, or pick from the **My Scores** list.
- **⚙ Settings** (top-right) — global app settings.

### Editor ribbon
| Tab | What it does |
|-----|--------------|
| **File** | New / Open / Save / Export PDF / Export PIPE / Print / Clear / Exit |
| **Notes** | Pick a duration; **Dot** / **Tie** the selected note |
| **Gracenotes** | Single gracenote and embellishments |
| **Bar** | Select a bar, then set its **Start** and **End** style |
| **Playback** | Instrument + Play (all / from note / from bar) / Stop |
| **Settings** | Per-tune: name, composer, type, time sig, BPM, gaps, score font |

### On the page
- **Hover** the stave (Notes/Gracenotes tab) to preview where a note lands.
- **Click empty stave** to place a note *and* select that bar.
- **Click a note** to select it and return to the **Notes** tab.
- **Double-click** the title / tune type / composer to edit its text and font
  style.
- **Drag a barline** to resize a bar (bars are independent per stave).
- **Delete / Backspace** removes the selected note (and its gracenotes).
- **Zoom**: 🔍 / Fit buttons, **Ctrl + mouse-wheel**, or **Ctrl +/-**;
  mouse-wheel scrolls.

---

## File formats

### `.pipe` (score) — JSON, format version `2.0.0`
```json
{
  "format_version": "2.0.0",
  "metadata": {
    "title": "...", "composer": "...", "tune_type": "...",
    "time_signature": "4/4", "tempo": 90,
    "gap_between_staves": 100, "gap_after_gracenotes": 14,
    "selected_font": "Sans Serif",
    "header_style": { "title": {...}, "tune_type": {...}, "composer": {...} }
  },
  "bar_lines":  { "1": [470, 860, 1250], "2": [...] },
  "bar_styles": { "1": [ {"start":"Normal","end":"Normal"}, ... ], "2": [...] },
  "score_timeline": [
    { "id": "a1b2c3d4", "pitch": "D", "duration": 0.5, "dur_type": "quarter",
      "staff": 1, "bar_index": 0, "raw_x": 320, "target_normal_id": null,
      "seq": 1 }
  ]
}
```
Pitches: `High A, High G, F, E, D, C, B, Low A, Low G`. Gracenotes carry a
`target_normal_id` linking them to the melody note they ornament. Legacy files
with a flat `bar_lines`/`bar_styles` list are auto-upgraded to per-stave form.

### `settings.json` (global)
Theme, app font/size, accent colour, playback volume, audio start-second,
default instrument/tempo/time-signature/type/composer, page border / page
number toggles, and confirm-before-clear.

---

## Audio notes

- Per-pitch `.wav` samples are **trimmed** by `audio_start_sec` (default 3s, to
  skip the reedy warm-up) and **amplified** toward the `volume` setting
  (default 200%).
- On playback the whole selection is concatenated into **one continuous WAV**
  and played via `SND_FILENAME` — so notes are gapless and gracenotes flow
  straight into the next note.

---

## Known limitations / TODO

- **Windows only** (winsound + Windows font files).
- **BWW export** is a placeholder.
- The full-page render buffer is large; very dense editing/playback can feel
  heavy on slower machines.
- At very slow tempos a long note can exceed its sample length, in which case
  the sample is tiled to fill.

---
