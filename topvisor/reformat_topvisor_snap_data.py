

def reformat_topvisor_data(csv_file: str):

    with open(csv_file, 'r', encoding='utf-8') as file:
        src = file.read().splitlines()
    file.close()

    src2 = []

    for item in src:
        src2.append(list(item.split(';')))

    dictionary_array = len(src2)
    string_array = len(src2[0])
    with open('data/snap_result.csv', 'w', encoding='utf-8') as file:
        for i in range(1, string_array):
            for v in range(1, dictionary_array):
                file.write('%s;%s;%s\n'%(src2[v][0],src2[0][i], src2[v][i]))
    file.close()
