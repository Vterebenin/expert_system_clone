import os
import struct
import time
from django.db import models


def read_double(f):
    value, = struct.unpack('d', f.read(8))
    return value


def read_32(f):
    value, = struct.unpack('i', f.read(4))
    return value


def read_chars(char_length, f):
    value = ""
    for r in range(char_length):
        val_char, = struct.unpack('s', f.read(1))
        value = value + val_char.decode('cp1251')
    return value


class File(models.Model):
    """
    file - файл базы знаний в формате kdb
    name - имя файла для отображения на фронте
    """
    file = models.FileField(upload_to='uploads/')
    name = models.CharField(max_length=50)


class ExpertSystem():
    facts = []
    rules = []
    questions = []

    @staticmethod
    def switch_facts(fact_type):
        switcher = {
            0: 'Изначальный',
            1: 'Промежуточный',
            2: 'Финальный',
        }
        return switcher.get(fact_type, 'Изначальный')

    def compute(self, initial_facts, target_fact, output=None, truth=1.0, level=1):
        if output is None:
            output = []

        for r in self.rules:
            if target_fact in r.conclusions:
                output.append(f'{level}) Факт "{target_fact}" является заключением правила *{r}*')
                rule_is_fine = True
                for f in r.conditions:
                    if f.fact_type == 'Изначальный':
                        if f in initial_facts:
                            truth = min(r.truth, f.truth)
                            output.append(f'{level}) Правило "{r}" ещё не сработало. Нашли исходный факт: "{f}"')
                        else:
                            rule_is_fine = False
                            break
                    else:
                        output.append(f'{level}) Правило "{r}" ещё не сработало. Проверяем факт: "{f}"')
                        child_truth = 1.0
                        child_result = self.compute(initial_facts, f, output, child_truth, level + 1)
                        if child_result is True:
                            truth = min(r.truth, child_truth)
                        else:
                            rule_is_fine = False
                            break
                if rule_is_fine is True:
                    output.append(f'{level}) Сработало правило: *{r}*')
                    return True
                else:
                    output.append(f'{level}) Правило *{r}* не выполняется! пропускаем дальнейшую обработку!')
        return False

    def check_fact(self, initial_facts, target_fact, output=None):
        if output is None:
            output = []

        t1 = time.time()
        output.append(f'Проверяем выполнение факта "{target_fact}"')
        truth = 1.0
        result = self.compute(initial_facts, target_fact, output, truth)
        if result is True:
            output.append(f'Факт "{target_fact}" подтверждается с достоверностью {truth}!')
        else:
            output.append(f'Факт "{target_fact}" не подтверждается!')
        t2 = time.time()
        timing = t2 - t1
        output.append(f'Было затрачено {timing}" времени')
        return output

    def open_file(self, file_name):
        file = "/".join([os.getcwd(), file_name])

        self.facts = []
        self.rules = []
        self.questions = []
        # f.decode('cp1251').encode('utf-8')

        with open(file, 'rb') as f:
            signature = read_32(f)
            print("сигнатура " + str(hex(signature)))
            version = read_32(f)
            print("версия " + str(hex(version)))
            # читаем факты
            facts_count = read_32(f)
            print("количество фактов " + str(facts_count))
            i = 0
            while i < facts_count:
                id = read_32(f)
                obj = read_chars(read_32(f), f)
                attribute = read_chars(read_32(f), f)
                value = read_chars(read_32(f), f)
                truth = read_double(f)
                fact_type = self.switch_facts(read_32(f))

                self.facts.append({
                    'id': id,
                    'obj': obj,
                    'attribute': attribute,
                    'value': value,
                    'truth': truth,
                    'fact_type': fact_type,
                })
                i += 1

            # читаем правила
            print(str(self.facts))
            rules_count = read_32(f)
            print("количество правил " + str(rules_count))
            i = 0
            while i < rules_count:
                id = read_32(f)
                name = read_chars(read_32(f), f)
                condi_strings = read_chars(read_32(f), f).split('&')
                conditions = []
                for condi_string in condi_strings:
                    condi_string = condi_string.split('__')
                    obj = condi_string[0]
                    attribute = condi_string[1]
                    value = condi_string[2]
                    for fact in self.facts:
                        if fact['obj'] == obj and fact['value'] == value and fact['attribute'] == attribute:
                            conditions.append(fact)
                            # break
                conclusions_count = read_32(f)
                conclusions = []
                for j in range(conclusions_count):
                    index = read_32(f)
                    if index < len(self.facts):
                        conclusions.append(self.facts[index])

                truth = read_double(f)
                self.rules.append({
                    'id': id,
                    'name': name,
                    'conditions': conditions,
                    'conclusions': conclusions,
                    'truth': truth,
                })
                i += 1
            print(self.rules)

            # читаем вопросы
            question_count = read_32(f)
            print("количество вопросов " + str(question_count))
            i = 0
            while i < question_count:
                id = read_32(f)
                text = read_chars(read_32(f), f)
                true_fact = self.facts[read_32(f)]
                false_fact = self.facts[read_32(f)]
                self.questions.append({
                    'id': id,
                    'text': text,
                    'true_fact': true_fact,
                    'false_fact': false_fact,
                })
                i += 1
            print(self.questions)
            return {
                'questions': self.questions,
                'facts': self.facts,
                'rules': self.rules,
            }


