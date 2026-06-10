import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
df = pd.read_csv('royalcsv/Untitled form.csv')

# Clean the data - convert rating columns to numeric
rating_columns = ['Overall Satisfaction', 'Cleanliness Quality', 'Staff Behavior', 'Value for Money']
for col in rating_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove rows with invalid data
df = df.dropna(subset=rating_columns)

# Create a comprehensive visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Customer Satisfaction Survey Analysis', fontsize=16, fontweight='bold')

# 1. Average Ratings Comparison (Top Left)
avg_ratings = df[rating_columns].mean()
ax1 = axes[0, 0]
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
bars = ax1.bar(range(len(avg_ratings)), avg_ratings.values, color=colors, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Average Rating', fontweight='bold')
ax1.set_title('Average Service Ratings')
ax1.set_xticks(range(len(avg_ratings)))
ax1.set_xticklabels(['Overall\nSatisfaction', 'Cleanliness\nQuality', 'Staff\nBehavior', 'Value for\nMoney'], fontsize=9)
ax1.set_ylim(0, 5)
ax1.grid(axis='y', alpha=0.3)
# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}', ha='center', va='bottom', fontweight='bold')

# 2. Overall Satisfaction Distribution (Top Right)
ax2 = axes[0, 1]
satisfaction_counts = df['Overall Satisfaction'].value_counts().sort_index()
colors_pie = ['#FFB6B6', '#FFD700', '#90EE90', '#87CEEB']
wedges, texts, autotexts = ax2.pie(satisfaction_counts.values, labels=[f'Rating {int(x)}' for x in satisfaction_counts.index],
                                     autopct='%1.0f%%', colors=colors_pie, startangle=90, textprops={'fontweight': 'bold'})
ax2.set_title('Overall Satisfaction Distribution')

# 3. Service Completion Status (Bottom Left)
ax3 = axes[1, 0]
completion = df['Was the service completed on time?'].value_counts()
bars = ax3.barh(completion.index, completion.values, color=['#90EE90', '#FFB6B6'], edgecolor='black', linewidth=1.5)
ax3.set_xlabel('Number of Responses', fontweight='bold')
ax3.set_title('Service Completion On Time')
ax3.grid(axis='x', alpha=0.3)
# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax3.text(width, bar.get_y() + bar.get_height()/2.,
            f' {int(width)}', ha='left', va='center', fontweight='bold')

# 4. Rating Distribution Heatmap (Bottom Right)
ax4 = axes[1, 1]
rating_data = df[rating_columns].apply(lambda x: x.value_counts()).fillna(0).astype(int)
im = ax4.imshow(rating_data.T, cmap='YlGn', aspect='auto')
ax4.set_xticks(range(len(rating_columns)))
ax4.set_xticklabels(rating_columns, rotation=45, ha='right', fontsize=9)
ax4.set_yticks(range(1, 6))
ax4.set_yticklabels(['Rating 1', 'Rating 2', 'Rating 3', 'Rating 4', 'Rating 5'])
ax4.set_title('Rating Frequency Heatmap')
# Add text annotations
for i in range(len(rating_columns)):
    for j in range(1, 6):
        if j in rating_data.index:
            text = ax4.text(i, j-1, int(rating_data.loc[j, rating_columns[i]]),
                          ha="center", va="center", color="black", fontweight='bold')

plt.colorbar(im, ax=ax4, label='Count')
plt.tight_layout()
plt.savefig('customer_satisfaction_analysis.png', dpi=300, bbox_inches='tight')
print("Chart saved as 'customer_satisfaction_analysis.png'")
plt.show()

# Print summary statistics
print("\n=== SUMMARY STATISTICS ===")
print(f"\nTotal Responses: {len(df)}")
print("\nAverage Ratings:")
print(avg_ratings.round(2))
print(f"\nService Completion Rate: {(completion.get('Yes', 0) / len(df) * 100):.1f}%")
