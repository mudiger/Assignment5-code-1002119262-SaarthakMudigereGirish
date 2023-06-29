from flask import request
from flask import Flask
from flask import render_template
import os

import PyPDF2, nltk
from collections import defaultdict
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.stem import snowball
from nltk.corpus import stopwords

# nltk.download_shell()
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


def extract_words_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        words = []
        sentences = []
        for page in reader.pages:
            # page
            text = page.extract_text()
            # sentences
            for sent in sent_tokenize(text):
                # words
                sentences.append(sent)
                word_tokens = word_tokenize(sent)
                words += word_tokens
    return sentences, words


# sentences = sent_tokenize(' '.join(words_list))
# Specify the path to your PDF file
pdf_file_path = r'C:\Users\Saarthak Mudigere\Desktop\Masters\Saarthak\UTA\Semester 2 Summer 2023\Assignment\assignment5\Textbooks\Textbook2.pdf'

# Call the function to extract words from the PDF
words_list = extract_words_from_pdf(pdf_file_path)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/page1/", methods=['GET', 'POST'])
def page1():
    stwords = set(stopwords.words('english'))
    # Using set difference to eliminate stopwords from our words
    stopfree_words = set(words_list[0]) - stwords

    nouns = []
    noun_freq = []
    for sentence in stopfree_words:
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)
        nouns.extend([word for word, pos in tagged_words[1:] if pos.startswith('NN') and word[0].isupper()])

    if request.method == "POST":
        n = int(request.form['n'])

        # Calculate the frequency distribution
        freq_dist = FreqDist(nouns)
        noun_freq = freq_dist.most_common(n)

    return render_template("1)Page.html", noun_freq=noun_freq)


@app.route("/page2/", methods=['GET', 'POST'])
def page2():
    # convert them all to lower case and eliminate duplicates
    lower_corpus_words = set([x.lower() for x in words_list[1]])

    characters = []
    total = 0
    for word in lower_corpus_words:
        for char in word:
            characters.append(char)
    # Calculate the frequency distribution
    letter_freq = FreqDist(characters)
    for letter,count in letter_freq.items():
        total += count

    count_list = []
    if request.method == "POST":
        chars = request.form['chars']
        mult_chars = list(chars)

        for i in mult_chars:
            count = letter_freq[i]
            count_list.append((i, count, round((count/total)*100, 2)))

    return render_template("2)Page.html", count_list=count_list)


@app.route("/page3/", methods=['GET', 'POST'])
def page3():
    # convert them all to lower case and eliminate duplicates
    lower_corpus_words = set([ x.lower() for x in words_list[1]])

    replaced = []
    if request.method == "POST":
        old_char = request.form['chars']
        new_char = request.form['replace']

        modified_tokens = [token.replace(old_char, new_char) for token in words_list[1]]
        modified_contents = ' '.join(modified_tokens)

        # Print the top few lines
        num_lines_to_print = 8  # Specify the number of lines to print
        lines = modified_contents.split('. ')  # Split the modified contents into lines
        for line in lines[:num_lines_to_print]:
            replaced.append(('============>', line))
        # # Write the modified contents back to the file
        # with open(pdf_file_path, 'w') as file:
        #     file.write(modified_contents)

    return render_template("3)Page.html", replaced=replaced)


@app.route("/page4/", methods=['GET', 'POST'])
def page4():
    w_in_s = []

    if request.method == "POST":
        n = int(request.form['n'])
        word = request.form['word']

        def search_word_in_sentence(w, s, f):
            tokens = nltk.word_tokenize(s)
            if w in tokens and f>0:
                w_in_s.append(('============>', s))
                return f - 1  # Decrement n by 1 and return the updated value
            return f  # Return n unchanged if the condition is not met

        c = n
        for sentence in words_list[0]:
            c = search_word_in_sentence(word, sentence, c)
            if c == 0:
                break

    return render_template("4)Page.html", w_in_s=w_in_s)


if __name__ == "__main__":
    app.run(debug=True)
