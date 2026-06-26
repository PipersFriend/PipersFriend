from .constants import *


class BagpipeScore:
    def __init__(self, title="Untitled Tune", time_signature="4/4", tempo=120, tune_type="March", composer="Unknown"):
        self.title = title
        self.time_signature = time_signature
        self.tempo = tempo
        self.tune_type = tune_type
        self.composer = composer
        self.gap_between_staves = 100   # default gap reduced 50% (was 200)
        self.gap_after_gracenotes = 14
        self.selected_font = "Sans Serif"
        self.header_style = {k: dict(v) for k, v in DEFAULT_HEADER_STYLE.items()}
        self.nodes = []
        # Per-staff bar start/end styles: "Normal" | "Repeat" | "Start"/"End".
        self.bar_styles = {s: [{"start": "Normal", "end": "Normal"} for _ in range(4)]
                           for s in (1, 2)}
        # Bar lines are independent per staff so resizing a bar on one stave
        # does not move the bars on the other stave.
        self.bar_lines = {1: [470, 860, 1250], 2: [470, 860, 1250]}

    def to_pipe_format(self):
        score_data = {
            "format_version": "2.0.0",
            "metadata": {
                "title": self.title, 
                "time_signature": self.time_signature, 
                "tempo": self.tempo,
                "tune_type": self.tune_type,
                "composer": self.composer,
                "gap_between_staves": self.gap_between_staves,
                "gap_after_gracenotes": self.gap_after_gracenotes,
                "selected_font": self.selected_font,
                "header_style": self.header_style
            },
            "bar_lines": self.bar_lines,
            "bar_styles": self.bar_styles,
            "score_timeline": self.nodes
        }
        return json.dumps(score_data, indent=2)

    def load_from_pipe_format(self, pipe_string):
        data = json.loads(pipe_string)
        meta = data.get("metadata", {})
        self.title = meta.get("title", "Untitled Tune")
        self.time_signature = meta.get("time_signature", "4/4")
        self.tempo = meta.get("tempo", 120)
        self.tune_type = meta.get("tune_type", "March")
        self.composer = meta.get("composer", "Unknown")
        self.gap_between_staves = meta.get("gap_between_staves", 100)
        self.gap_after_gracenotes = meta.get("gap_after_gracenotes", 14)
        self.selected_font = meta.get("selected_font", "Sans Serif")
        self.header_style = {k: dict(v) for k, v in DEFAULT_HEADER_STYLE.items()}
        for k, v in (meta.get("header_style") or {}).items():
            if k in self.header_style and isinstance(v, dict):
                self.header_style[k].update(v)
        bl = data.get("bar_lines", [470, 860, 1250])
        if isinstance(bl, dict):
            self.bar_lines = {int(k): list(v) for k, v in bl.items()}
        else:  # legacy flat list -> shared across both staves
            self.bar_lines = {1: list(bl), 2: list(bl)}
        for s in (1, 2):
            self.bar_lines.setdefault(s, [470, 860, 1250])
        bs = data.get("bar_styles")
        self.bar_styles = {s: [{"start": "Normal", "end": "Normal"} for _ in range(4)]
                           for s in (1, 2)}
        if isinstance(bs, dict):
            for k, v in bs.items():
                self.bar_styles[int(k)] = v
        elif isinstance(bs, list):  # legacy flat -> both staves
            self.bar_styles = {1: bs, 2: [dict(x) for x in bs]}
        self.nodes = data.get("score_timeline", [])


