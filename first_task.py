with open ("./data/first_task.txt", encoding="utf-8") as file:
    lines = file.readlines()

#Первое
freq_dictironary = {}
text_array = []
for line in lines:
    _line = line.replace('\'', '').replace('?','').replace('!','').replace('.','').replace('-','').replace(',','').lower().strip()
    text_array+= _line.split(' ')


for word in text_array:
    if (word in freq_dictironary):
        freq_dictironary[word]+=1
    else:
        freq_dictironary[word]=1

freq_dictironary = sorted(freq_dictironary.items(), key=lambda item: item[1], reverse=True)

result_file = open('result_first_task.txt', 'w+')

for key_value in freq_dictironary:
    result_file.write(f'{key_value[0]}: {key_value[1]}\n')
result_file.close()

#Вариант 33
length_word_dic = {'five_letters': 0,
                   'more_five_letters': 0,
                   'all_words': 0
                   }

for word in text_array:
    if (len(word) <= 5):
        length_word_dic['five_letters'] +=1
    else:
        length_word_dic['more_five_letters'] +=1
    length_word_dic['all_words'] +=1

print(f"Всего слов с длинной от 1 до 5 букв: {length_word_dic['five_letters']} \nСлов с длинной больше 5 букв: {length_word_dic['more_five_letters']} \nДоля всех слов, не превышающих длину в 5 символов: {round((length_word_dic['five_letters'] / length_word_dic['all_words']) * 100, 2)}")