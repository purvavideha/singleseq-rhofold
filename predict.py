import os
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
# Paths


# Function to split input FASTA file into smaller FASTA files
def split_fasta(input_fasta, output_dir):
    files = []
    with open(input_fasta, "r") as file:
        lines = file.readlines()

    current_index = 0
    for i in range(0, len(lines), 2):
        if i + 1 >= len(lines):  # Ensure there are both a header and a sequence
            break
        header = lines[i].strip()
        sequence = lines[i + 1].strip()
        output_file = os.path.join(output_dir, f"split_{current_index}.fasta")
        with open(output_file, "w") as out_file:
            out_file.write(f"{header}\n{sequence}\n")
        files.append(output_file)
        current_index += 1
    return files

# Function to run the inference command
def run_inference(fasta_file,inference_script,output_dir,device):
    # Each output will go directly into the main output_dir
    command = (
        f"python {inference_script} "
        f"--input_fas \"{fasta_file}\" "
        f"--output_dir \"{output_dir}\" "
        f"--device \"{device}\" "
        f"--single_seq_pred 'True'"
    )
    os.system(command)
# Main function
if __name__ == "__main__":
    input_fasta = "/home/jyjiang/RhoFold/gRNAde_test_new.fasta"  # Replace this with your input FASTA file
    output_dir = "/home/jyjiang/RhoFold/pdbs"   # Directory to store split FASTA files and results
    inference_script = "inference.py"    # Path to your inference script
    device = "cuda:1"                       # Device to run inference on (e.g., "cpu" or "cuda:0")

# Ensure output directory exists
    split_fasta_dir = os.path.join(output_dir, "split_fasta")
    Path(split_fasta_dir).mkdir(parents=True, exist_ok=True)
    # Step 1: Split the input FASTA file
    split_files = split_fasta(input_fasta, split_fasta_dir)
    print(f"Split input FASTA into {len(split_files)} files in {split_fasta_dir}")

    # Step 2: Run inference in parallel
    for file in split_files[:10]:
        run_inference(file,inference_script,output_dir,device)

    print("Inference completed for all files!")