#
# corpus = [
#     """
#     So she swallowed one of the cakes and was delighted to find that she
#     began shrinking directly. As soon as she was small enough to get through the door,
#     she ran out of the house and found quite a crowd of little animals and birds waiting outside.
#     They all made a rush at Alice the moment she appeared, but she ran off as hard as
#     she could and soon found herself safe in a thick wood.
#     """,
#     """
#     If two strips of different metals, such as silver and iron, be soldered together
#     at one end, and the other ends be connected with a galvanometer, on heating the
#     soldered junction of the metals it will be found that a current of electricity
#     traverses the circuit from the iron to the silver. If other metals be used,
#     having the same size, and the same degree of heat be applied, the current of
#     electricity thus generated will give a greater or a less deflection, which will be
#     constant for the metals employed. The two metals generally employed are bismuth
#     and antimony, in bars about an inch long and an eighth of an inch square.
#     These are soldered together in series so as to present for faces the ends of the
#     bars, and these often number as many as fifty pairs. Such a series is called a thermo-pile.
#     This method of[25] generating electricity was discovered by Seebeck of Berlin in 1821,
#     but the thermo-pile so much in use now in heat investigations was invented by Nobili in 1835.
#     """,
#     """
#     According to this authority a field testing laboratory will cost for equipment $250 to $350.
#     Such a laboratory can be operated by two or three men at a salary charge of from $100 to $200
#     per month. Two men will test on an average four samples per day and each additional man will
#     test four more samples. The cost of testing will range from $3 to $5 per sample, which
#     is roughly equivalent to 3 cts. per barrel of[Pg 5] cement, or from 3 to 5 cts.per cubic yard
#     of concrete. These figures are for field laboratory work reasonably well conducted
#     under ordinarily favorable conditions. In large laboratories the cost per sample will
#     run somewhat lower.
#     """,
#     """
#     Just then Alice ran across the Duchess (who was now out of prison). She tucked her arm
#     affectionately into Alice's and they walked off together. Alice was very glad to find her in
#     such a pleasant temper. She was a little startled, however, when she heard the voice of the
#     Duchess close to her ear. "You're thinking about something, my dear, and that makes you forget to talk."
#     """,
#     """
#     It was the jackal—Tabaqui, the Dish-licker—and the wolves of India despise Tabaqui because he
#     runs about making mischief, and telling tales, and eating rags and pieces of leather from the
#     village rubbish-heaps. But they are afraid of him too, because Tabaqui, more than
#     anyone else in the jungle, is apt to go mad, and then he forgets that he was ever afraid of
#     anyone, and runs through the forest biting everything in his way. Even the tiger runs and
#     hides when little Tabaqui goes mad, for madness is the most disgraceful thing that can
#     overtake a wild creature. We call it hydrophobia, but they call it dewanee—the madness—and run.
#     """,
#     """
#     A great roofless palace crowned the hill, and the marble of the courtyards and the fountains
#     was split, and stained with red and green, and the very cobblestones in the courtyard where the
#     king’s elephants used to live had been thrust up and apart by grasses and young trees.
#     From the palace you could see the rows and rows of roofless houses that made up the city looking
#     like empty honeycombs filled with blackness; the shapeless block of stone that had been an idol
#     in the square where four roads met; the pits and dimples at street corners where the public wells
#     once stood, and the shattered domes of temples with wild figs sprouting on their sides.
#     The monkeys called the place their city, and pretended to despise the Jungle-People because they
#     lived in the forest. And yet they never knew what the buildings were made for nor how to use them.
#     They would sit in circles on the hall of the king’s council chamber, and scratch for fleas and
#     pretend to be men; or they would run in and out of the roofless houses and collect pieces of plaster
#     and old bricks in a corner, and forget where they had hidden them, and fight and cry in scuffling crowds,
#     and then break off to play up and down the terraces of the king’s garden, where they would shake the
#     rose trees and the oranges in sport to see the fruit and flowers fall. They explored all the passages
#     and dark tunnels in the palace and the hundreds of little dark rooms, but they never remembered what
#     they had seen and what they had not; and so drifted about in ones and twos or crowds telling each
#     other that they were doing as men did. They drank at the tanks and made the water all muddy,
#     and then they fought over it, and then they would all rush together in mobs and shout:
#     "There is no one in the jungle so wise and good and clever and strong and gentle as the Bandar-log."
#     Then all would begin again till they grew tired of the city and went back to the tree-tops,
#     hoping the Jungle-People would notice them.
#     """
# ]
#
#
# # This will contain a list of all words in the corpus
# corpus_words = []
#
# # Tokenize a paragraph into sentences and each sentence in to
# # words
# for c in corpus:
#     for sent in sent_tokenize(c):
#         word_tokens = word_tokenize(sent)
#         corpus_words += word_tokens
#
# print(len(corpus_words))
#
# # convert them all to lower case and eliminate duplicates
# lower_corpus_words = set([ x.lower() for x in corpus_words ])
# print(len(lower_corpus_words))
#
#
# # Remove the stopwords
# from nltk.corpus import stopwords
#
# stwords = set(stopwords.words('english'))
#
# # Using set difference to eliminate stopwords from our words
# stopfree_words = lower_corpus_words - stwords
# len(stopfree_words)
#
# # grammar tense
# stemmer = snowball.SnowballStemmer('english')
# stemmed_words = set([stemmer.stem(x) for x in stopfree_words])
# print(stemmed_words)
#
#
# # Our index is a map of word -> documents it is found in
# inverted_index = defaultdict(set)
#
# # We maintain the reference to the document by its index in the corpus list
# for docid, c in enumerate(corpus):
#     for sent in sent_tokenize(c):
#         for word in word_tokenize(sent):
#             word_lower = word.lower()
#             if word_lower not in stwords:
#                 word_stem = stemmer.stem(word_lower)
#                 # We add the document to the set againt the word in our
#                 # index
#                 inverted_index[word_stem].add(docid)
#
# print(sorted(inverted_index.keys()))
#
#
# def process_and_search(query):
#     matched_documents = set()
#     for word in word_tokenize(query):
#         word_lower = word.lower()
#         if word_lower not in stwords:
#             word_stem = stemmer.stem(word_lower)
#             matches = inverted_index.get(word_stem)
#             if matches:
#                 # The operator |= is a short hand for set union
#                 matched_documents |= matches
#     return matched_documents
#
# print(len(process_and_search("alice")))