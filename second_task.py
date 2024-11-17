with open ("./data/second_task.txt", encoding="utf-8") as file:
    text = file.readlines()

numbers_array = []
index=0
for line in text:
    numbers_array.append(0)
    for number in line.split():
        int_num = int(number)
        if ((abs(int_num) ** 2) <= 100000):
            numbers_array[index]+= int_num
    index+=1

result_file = open('result_second_task.txt', 'w+')

numbers_array = sorted(numbers_array, reverse=True)

for i in range(10):
    result_file.write(f'{str(numbers_array[i])}\n')
result_file.close()
