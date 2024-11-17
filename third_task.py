def read_file():
    with open ("./data/third_task.txt", encoding="utf-8") as file:
        lines = file.readlines()
        table = []
        for line in lines:
            words = line.strip().split(" ")
            table.append(words)

        return table
    

def fill_na(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == 'N/A':
                table[i][j] = table[i][j-1] + int(table[i][j+1]) / 2
            else:
                table[i][j] = int(table[i][j])


def filter_and_sum(table):
    results = []
    for line in table:
        filtered_lines = [num for num in line if num % 2 != 0 and num <= 500]  
        lines_sum = sum(filtered_lines)  
        results.append(lines_sum)  
    return results

def write_results_to_file(results, filename='result_third_task.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        for result in results:
            file.write(f"{result}\n")


table = read_file()
fill_na(table)
print(table)    

filtered_sums = filter_and_sum(table)  
write_results_to_file(filtered_sums)   