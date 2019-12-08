import os
import codecs
import struct
from pprint import pprint


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

    def open_file(self):
        file = "/".join([os.getcwd(), 'PL.kdb'])

        # f.decode('cp1251').encode('utf-8')

        with open(file, 'rb') as f:
            signature = read_32(f)
            print("сигнатура " + str(hex(signature)))
            version = read_32(f)
            print("версия " + str(hex(version)))
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

            print(str(self.facts))
            rules_count = read_32(f)
            print("количество правил " + str(rules_count))
            i = 0
            while i < rules_count:
                id = read_32(f)
                name = read_chars(read_32(f), f)
                condi_strings = read_chars(read_32(f), f).split('&')
                for condi_string in condi_strings:
                    condi_string = condi_string.split('__')
                    obj = condi_string[0]
                    attribute = condi_string[1]
                    value = condi_string[2]
                    conditions = []
                    for fact in self.facts:
                        if fact['obj'] == obj and fact['value'] == value and fact['attribute'] == attribute:
                            conditions.append(fact)
                            break
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
            # obj = read_chars(read_32(f), f)
            # attribute = read_chars(read_32(f), f)
            # value = read_chars(read_32(f), f)
            # truth = read_double(f)
            # fact_type = self.switch_facts(read_32(f))

            # self.facts.append({
            #     'id': id,
            #     'obj': obj,
            #     'attribute': attribute,
            #     'value': value,
            #     'truth': truth,
            #     'fact_type': fact_type,
            # })
            # pprint(self.facts)


es = ExpertSystem()
es.open_file()