<h1>Код для поворота BMP изобажения на 90 градусов</h1>

<h3>Задание:</h3>
Преобразовать TrueColor BMP файл, развернув растр на 90 градусов. <br>
Длина
строки BMP файла выравнивается по 32-битовой границе, (4-м байт), при
необходимости к каждой строке в файле добавляются выравнивающие байты!
Изменить соответствующие поля в заголовке и сохранить файл под новым
именем.

------

<h3>Программная реализация: </h3>

```read_bmp```

```python
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
```
Функция для считывая BMP изображения. Сначала считываются заголовок BMP изображения ```bmp_header```, в котором храняться его размер и смещение пикселей, 
и ```dip_header```, в котором храниться  его ширина, высота, глубина цвета и сжатие. <br>
Далее узнаётся размер изображения и делается выравнивание по 32-битной границе. В случае если изображение 8-бит, то идёт корректирование палитры цветов RGBA

-----

```rotate_bmp_90```

```python
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
```
Основная функция поворота изображения на 90 градусов. <br>
Тут происходит переопределение новый размеров изображения и запись информации о новом расположении пикселей в массив. <br>
Также переопределение расположения пикселей разделено для 8-битных изображений и 24-битных

-----

Оставшиеся функции ```write_bmp``` и ```main``` можно увидеть [тут](https://github.com/sinedfq/Convert_BMP/tree/main) 

-----

<h3>Результат работы программы: </h3>

![image](https://github.com/user-attachments/assets/8e2d0df7-9993-4b6d-88d0-c4684ea08230)
