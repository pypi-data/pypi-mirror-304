import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
import re
import subprocess
import csv
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore", category=UserWarning, message=".*tight_layout.*")


# Function to parse eggnog-mapper output and prepare for KEGG-Decoder
def parse_emapper(input_file, temp_folder):
    print("Parsing eggnog-mapper output...")

    # Read the input file with progress bar
    with tqdm(total=1, desc="Reading eggnog-mapper file") as pbar:
        df_filtered = pd.read_csv(input_file, sep="\t", skiprows=4)
        pbar.update(1)

    # Filter the 'KEGG_ko' column
    df_kegg_ko = df_filtered[["KEGG_ko"]]
    df_kegg_ko = df_kegg_ko[df_kegg_ko["KEGG_ko"] != "-"]

    # Format 'KEGG_ko' column for KEGG-Decoder
    with tqdm(total=1, desc="Formatting KEGG_ko column") as pbar:
        df_kegg_ko["KEGG_ko"] = df_kegg_ko["KEGG_ko"].str.replace(
            r"ko:(K\d+)", r"SAMPLE \1", regex=True
        )
        df_kegg_ko["KEGG_ko"] = df_kegg_ko["KEGG_ko"].str.replace(",", "\n")
        pbar.update(1)

    # Save the parsed file
    parsed_file = os.path.join(temp_folder, "parsed.txt")
    with tqdm(total=1, desc="Saving parsed file") as pbar:
        df_kegg_ko.to_csv(
            parsed_file,
            sep="\t",
            index=False,
            header=False,
            quoting=csv.QUOTE_MINIMAL,
            escapechar="\\",
        )
        pbar.update(1)

    # Remove all quotation marks from the parsed file
    parsed_filtered_file = os.path.join(temp_folder, "parsed_filtered.txt")
    with open(parsed_file, "r") as file:
        content = file.read()

    content = content.replace('"', "")
    with open(parsed_filtered_file, "w") as file:
        file.write(content)

    return parsed_filtered_file


# Function to run KEGG-Decoder and process the output
def run_kegg_decoder(input_file, temp_folder, sample_name):
    print("Running KEGG-Decoder...")

    output_file = os.path.join(temp_folder, "output.list")

    # Run KEGG-Decoder via subprocess with progress bar
    with tqdm(total=1, desc="Executing KEGG-Decoder") as pbar:
        subprocess.run(
            ["KEGG-decoder", "-i", input_file, "-o", output_file, "-v", "static"]
        )
        pbar.update(1)

    with open(output_file, "r") as file:
        content = file.read()

    content = content.replace("SAMPLE", f"{sample_name}")

    with open(output_file, "w") as file:
        file.write(content)

    return output_file


# Function to generate the heatmap with progress
def generate_heatmap(kegg_decoder_file, output_folder, dpi, color, sample_name):
    print("Generating heatmap...")

    # Read the KEGG-Decoder output with progress bar
    with open(kegg_decoder_file, "r") as file:
        lines = file.readlines()

    # Process data for heatmap with progress bar
    with tqdm(total=3, desc="Preparing heatmap data") as pbar:
        header = lines[0].strip().split("\t")
        values = lines[1].strip().split("\t")
        data = {"Function": header[1:], sample_name: [float(v) for v in values[1:]]}
        df = pd.DataFrame(data)
        pbar.update(1)

        # Split into three parts for separate heatmaps
        df1, df2, df3 = np.array_split(df, 3)
        pbar.update(2)

    # Plot heatmaps with progress bar for each part
    fig, axes = plt.subplots(1, 3, figsize=(20, 20))
    cbar_ax = fig.add_axes([0.92, 0.4, 0.02, 0.2])  # Colorbar axis on the right

    with tqdm(total=3, desc="Creating heatmap parts") as pbar:
        sns.heatmap(
            df1.pivot_table(values=sample_name, index="Function", fill_value=0),
            cmap=f"{color}",
            annot=True,
            linewidths=0.5,
            ax=axes[0],
            cbar=False,
        )
        axes[0].set_title("Part 1")
        pbar.update(1)

        sns.heatmap(
            df2.pivot_table(values=sample_name, index="Function", fill_value=0),
            cmap=f"{color}",
            annot=True,
            linewidths=0.5,
            ax=axes[1],
            cbar=False,
        )
        axes[1].set_title("Part 2")
        pbar.update(1)

        sns.heatmap(
            df3.pivot_table(values=sample_name, index="Function", fill_value=0),
            cmap=f"{color}",
            annot=True,
            linewidths=0.5,
            ax=axes[2],
            cbar_ax=cbar_ax,
            cbar_kws={"label": "Pathway completeness"},
        )
        axes[2].set_title("Part 3")
        pbar.update(1)

    plt.tight_layout(rect=[0, 0, 0.9, 1])
    output_file = os.path.join(output_folder, "heatmap_figure.png")
    plt.savefig(output_file, dpi=dpi, bbox_inches="tight")
    plt.show()


# Main function to run the tool with a progress bar
def main():
    print("KEGGaNOG v. 0.2.1 by Ilia V. Popov")
    parser = argparse.ArgumentParser(
        description="KEGGaNOG: Link eggnog-mapper and KEGG-Decoder for pathway visualization."
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Path to eggnog-mapper output file"
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Output folder to save results"
    )
    parser.add_argument(
        "-dpi",
        "--dpi",
        type=int,
        default=300,
        help="DPI for the output image (default: 300)",
    )
    parser.add_argument(
        "-c", "--color", "--colour", default="Blues", help="Cmap for seaborn heatmap"
    )
    parser.add_argument(
        "-s", "--sample", default="Sample", help="Sample name for labeling"
    )
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    temp_folder = os.path.join(args.output, "temp")
    os.makedirs(temp_folder, exist_ok=True)

    # Parsing and Running KEGG-Decoder with progress
    parsed_file = parse_emapper(args.input, temp_folder)
    kegg_output = run_kegg_decoder(parsed_file, temp_folder, args.sample)

    # Generating the heatmap
    generate_heatmap(kegg_output, args.output, args.dpi, args.color, args.sample)


if __name__ == "__main__":
    main()
