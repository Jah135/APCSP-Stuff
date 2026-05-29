FILE_HEADER_SIZE = 14
DIB_HEADER_SIZE = 40  # BITMAPINFOHEADER variant


class Image:
    pixels: list[tuple[int, int, int]]
    width: int
    height: int

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.pixels = [(0, 0, 0)] * (width * height)


def write_image_to_file(image: Image, path: str):
    total_header_size = FILE_HEADER_SIZE + DIB_HEADER_SIZE
    total_file_size = total_header_size + (image.width * image.height * 4)

    with open("test.bmp", "wb") as f:
        # file header
        f.write(b"BM")
        f.write(total_file_size.to_bytes(4, "little"))
        f.write((0).to_bytes(2, "little"))
        f.write((0).to_bytes(2, "little"))
        f.write(total_header_size.to_bytes(4, "little"))

        # dib header
        f.write((40).to_bytes(4, "little"))
        f.write(image.width.to_bytes(4, "little"))
        f.write(image.height.to_bytes(4, "little"))
        f.write((1).to_bytes(2, "little"))
        f.write(
            (8 * 4).to_bytes(2, "little")
        )  # 8 bits per channel, 3 channels + 1 padding
        f.write((0).to_bytes(4, "little"))
        f.write(total_file_size.to_bytes(4, "little"))
        f.write((0).to_bytes(4, "little"))
        f.write((0).to_bytes(4, "little"))
        f.write((0).to_bytes(4, "little"))
        f.write((0).to_bytes(4, "little"))

        # pixel data
        for y in range(image.height - 1, -1, -1):
            for x in range(0, image.width):
                r, g, b = image.pixels[y * image.width + x]

                f.write(bytearray([b, g, r, 0]))


test_image = Image(25, 25)

for x in range(test_image.width):
    for y in range(test_image.height):
        test_image.pixels[y * test_image.width + x] = (
            int(x / (test_image.width - 1) * 255),
            int(y / (test_image.height - 1) * 255),
            0,
        )

write_image_to_file(test_image, "test.bmp")
