import shutil
import argparse
import pandas as pd
import seq2seq_model as m
import numpy as np
import tensorflow as tf
import os
from sklearn.model_selection import train_test_split

def check_spell(text, am_giua, viet_tat):
    am_dau = ['ch', 'đ', 'kh', 'ngh', 'ng','gh', 'nh', 'tr', 'th', 'ph', 'p', 'q',
              'r', 's', 't', 'v', 'b', 'x', 'c', 'd','g', 'h','k', 'l', 'm', 'n', '']
    am_cuoi = ['ch', 'ng', 'nh', 'c', 'm', 'n', 'p', 't', '']
    count = 0
    if text in viet_tat:
        return True
    for j in am_dau:
        if len(text)>=3:
            if text[0:3] in am_dau:
                temp = text[3:]
                text = temp
                break
        if len(text)>=2:
            if text[0:2] in am_dau:
                temp = text[2:]
                text = temp
                break
        if len(text)>=1:
            if text[0:1] in am_dau:
                temp = text[1:]
                text = temp
                break
    for k in am_cuoi:
        if len(text)>=2:
            if text[-2:] in am_cuoi:
                temp = text[:-2]
                text = temp
                break
        if len(text)>=1:
            if text[-1:] in am_cuoi:
                temp = text[:-1]
                text = temp
                break
    if text not in am_giua:
        count = count + 1
    if count>0:
        return False
    else:
        return True

def check_dial(text):
    if text.isalpha():
        return True
    if text.isdigit():
        return False
    for i in range(len(text)):
        if not (text[i].isdigit() or text[i].isalpha()):
            return False
    return True
def convert_word(text):
    temp = ''
    for i in text:
        temp = temp + ' ' + i
    return temp.strip()
def heuristic_data(text):
    List_Data = text.split()
    text = text.lower()
    list_data = text.split()
    for i in range(len(list_data)):
        if list_data[i] in dictionary:
            list_data[i] = dictionary[list_data[i]]
        if List_Data[i][0].isupper():
            list_data[i] = list_data[i][0].upper() + list_data[i][1:]
    data = " ".join(list_data)
    return data

def evaluate(sentence):
    attention_plot = np.zeros((max_length_targ, max_length_inp))

    sentence = m.preprocess_sentence(sentence)
    try:
        inputs = [inp_lang.word_index[i] for i in sentence.split(' ')]
    except:
        return sentence
    # inputs = [inp_lang.word_index[i] for i in sentence.split(' ')]
    inputs = tf.keras.preprocessing.sequence.pad_sequences([inputs],
                                                            maxlen=max_length_inp,
                                                            padding='post')
    inputs = tf.convert_to_tensor(inputs)

    result = ''

    hidden = [tf.zeros((1, units))]
    enc_out, enc_hidden = encoder(inputs, hidden)

    dec_hidden = enc_hidden
    dec_input = tf.expand_dims([targ_lang.word_index['<start>']], 0)

    for t in range(max_length_targ):
        predictions, dec_hidden, attention_weights = decoder(dec_input, dec_hidden, enc_out)
        attention_weights = tf.reshape(attention_weights, (-1, ))
        attention_plot[t] = attention_weights.numpy()

        predicted_id = tf.argmax(predictions[0]).numpy()

        result += targ_lang.index_word[predicted_id] + ' '

        if targ_lang.index_word[predicted_id] == '<end>':
            return result
        dec_input = tf.expand_dims([predicted_id], 0)

    return result


