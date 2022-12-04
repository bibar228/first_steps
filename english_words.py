import json
import random

with open("gg.json", "r", encoding="UTF-8") as file:
    d = json.load(file)

class Bareba:
    def __init__(self, lst):
        self.lst = lst
        self.mistakes = {}

    def check_word(self, word, translate):
        if type(self.lst[word]) == list:
            if translate in self.lst[word]:
                return "+"
            else:
                return "-"
        else:
            if translate == self.lst[word]:
                return "+"
            else:
                return "-"

    def mistake_word(self, key, value):
        if key not in self.mistakes.keys():
            self.mistakes[key] = value
mm = list(d.keys())
random.shuffle(mm)
d = {key: d[key] for key in mm}
x = Bareba(d)
for i, j in d.items():
    print(i)
    command = input()
    if command == "ВСЕ":
        break
    sign = x.check_word(i, command)
    count = 0
    while sign != "+" and count != len(j):
        x.mistake_word(i, j)
        print("Не правильный ответ.")
        print("Повторите попытку:")
        print(i)
        if type(d[i]) == list:
            print(f"Подсказка: {d[i][0][:count]}")
            j = d[i][0]
        else:
            print(f"Подсказка: {d[i][:count]}")
        sign = x.check_word(i, input())
        count += 1

print(x.mistakes)
