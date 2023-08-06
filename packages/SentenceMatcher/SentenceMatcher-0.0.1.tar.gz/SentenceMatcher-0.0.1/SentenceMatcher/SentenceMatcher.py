def SentenceMatch(to_be_matched, list_to_match_against):
    sentences_original = list_to_match_against
    userin = to_be_matched
    sentences = sentences_original.copy()
    symbols = ['!', '?', ';', ',', '.', '/', '(', ')', '\'', '"']

    for i, sentence in enumerate(sentences):
        sentences[i] = sentence.split()

    for i, sentence in enumerate(sentences):
        for j, word in enumerate(sentence):
            word = word.lower()
            word = [*word]
            purified_word = [ch for ch in word if not ch in symbols]
            word = ""
            for ch in purified_word:
                word += ch
            sentence[j] = word
        sentences[i] = sentence

    sentences = [[' '.join(sentence)] for sentence in sentences]

    wordlist = []
    for sentence in sentences:
        sentence = sentence[0].split()
        for word in sentence:
            wordlist.append(word)

    wordlist = sorted(set(wordlist))

    binary_lists = []
    for sentence in sentences:
        sentence_binary = [0] * len(wordlist)
        sentence = sentence[0].split()
        for i, word in enumerate(wordlist):
            if word in sentence:
                sentence_binary[i] = 1
            else:
                sentence_binary[i] = 0

        binary_lists.append(sentence_binary)

    userin = userin.split()
    for i, word in enumerate(userin):
        word = word.lower()
        word = [*word]
        purified_word = []
        purified_word = [ch for ch in word if not ch in symbols]
        word = ""
        for ch in purified_word:
            word += ch
        userin[i] = word

    userin_binary = [0] * len(wordlist)
    for i, word in enumerate(wordlist):
        if word in userin:
            userin_binary[i] = 1
        else:
            userin_binary[i] = 0
        
    percentage_accrs = []
    for j, binary_list in enumerate(binary_lists):
        score_for_current_sentence = 0
        for i in range(len(binary_list)):
            if binary_list[i] == 1 and userin_binary[i] == 1:
                score_for_current_sentence += 1
        len_of_user_in = len(userin)
        percentage_accr = (score_for_current_sentence/len_of_user_in) * 100
        percentage_accrs.append(percentage_accr)

    max_accr = 0.0
    for accr in percentage_accrs:
        if accr > max_accr:
            max_accr = accr

    index_of_sentence_with_max_accr = percentage_accrs.index(max_accr)
    output = sentences_original[index_of_sentence_with_max_accr]

    max_accr = "%.1f" % max_accr
    return output, max_accr




new_list_of_sentences = ["Hey there!", "How're you?", "How's your day going?", "So tell me about yourself please!"]
new_sentence = "Please tell me about you."

output, new_accr = SentenceMatch(new_sentence, new_list_of_sentences)
print("Closest Match:", output)
print("Accuracy:", new_accr)