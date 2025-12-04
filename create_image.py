from PIL import Image, ImageFilter
import numpy as np
import os

def combine_with_background(gradient_path, output_path):
    """
    Combines a gradient image with a black background and saves it,
    with enhanced smoothing.

    gradient_path (str): The path to the gradient image.
    output_path (str): The path to save the new image.
    """
    try:

        gradient_image = Image.open(gradient_path).convert("RGBA")

        # Apply Gaussian blur
        smoothed_gradient = gradient_image.filter(ImageFilter.GaussianBlur(radius=25))

        # Create black background image
        background = Image.new("RGBA", smoothed_gradient.size, (0, 0, 0, 255))

        # Convert images to numpy arrays
        gradient_np = np.array(smoothed_gradient)
        background_np = np.array(background)

        alpha = gradient_np[:, :, 3] / 255.0
        
        alpha = alpha[:, :, np.newaxis]

        blended_np = (gradient_np[:, :, :3] * alpha + background_np[:, :, :3] * (1 - alpha)).astype(np.uint8)
        
        # Create a new image from the blended numpy array
        blended_image = Image.fromarray(blended_np, 'RGB')


        # Save the image
        blended_image.save(output_path, "PNG")
        print(f"Image saved to {output_path}")

    except FileNotFoundError:
        print(f"Error: The file {gradient_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gradient_file = os.path.join(script_dir, "Gradients", "gradient.png")
    output_file = os.path.join(script_dir, "output_image_smooth_v2.png")
    combine_with_background(gradient_file, output_file)
