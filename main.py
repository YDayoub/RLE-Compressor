import argparse
import numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
chunk_size = 128


def compress_chunk(chunk):
    compressed = bytearray()
    last = chunk[0]
    count = 1
    for i in chunk[1:]:
        if i == last:
            count += 1
        else:
            compressed.append((count | (last * chunk_size)))
            count = 1
            last = i
    compressed.append((count | last * chunk_size))
    return compressed


def compress_row(row):
    compressed = bytearray()
    chunks = split_bits(row, chunk_size - 1)
    for chunk in chunks:
        compressed.extend(compress_chunk(chunk))
    return compressed


def split_bits(bits, width):
    for i in range(0, len(bits), width):
        yield bits[i:i + width]


def compress_in_executor(executor, bits, width):
    row_compressed = []
    for row in split_bits(bits, width):
        compressor = executor.submit(compress_row, row)
        row_compressed.append(compressor)
    compressed = bytearray()
    for compressor in row_compressed:
        compressed.extend(compressor.result())
    return compressed


def compress_image(in_file, out_file, executor=None):
    executor = executor if executor else ProcessPoolExecutor()
    with Image.open(in_file) as img:
        bits = np.array(img.convert('1').getdata()) > 0
        width, height = img.size
    compressed = compress_in_executor(executor, bits, width)
    with open(out_file, 'wb') as file:
        file.write(width.to_bytes(2, 'little'))
        file.write(height.to_bytes(2, 'little'))
        file.write(compressed)


def function_dir(in_dir, out_dir, function):
    if not out_dir.exists():
        out_dir.mkdir()
    executor = ProcessPoolExecutor()
    extension = '.rle' if function.__name__ == 'compress_image' else '.bmp'
    for file in (f for f in in_dir.iterdir()):
        out_file = (out_dir / file.name).with_suffix(extension)
        executor.submit(function, str(file), str(out_file))


def decompress(width, height, bytes):
    image = Image.new('1', (width, height))
    col = 0
    row = 0
    for byte in bytes:
        color = (byte & 128) >> 7
        count = byte & ~128
        for i in range(count):
            image.putpixel((row, col), color)
            row += 1
        if not row % width:
            col += 1
            row = 0
    return image

def decompress_image(in_file,out_file):
    with open(in_file, 'rb') as file:
        width = int.from_bytes(file.read(2), 'little')
        height = int.from_bytes(file.read(2), 'little')
        image = decompress(width, height, file.read())
        image.save(out_file)


if __name__ == '__main__':
    txt = 'This is an implementation of RLE-algorithm to compress Black and White images'
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='path to input directory', required=True)
    parser.add_argument('-o', '--output', help='path to output diretory', required=True)
    parser.add_argument('--compress', dest='action_compress', action='store_true')
    parser.add_argument('--decompress', dest='action_compress', action='store_false')
    parser.set_defaults(action_compress=True)

    try:
        args = parser.parse_args()
        input_dir = args.input
        output_dir = args.output
        act_compress = args.action_compress
        if act_compress:
            function = compress_image
        else:
            function = decompress_image
        function_dir(Path(input_dir), Path(output_dir), function)

    except Exception as e:
        print(e)
