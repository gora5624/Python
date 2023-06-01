from PIL import Image


def get_color_at_point(image_path, x, y):
    image = Image.open(image_path)
    pixels = image.load()
    return pixels[x, y]


def create_mask(image_path, mask_color, filename="result.png"):
    image = Image.open(image_path)
    width, height = image.size
    mask = Image.new("1", (width, height))
    pixels = image.load()
    mask_pixels = mask.load()
    
    for x in range(width):
        for y in range(height):
            if pixels[x, y] == mask_color:
                mask_pixels[x, y] = 1
    
    return mask


def main():
    image_path = r"D:\mask.png"
    x = 10
    y = 10
    
    color_at_point = get_color_at_point(image_path, x, y)
    print(f"Color at point ({x}, {y}): {color_at_point}")
    
    mask = create_mask(image_path, color_at_point)
    mask.show()
    
    result = Image.new("RGBA", mask.size)
    mask = mask.convert("L")
    mask.save(r"D:\chBmask.png")
    result.paste(color_at_point, mask=mask)
    result.show()
    result.save(r"D:\output.png")


if __name__ == "__main__":
    main()