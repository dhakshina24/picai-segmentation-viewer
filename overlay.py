"""Overlay predicted cancer segmentation mask on T2 MRI slice"""
import cv2 
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib as mp

def transparent_overlay(img, mask, alpha=0.4):
    """Blend segmentation mask over MRI image"""
    # Converts grayscale MRI to BGR 
    img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) 
    # Remove outliers from mask and normalize
    prob_map = np.clip(mask, 0, 1)
    mask = (prob_map * 255).astype(np.uint8)
    # Convert to heatmap based on probability
    heatmap = cv2.applyColorMap(mask, cv2.COLORMAP_INFERNO) 
    # Overlay heatmap on original image
    overlay = cv2.addWeighted(img_bgr, 1 - alpha, heatmap, alpha, 0) 
    overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB) 

    # Plot color bar
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(overlay_rgb)
    ax.axis("off")

    norm = mp.colors.Normalize(vmin=0, vmax=1)
    cmap = plt.cm.get_cmap("inferno")
    cbar = plt.colorbar(mp.cm.ScalarMappable(norm=norm, cmap=cmap),
                        ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Lesion Confidence", fontsize=10)
    cbar.ax.tick_params(labelsize=8)
    cbar.outline.set_visible(False)

    return fig
