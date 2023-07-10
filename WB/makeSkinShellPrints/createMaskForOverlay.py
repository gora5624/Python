from PIL import Image


def get_color_at_point(image_path, x, y):
    image = Image.open(image_path)
    pixels = image.load()
    return pixels[x, y]


def create_mask(image_path, mask_color):
    image = Image.open(image_path)
    width, height = image.size
    mask = Image.new("1", (width, height))
    pixels = image.load()
    mask_pixels = mask.load()
    for x in range(width):
        for y in range(height):
            if (0,0,0)<=pixels[x, y]<(70,70,70):#== mask_color:
                mask_pixels[x, y] = 1
    return mask

def main(clownPath, maskPath):
    # image_path = r"D:\mask.png"
    x = 1190
    y = 10
    #color_at_point = get_color_at_point(clownPath, x, y)
    color_at_point = (0,0,0)
    print(f"Color at point ({x}, {y}): {color_at_point}")
    mask = create_mask(clownPath, color_at_point)
    # result = Image.new("RGBA", mask.size)
    mask = mask.convert("L")
    mask.save(maskPath)
    # mask.save(r"D:\chBmask.png")
    # result.paste(color_at_point, mask=mask)
    # result.show()
    # result.save(r"D:\output.png")


if __name__ == "__main__":
    clownPath = r"\\192.168.0.33\shared\_Общие документы_\Егор\Модели SkinShell\Рендеры\Чехол iPhone 11 (6.1) силикон с зак.кам. черный противоуд. SkinShell\1_clown.png"
    maskPath = r"D:\chBmask.png"
    main(clownPath, maskPath)