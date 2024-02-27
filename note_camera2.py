from PIL import Image, ImageDraw

def magic_wand(input_image_path, output_image_path, seed_x, seed_y, tolerance=10):
    # Open the input image
    image = Image.open(input_image_path)
    width, height = image.size

    # Create a mask to store selected pixels
    mask = Image.new('1', (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # Get the color of the seed pixel
    seed_color = image.getpixel((seed_x, seed_y))

    # Flood fill algorithm to select pixels
    stack = [(seed_x, seed_y)]
    while stack:
        x, y = stack.pop()

        # Check if the pixel is within the image bounds and has similar color
        if 0 <= x < width and 0 <= y < height and mask.getpixel((x, y)) == 0:
            pixel_color = image.getpixel((x, y))
            if all(abs(pixel_color[i] - seed_color[i]) <= tolerance for i in range(3)):
                draw.point((x, y), fill=255)  # Select the pixel
                stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

    # Apply the mask to the original image
    result = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    result.paste(image, (0, 0), mask)

    # Save the result
    result.save(output_image_path)
    print("Image with selected area saved successfully!")

# Example usage
input_image_path = "learning_camera_0001.png"  # Path to the input PNG file
output_image_path = "learning_camera_0001_1.png"  # Path to save the image with selected area

# Coordinates for the seed pixel (starting point for selection)
seed_x = 100
seed_y = 100

# Tolerance for color similarity (adjust as needed)
tolerance = 20

# Call the function to apply magic wand selection and save the result
magic_wand(input_image_path, output_image_path, seed_x, seed_y, tolerance)