def parse_args():
    parser = argparse.ArgumentParser(description="Correcting texts in an input file")
    parser.add_argument("input_file", type=str, help="Path to the input text file", default='./input.txt')
    parser.add_argument("output_file", type=str, help="Path to the output corrected text file", default='./output.txt')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    arguments = parse_args()
    input_file = arguments.input_file
    output_file = arguments.output_file



    res = pd.read_csv('./data/csv_data_word.csv',dtype=str, sep='\t')


    inp = list()
    tar = list()
    for i in range(len(res)):
        inp.append(m.preprocess_sentence(res.iloc[i, 0]))
        tar.append(m.preprocess_sentence(res.iloc[i, 1]))
    inp = tuple(inp)
    tar = tuple(tar)
    input_tensor, target_tensor, inp_lang, targ_lang = m.load_dataset(inp, tar)
    max_length_targ, max_length_inp = m.max_length(target_tensor), m.max_length(input_tensor)
    input_tensor_train, input_tensor_val, target_tensor_train, target_tensor_val = train_test_split(input_tensor, target_tensor, test_size=0.2)



    BUFFER_SIZE = len(input_tensor_train)
    BATCH_SIZE = 64
    steps_per_epoch = len(input_tensor_train)//BATCH_SIZE
    embedding_dim = 256
    units = 1024
    vocab_inp_size = len(inp_lang.word_index)+1
    vocab_tar_size = len(targ_lang.word_index)+1

    dataset = tf.data.Dataset.from_tensor_slices((input_tensor_train, target_tensor_train)).shuffle(BUFFER_SIZE)
    dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)

    example_input_batch, example_target_batch = next(iter(dataset))
    example_input_batch.shape, example_target_batch.shape

    encoder = m.Encoder(vocab_inp_size, embedding_dim, units, BATCH_SIZE)

    # sample input
    sample_hidden = encoder.initialize_hidden_state()
    sample_output, sample_hidden = encoder(example_input_batch, sample_hidden)
    attention_layer = m.BahdanauAttention(10)
    attention_result, attention_weights = attention_layer(sample_hidden, sample_output)

    decoder = m.Decoder(vocab_tar_size, embedding_dim, units, BATCH_SIZE)

    sample_decoder_output, _, _ = decoder(tf.random.uniform((BATCH_SIZE, 1)), sample_hidden, sample_output)

    optimizer = tf.keras.optimizers.Adam()
    loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True, reduction='none')
    checkpoint_dir = './training_checkpoints'
    checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
    checkpoint = tf.train.Checkpoint(optimizer=optimizer,
                                    encoder=encoder,
                                    decoder=decoder)
    checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))



    input = list()
    with open(input_file, 'r', encoding ='utf-8') as f:
        for i in f:
            input.append(i.strip())
    Ngan = pd.read_excel("./data/Ngan.xlsx", header = None, dtype=str)
    dictionary = {}
    for i in range(len(Ngan)):
        dictionary[Ngan.iloc[i, 0].strip()] = Ngan.iloc[i, 1].strip()
    viet_tat=set()
    am_giua = set()
    with open('./data/am_giua.txt','r', encoding='utf-8') as f:
        for i in f:
            am_giua.add(i.strip())
    with open("./data/viet_tat.txt", "r", encoding='utf-8') as f:
        for i in f:
            viet_tat.add(i.strip().lower())
    output = list()


    for question in input:
        question = heuristic_data(question)
        Word_Q = question.split()
        question = question.lower()
        word_q = question.split()
        n_word = len(word_q)
        for i in range(n_word):
            vcl = word_q[i]
            if check_dial(word_q[i]):
                if not check_spell(word_q[i], am_giua, viet_tat):
                    temp = convert_word(word_q[i])
                    answer = evaluate(temp)
                    answer = answer.replace('<start>', '')
                    answer = answer.replace('<end>', '')
                    answer = answer.replace(' ', '')
                    answer = answer.strip()
                    if len(answer) > len(word_q[i]) + 5:
                        vcl = answer[:len(word_q[i])]
                    else:
                        vcl = answer
            if Word_Q[i].isupper():
                word_q[i] = vcl.upper()
            elif Word_Q[i][0].isupper():
                word_q[i] = vcl[0].upper() + vcl[1:]
            else:
                word_q[i] = vcl
        answer = ' '.join(word_q)
        output.append(answer)
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in output:
            f.write("%s\n" % item)