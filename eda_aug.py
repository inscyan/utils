import random

import jieba
import pprint
import pandas as pd

# 加载行业词典
jieba.load_userdict('industry_dict.txt')

# 加载同义词典
synonym_dict = {}
df = pd.read_excel('synonym_dict.xlsx').fillna('')
for idx, row in df.iterrows():
    if row['词典'].strip() and row['同义词'].strip():
        synonym_dict[row['词典'].strip()] = row['同义词'].strip().split('，')
synonym_dict_words = synonym_dict.keys()


def synonym_replacement(words, n):
    new_words = words.copy()
    random_word_list = list(set(words))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        if random_word in synonym_dict_words:
            synonyms = synonym_dict[random_word]
            synonym = random.choice(synonyms)
            new_words = [synonym if word == random_word else word for word in new_words]
            # print("replaced", random_word, "with", synonym)
            num_replaced += 1
            if num_replaced >= n:
                break

    return new_words


def add_word(new_words):
    synonyms = []
    counter = 0
    while len(synonyms) < 1:
        random_word = new_words[random.randint(0, len(new_words) - 1)]
        try:
            synonyms = synonym_dict[random_word]
        except:
            counter += 1
            if counter >= 10:
                return
    random_synonym = random.choice(synonyms)
    random_idx = random.randint(0, len(new_words) - 1)
    new_words.insert(random_idx, random_synonym)


def random_insertion(words, n):
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words)

    return new_words


def swap_word(new_words):
    random_idx_1 = random.randint(0, len(new_words) - 1)
    random_idx_2 = random_idx_1
    counter = 0
    while random_idx_2 == random_idx_1:
        random_idx_2 = random.randint(0, len(new_words) - 1)
        counter += 1
        if counter > 3:
            return
    new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]


def random_swap(words, n):
    new_words = words.copy()
    for _ in range(n):
        swap_word(new_words)

    return new_words


def random_deletion(words, p):
    if len(words) == 1:
        return words

    new_words = []
    for word in words:
        r = random.uniform(0, 1)
        if r > p:
            new_words.append(word)

    if len(new_words) == 0:
        rand_int = random.randint(0, len(words) - 1)
        return [words[rand_int]]

    return new_words


def eda(raw_sen,
        num_aug=10,
        return_split_char='',
        alpha_sr=0.1,
        alpha_ri=0.1,
        alpha_rs=0.1,
        p_rd=0.1,
        synonym_replace=True):
    words = jieba.lcut(raw_sen)
    # print('words:', words)
    num_words = len(words)

    augmented_sentences = []
    num_new_per_technique = int(num_aug / 3) + 1
    n_sr = max(1, int(alpha_sr * num_words))
    n_ri = max(1, int(alpha_ri * num_words))
    n_rs = max(1, int(alpha_rs * num_words))

    # sr for standard
    # for _ in range(num_new_per_technique):
    #    a_words = synonym_replacement(words, n_sr)
    #    augmented_sentences.append(return_split_char.join(a_words))

    # sr for kg
    # if synonym_replace:
    synonym_words = synonym_replacement(words, n_sr)
    # print(return_split_char.join(synonym_words))

    # ri
    for _ in range(num_new_per_technique):
        a_words = random_insertion(synonym_words, n_ri)
        augmented_sentences.append(return_split_char.join(a_words))
    # pprint.pprint(augmented_sentences)

    # rs
    for _ in range(num_new_per_technique):
        a_words = random_swap(synonym_words, n_rs)
        augmented_sentences.append(return_split_char.join(a_words))
    # pprint.pprint(augmented_sentences[4:])

    # rd
    for _ in range(num_new_per_technique):
        a_words = random_deletion(synonym_words, p_rd)
        augmented_sentences.append(return_split_char.join(a_words))
    # pprint.pprint(augmented_sentences[8:])

    random.shuffle(augmented_sentences)

    if num_aug >= 1:
        augmented_sentences = augmented_sentences[:num_aug - 2]
    else:
        keep_prob = num_aug / len(augmented_sentences)
        augmented_sentences = [
            s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

    augmented_sentences.append(return_split_char.join(synonym_words))
    augmented_sentences.append(return_split_char.join(words))

    return augmented_sentences


if __name__ == "__main__":
    sen = '我爱北京天安门'
    augmented_sens = eda(sen, return_split_char=' ')
    pprint.pprint(augmented_sens)
