
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math
import random

def plot_parliament(total_seats, features, seats, slices=50, additional_rows=5, feature_colors=None):
    # Validate inputs
    if len(features) != len(seats):
        raise ValueError("Number of features and seats must match.")
    
    # Renkleri belirleme ve sabitleme
    if feature_colors is None:
        # Eğer renk haritası sağlanmamışsa rastgele değil, sabit bir renk sıralaması kullan
        colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'cyan', 'magenta', 'lime', 'pink']
        if len(features) > len(colors):
            import matplotlib.colors as mcolors
            all_colors = list(mcolors.CSS4_COLORS.values())
            random.shuffle(all_colors)
            colors += all_colors[:len(features) - len(colors)]
        feature_colors = {features[i]: colors[i % len(colors)] for i in range(len(features))}
    
    # Meclis düzeni parametreleri
    pieces_per_slice_without_additional = math.ceil(total_seats / slices)
    pieces_per_slice = pieces_per_slice_without_additional + additional_rows
    
    # Açı hesaplamaları
    angle_per_slice = 180 / slices
    
    # Figür oluştur ve yarım daire çizin
    fig, ax = plt.subplots(figsize=(14, 8))
    radius = 10
    
    # Yeni yarıçap hesaplamaları
    piece_depth = radius / pieces_per_slice
    start_radius = piece_depth * additional_rows
    
    # Açısal boşluk
    angle_gap = 0.2
    radial_angles = np.linspace(180, 0, slices + 1)
    
    current_feature = 0
    current_color = feature_colors[features[current_feature]]
    remaining_seats = seats[current_feature]
    
    total_assigned_seats = 0
    
    for slice_index in range(slices):
        start_angle = radial_angles[slice_index]
        end_angle = radial_angles[slice_index + 1] - angle_gap
        piece_angle = end_angle - start_angle
        
        for piece_index in range(pieces_per_slice):
            if remaining_seats <= 0 and current_feature < len(features) - 1:
                current_feature += 1
                current_color = feature_colors[features[current_feature]]
                remaining_seats = seats[current_feature]
            
            if total_assigned_seats >= total_seats:
                break
            
            seat_angle = start_angle + piece_index * piece_angle / pieces_per_slice
            piece = patches.Wedge((0, 0), start_radius + piece_depth * (piece_index + 1), 
                                  seat_angle, seat_angle + piece_angle / pieces_per_slice, 
                                  facecolor=current_color, edgecolor='white')
            ax.add_patch(piece)
            
            remaining_seats -= 1
            total_assigned_seats += 1
    
    ax.set_xlim(-radius, radius)
    ax.set_ylim(0, radius)
    ax.axis('off')
    plt.title(f"{total_seats} Sandalyeli Meclis Temsili")

    # Legend creation
    legend_patches = [patches.Patch(color=feature_colors[feature], label=f"{feature} ({seats[i]} MV)") for i, feature in enumerate(features)]
    plt.legend(handles=legend_patches, loc='upper right', bbox_to_anchor=(1.15, 1))

    plt.show()
