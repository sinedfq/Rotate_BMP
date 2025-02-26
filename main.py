import struct


def read_bmp(filename):
    with open(filename, 'rb') as f:
        bmp_header = f.read(14)
        dib_header = f.read(40)

        width = struct.unpack('<I', dib_header[4:8])[0]
        height = struct.unpack('<i', dib_header[8:12])[0]  # Signed integer for height
        bits_per_pixel = struct.unpack('<H', dib_header[14:16])[0]

        row_size = ((width * bits_per_pixel + 31) // 32) * 4
        palette = None

        if bits_per_pixel == 8:
            palette = f.read(1024)  # 256 colors * 4 bytes per entry (RGBA)

        pixel_data = [f.read(row_size) for _ in range(abs(height))]

    return bmp_header, dib_header, width, height, bits_per_pixel, palette, pixel_data


def rotate_bmp_90(width, height, bits_per_pixel, palette, pixel_data):
    new_width, new_height = height, width
    new_row_size = ((new_width * bits_per_pixel + 31) // 32) * 4
    rotated_data = [bytearray(new_row_size) for _ in range(new_height)]

    if bits_per_pixel == 24:
        for y in range(abs(height)):
            for x in range(width):
                old_offset = x * 3
                new_x, new_y = new_width - y - 1, x
                new_offset = new_x * 3
                rotated_data[new_y][new_offset:new_offset + 3] = pixel_data[y][old_offset:old_offset + 3]
    elif bits_per_pixel == 8:
        for y in range(abs(height)):
            for x in range(width):
                old_offset = x
                new_x, new_y = new_width - y - 1, x
                new_offset = new_x
                rotated_data[new_y][new_offset] = pixel_data[y][old_offset]

    return new_width, new_height, rotated_data, palette


def write_bmp(filename, bmp_header, dib_header, width, height, bits_per_pixel, palette, pixel_data):
    with open(filename, 'wb') as f:
        f.write(bmp_header)
        f.write(dib_header[:4])
        f.write(struct.pack('<I', width))
        f.write(struct.pack('<i', height))  # Signed integer for height
        f.write(dib_header[12:])

        if bits_per_pixel == 8 and palette:
            f.write(palette)

        for row in pixel_data:
            f.write(row)


if __name__ == "__main__":
    input_bmp_file = "./Images/_сarib_TC.bmp"
    output_bmp_file = "./Images/carib_Out.bmp"

    try:
        bmp_header, dib_header, width, height, bits_per_pixel, palette, pixel_data = read_bmp(input_bmp_file)
        new_width, new_height, rotated_data, palette = rotate_bmp_90(width, height, bits_per_pixel, palette, pixel_data)
        write_bmp(output_bmp_file, bmp_header, dib_header, new_width, new_height, bits_per_pixel, palette, rotated_data)
        print("Rotation successful.")
    except Exception as e:
        print(f"An error occurred: {e}")