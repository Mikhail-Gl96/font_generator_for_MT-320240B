import numpy as np, sys
from PIL import Image, ImageFont


def arr_print(arr, symb_nth=0):
    arr_len = list(arr.shape)
    arr_out = []
    for dim in range(arr_len[0]):
        arr_current_string = []
        for dim_inside in arr[dim]:
            arr_current_string.append(dim_inside)
        arr_out.append(arr_current_string.copy())
    new = '\n'
    round_number = 2
    max_numbers_per_column = 3 + round_number
    def gen_nth(length):
        return "".join([" " for i in range(length)])
    def check_enough_elements(string, length):
        add_number = 0
        if len(string) < length:
            add_number = length - len(string)
        return add_number
    line_horizontal = gen_nth(symb_nth) + "-" * (arr_len[1]*(max_numbers_per_column + 3) + 1)
    generated_data = f"{new}{gen_nth(symb_nth)}| ".join(["".join([str(iii) + gen_nth(check_enough_elements(str(iii), max_numbers_per_column)) + " | " for iii in np.around(i, decimals=round_number)]) for i in arr_out])
    return f'\n{line_horizontal}\n{gen_nth(symb_nth)}| {generated_data}\n{line_horizontal}'


def generate_string(data, file, size):
    print(f"doc = {file.name}")
    font = ImageFont.truetype(font_name, size=size)
    ascent, descent = font.getmetrics()
    (width, baseline), (offset_x, offset_y) = font.font.getsize(data)
    print(f'width = {width} baseline = {baseline}, offset_x = {offset_x}, offset_y = {offset_y}  '
          f'ascent = {ascent}  descent = {descent}')

    mask = font.getmask(text=f"{data}")
    mask_reshaped = np.array(mask).reshape(baseline, width)
    # print(arr_print(mask_reshaped))
    for i in range(mask_reshaped.shape[0]):
        for j in range(mask_reshaped.shape[1]):
            if mask_reshaped[i][j] > 100:
                mask_reshaped[i][j] = 1
            else:
                mask_reshaped[i][j] = 0
    print(f'mask_reshaped = {mask_reshaped.shape}')
    number_of_input_symb = len(data)
    #               height          width
    output_size = (baseline, width / number_of_input_symb)
    print(f'output_size  height = {baseline}  width = {width / number_of_input_symb}')
    data_out = [[[] for ii in range(output_size[0])] for i in range(number_of_input_symb)]
    # [ symb_1, symb_2, ...]  symb_1 = [[str_1], [str_2], ...]
    for string in range(mask_reshaped.shape[0]):    # (height)
        data_string = mask_reshaped[string]
        data_collected = []
        found_symbols = 0
        for column in range(data_string.shape[0]):     # (width)
            if found_symbols < output_size[1]:
                data_collected.append(mask_reshaped[string][column])
                found_symbols += 1
                if column == data_string.shape[0] - 1:
                    found_symbols = 1
                    data_out[int((column + 1) // output_size[1]) - 1][string].append(data_collected.copy())
                    data_collected.clear()
            elif found_symbols == output_size[1]:
                found_symbols = 1
                data_out[int(column//output_size[1]) - 1][string].append(data_collected.copy())
                data_collected.clear()
                data_collected.append(mask_reshaped[string][column])
    print("")
    iterat = 0
    count_strings_zero = 0
    for i in data_out:
        iterat += 1
        for j in i:
            if np.max(j) == 0:
                count_strings_zero += 1
            file.write(str(j).replace("0", "-").replace(",", "").replace("[", "").replace("]", "") + '\n')
        # print(f'iter = {iterat}  count_strings_zero = {count_strings_zero}')
        count_strings_zero = 0
        file.write('\n')
    file.close()


# font_name = 'JetBrainsMono-Regular.ttf'
font_name = 'bgothl.ttf'


file_numbers = open("file_numbers.txt", 'w', encoding='utf-8')
file_rus = open("file_rus.txt", 'w', encoding='utf-8')
file_RUS = open("file_RUS1.txt", 'w', encoding='utf-8')
file_eng = open("file_eng.txt", 'w', encoding='utf-8')
file_ENG = open("file_ENG1.txt", 'w', encoding='utf-8')


char_eng = [chr(ord("a") + i) for i in range(26)]
char_ENG = [chr(ord("A") + i) for i in range(26)]

char_rus = [chr(ord("а") + i) for i in range(32)]
char_RUS = [chr(ord("А") + i) for i in range(32)]
char_rus.append(chr(ord('ё')))
char_RUS.append(chr(ord('Ё')))
char_numbers = [chr(ord("0") + i) for i in range(10)]
# print(char_eng, char_ENG, char_rus, char_RUS, char_numbers)

files = [file_numbers, file_rus, file_RUS, file_eng, file_ENG]
data_args = [char_numbers, char_rus, char_RUS, char_eng, char_ENG]
for index in range(len(files)):
    generate_string(data="".join(data_args[index]), file=files[index], size=16)


