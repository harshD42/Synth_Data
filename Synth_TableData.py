import os
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv

def recursive_rotation(ax, angle):
    if angle <= 360:
        ax.view_init(elev=20, azim=angle)
        #plt.pause(0.01)  # Pause for a short duration to see the animation

def draw_table_3d(label, keypoints, save_path, figsize=(10, 10)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')

    # Disable automatic scaling
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(False)
    ax.set_axis_off()
    #ax.set_proj_type('ortho')

    #View Rotation
    rotation_angle=round(random.uniform(0, 360),2)
    recursive_rotation(ax, rotation_angle)
    
    # Define table dimensions
    table_width, table_length, table_height = keypoints['TableDimensions']

    # Calculate leg length based on the maximum of table_width and table_length
    #leg_length = max(table_width, table_length)

    # Set the limits of the plot
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_zlim(0, 10)

    # Draw table top
    ax.plot([0, table_length], [0, 0], [table_height, table_height], color='red')
    ax.plot([0, 0], [0, table_width], [table_height, table_height], color='red')
    ax.plot([table_length, table_length], [0, table_width], [table_height, table_height], color='red')
    ax.plot([0, table_length], [table_width, table_width], [table_height, table_height], color='red')

    # Draw table legs
    ax.plot([0, 0], [0, 0], [0, table_height], color='green')
    ax.plot([0, 0], [table_width, table_width], [0, table_height], color='green')
    ax.plot([table_length, table_length], [0, 0], [0, table_height], color='green')
    ax.plot([table_length, table_length], [table_width, table_width], [0, table_height], color='green')

    # Draw keypoints
    for keypoint, coord in keypoints.items():
        if keypoint != 'TableDimensions':
            ax.text(coord[0], coord[1], coord[2], keypoint, fontsize=8, ha='center', va='top')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Save the plot with label
    plt.title(f'{label}  (Angle = {rotation_angle}°)')
    plt.savefig(save_path)

    # Save the keypoints in a CSV file
    with open('keypoints.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        row = [label] + [coord for coord in keypoints.values()]
        writer.writerow(row)

    plt.close()

# Create training_images folder if it doesn't exist
if not os.path.exists('training_images'):
    os.makedirs('training_images')

# Clear existing keypoints.csv file
with open('keypoints.csv', 'w') as csvfile:
    pass

for i in range(0, 500):
    label = f'Table_{i:04d}'
    table_width = round(random.uniform(6, 8),2)
    table_length = round(random.uniform(6, 10),2)
    table_height = round(random.uniform(5, 6),2)

    keypoints = {
        'TableDimensions': (table_width, table_length, table_height),
        'Edge1': (0, 0, table_height),
        'Edge2': (0, table_width, table_height),
        'Edge3': (table_length, 0, table_height),
        'Edge4': (table_length, table_width, table_height),
        'Leg1': (0, 0, 0),
        'Leg2': (0, table_width, 0),
        'Leg3': (table_length, 0, 0),
        'Leg4': (table_length, table_width, 0)
    }
    save_path = f'training_images/table_{i:05d}.png'
    draw_table_3d(label, keypoints, save_path)
