import pandas as pd
import matplotlib.pyplot as plt
import pickle
import glob
import os

# Load paper results
with open('plot_data/ogbench-agg.pkl', 'rb') as f:
    paper_data = pickle.load(f)

# Use the correct task name from the pickle file
task = 'cube-triple'
method = 'QC'
paper_results = paper_data[(task, method)]

print(f"Paper data loaded for {task} - {method}")
print(f"Paper steps: {paper_results['steps']}")
print(f"Paper means: {paper_results['means']}")

# Find your CSV files
base_path = 'exp/qc/reproduce/cube-triple-play-singletask-task2-v0/'
csv_files = glob.glob(os.path.join(base_path, '*/eval.csv'))

if not csv_files:
    print(f"\nNo CSV files found in {base_path}")
    print("Please check your experiment directory.")
    exit()

print(f"\nFound {len(csv_files)} CSV file(s):")
for f in csv_files:
    print(f"  {f}")

# Load the most recent (or you can specify which one)
reproduction_csv = csv_files[0]
ablation_csv = csv_files[1] if len(csv_files) > 1 else None

print(f"\nUsing for reproduction: {reproduction_csv}")
if ablation_csv:
    print(f"Using for ablation: {ablation_csv}")

# Load your results
reproduction_data = pd.read_csv(reproduction_csv)

# ========== FIGURE 1 LEFT: Reproduction vs Original ==========
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Left plot: Reproduction vs Original
ax = axes[0]
paper_steps = paper_results['steps'] * 1e6  # Convert millions to actual steps

ax.plot(paper_steps, paper_results['means'], 
        label='Original Paper (QC)', marker='o', linewidth=2, markersize=8)
ax.fill_between(paper_steps, 
                paper_results['ci_lows'], 
                paper_results['ci_highs'], 
                alpha=0.2)

ax.plot(reproduction_data['step'], reproduction_data['episode.normalized_return'],
        label='My Reproduction', marker='s', linewidth=2, markersize=6)

ax.set_xlabel('Training Steps', fontsize=12)
ax.set_ylabel('Normalized Return', fontsize=12)
ax.set_title('Left: Reproduction vs. Original Baseline', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

# ========== FIGURE 1 RIGHT: Ablation Study ==========
ax = axes[1]

# Plot baseline (reproduction)
ax.plot(reproduction_data['step'], reproduction_data['episode.normalized_return'],
        label='Baseline (QC)', marker='o', linewidth=2, markersize=6)

# Plot ablation if available
if ablation_csv:
    ablation_data = pd.read_csv(ablation_csv)
    ax.plot(ablation_data['step'], ablation_data['episode.normalized_return'],
            label='Ablation (modified params)', marker='^', linewidth=2, markersize=6)
else:
    print("\nWarning: Only one CSV found. Please specify your ablation study CSV.")
    ax.text(0.5, 0.5, 'Ablation study data needed', 
            transform=ax.transAxes, ha='center', va='center', fontsize=14)

ax.set_xlabel('Training Steps', fontsize=12)
ax.set_ylabel('Normalized Return', fontsize=12)
ax.set_title('Right: Ablation Study Results', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('figure1_comparison.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: figure1_comparison.png")

# Also save individual plots
plt.figure(figsize=(10, 6))
plt.plot(paper_steps, paper_results['means'], 
        label='Original Paper (QC)', marker='o', linewidth=2, markersize=8)
plt.fill_between(paper_steps, 
                paper_results['ci_lows'], 
                paper_results['ci_highs'], 
                alpha=0.2)
plt.plot(reproduction_data['step'], reproduction_data['episode.normalized_return'],
        label='My Reproduction', marker='s', linewidth=2, markersize=6)
plt.xlabel('Training Steps', fontsize=12)
plt.ylabel('Normalized Return', fontsize=12)
plt.title('Reproduction vs. Original Baseline', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('reproduction_vs_original.png', dpi=300, bbox_inches='tight')
print("✓ Saved: reproduction_vs_original.png")

print("\nDone! Check the PNG files for your assignment plots.")