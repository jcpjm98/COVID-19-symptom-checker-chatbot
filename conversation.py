import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer ()

import numpy
import tflearn
import tensorflow
import random
import json

with open("intents.json") as file:
    data = json.load(file)
    
words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(pattern)
        docs_y.append(intent["tag"])
        
    if intent["tag"] not in labels:
        labels.append(intent["tag"])
        
words = [stemmer.stem(w.lower()) for w in words]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []
    
    wrds = [stemmer.stem(w) for w in doc]
    
    for w in words:
        if w in wrds: 
            bag.append(1)
        else:
            bag.append(0)
   
    output_row = list(out_empty[:]
    output_row[labels.index(docs_y[x])] = 1
                      
    training.append(bag)
    output.append(output_row)
                      
training = numpy.array(training)
output = np.array(output)

        

sex_norm = {
    'male': 'male',
    'm': 'male',
    'man': 'male',
    'female': 'female',
    'f': 'female',
    'woman': 'female',
}


answer_norm = {
    'yes': 'present',
    'y': 'present',
    'present': 'present',
    'no': 'absent',
    'n': 'absent',
    'absent': 'absent',
    '?': 'unknown',
    'skip': 'unknown',
    'unknown': 'unknown',
    'dont know': 'unknown',
    'don\'t know': 'unknown',
}


modality_symbol = {'present': '+', 'absent': '-', 'unknown': '?'}


def read_input(prompt):
    if prompt.endswith('?'):
        prompt = prompt + ' '
    else:
        prompt = prompt + ': '
    print(prompt, end='', flush=True)
    return sys.stdin.readline().strip()


def read_age_sex():
    """Primitive routine for reading age and sex specification such as "30 male".
    This is very crude. This is because reading answers to simple questions is not the main scope of this
    example. In real chatbots, either use some real intent+slot recogniser such as snips_nlu,
    or at least write a number of regular expressions to capture most typical patterns for a given language.
    Also, age below 12 should be rejected as our current knowledge doesn't support paediatrics
    (it's being developed but not delivered yet)."""
    agesex = read_input('Patient age and sex (e.g., 30 male)')
    age, sex = agesex.split()
    return int(age), sex_norm[sex.lower()]


def mention_as_text(mention):
    """Represent the given mention structure as simple textual summary."""
    name = mention['name']
    symbol = modality_symbol[mention['choice_id']]
    return '{}{}'.format(symbol, name)


def context_from_mentions(mentions):
    return [m['id'] for m in mentions if m['choice_id'] == 'present']


def summarise_mentions(mentions):
    print('Noting: {}'.format(', '.join(mention_as_text(m) for m in mentions)))


def read_complaints(auth_string, case_id, language_model=None):
    """Keep reading complaint-describing messages from user until empty message read (or just read the story if given).
    Will call the /parse endpoint and return mentions captured there."""
    mentions = []
    context = []  # a list of ids of present symptoms in the order of reporting
    while True:
        portion = read_complaint_portion(auth_string, case_id, context, language_model=language_model)
        if portion:
            summarise_mentions(portion)
            mentions.extend(portion)
            # remember the mentions understood as context for next /parse calls
            context.extend(context_from_mentions(portion))
        if mentions and portion is None:
            # user said there's nothing more but we've already got at least one complaint
            return mentions


def read_single_question_answer(question_text):
    """Primitive implementation of understanding user's answer to a single-choice question.
    Prompt the user with question text, read user's input and convert it to one of the expected
    evidence statuses: present, absent or unknown. Return None if no answer provided."""
    answer = read_input(question_text)
    if not answer:
        return None
    return answer_norm[answer]


def conduct_interview(evidence, age, sex, case_id, auth, language_model=None):
    """Keep asking questions until API tells us to stop or the user gives an empty answer."""
    while True:
        resp = apiaccess.call_diagnosis(evidence, age, sex, case_id, auth, language_model=language_model)
        question_struct = resp['question']
        diagnoses = resp['conditions']
        should_stop_now = resp['should_stop']
        if should_stop_now:
            # triage recommendation must be obtained from a separate endpoint, call it now
            # and return all the information together
            triage_resp = apiaccess.call_triage(evidence, age, sex, case_id, auth, language_model=language_model)
            return evidence, diagnoses, triage_resp
        new_evidence = []
        if question_struct['type'] == 'single':
            # if you're calling /diagnosis in "disable_groups" mode, you'll only get "single" questions
            # these are simple questions that require a simple answer --
            # whether the observation being asked for is present, absent or unknown
            question_items = question_struct['items']
            assert len(question_items) == 1  # this is a single question
            question_item = question_items[0]
            observation_value = read_single_question_answer(question_text=question_struct['text'])
            if observation_value is not None:
                new_evidence.extend(apiaccess.question_answer_to_evidence(question_item, observation_value))
        else:
            # You'd need a rich UI to handle group questions gracefully.
            # There are two types of group questions: "group_single" (radio buttons)
            # and "group_multiple" (a bunch of single questions gathered under one caption).
            # Actually you can try asking sequentially for each question item from "group_multiple" question
            # and then adding the evidence coming from all these answers.
            # For "group_single" there should be only one present answer. It's recommended to include only this chosen
            # answer as present symptom in the new evidence.
            # For more details, please consult:
            # https://developer.infermedica.com/docs/diagnosis#group_single
            raise NotImplementedError('Group questions not handled in this example')
        # important: always update the evidence gathered so far with the new answers
        evidence.extend(new_evidence)


def summarise_some_evidence(evidence, header):
    print(header + ':')
    for idx, piece in enumerate(evidence):
        print('{:2}. {}'.format(idx + 1, mention_as_text(piece)))
    print()


def summarise_all_evidence(evidence):
    reported = []
    answered = []
    for piece in evidence:
        (reported if piece.get('initial') else answered).append(piece)
    summarise_some_evidence(reported, 'Patient complaints')
    summarise_some_evidence(answered, 'Patient answers')


