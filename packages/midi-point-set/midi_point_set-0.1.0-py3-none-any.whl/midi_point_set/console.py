"""CLI utilities."""
import argparse
from pathlib import Path
import json
import pretty_midi
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show
from bokeh.models import HoverTool


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Convert MIDI files to point set encoding.',
    )
    parser.add_argument(
        "--input-midi",
        help="MIDI file that will be converted.",
        required=True,
        type=Path,
    )
    parser.add_argument(
        "--output-json",
        help="Output JSON file path with the point set.",
        required=False,
        type=Path,
    )
    parser.add_argument(
        "--output-plot",
        help="Output plot file path with the point set.",
        required=False,
        type=Path,
    )
    parser.add_argument(
        "--show-plot",
        help="Display an interactive plot of the point set.",
        action='store_const',
        const=True,
        default=False,
    )
    args = parser.parse_args()

    # Extract point set from MIDI
    midi_data = pretty_midi.PrettyMIDI(str(args.input_midi))
    point_set = list()
    for instrument in midi_data.instruments:
        if instrument.is_drum:
            raise ValueError("Drum instruments not supported!")
        for note in instrument.notes:
            point_set.append((note.start, note.pitch))

    # Serialize to plot
    if args.output_plot is not None:
        fig, ax = plt.subplots()
        x = [x for x, _ in point_set]
        y = [y for _, y in point_set]
        ax.scatter(x, y, s=0.1)
        fig.savefig(args.output_plot)
        print(f"Wrote {args.output_plot}")

    if args.output_json is not None:
        with open(args.output_json, "wt") as fp:
            json.dump(point_set, fp, indent=2)
            print(f"Wrote {args.output_json}")

    if args.show_plot:
        hover = HoverTool(tooltips=[
            ("(x,y)", "(@x, @y)"),
        ])
        p = figure(tools=['pan, ywheel_zoom, xwheel_zoom, lasso_select', hover])
        x = [x for x, _ in point_set]
        y = [y for _, y in point_set]
        p.circle(x, y)
        show(p)
