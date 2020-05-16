import nltk
import re
import random
import wikipedia as wk

nltk.download('words')
nltk.download('punkt')

from nltk.corpus import words
from spellchecker import SpellChecker
from nltk.chat.util import reflections

spell = SpellChecker()
def spellCheck(ip_str):
  tokens = nltk.word_tokenize(ip_str)
  correction=''
  misspelled = spell.unknown(tokens)
  if len(misspelled)>0:
    print("CB> I tried to correct your misplet words to best of my ability")
  for word in misspelled:
    # Get the one `most likely` answer
    print("The most probable word is "+spell.correction(word))
    correction = spell.correction(word)
    # Get a list of `likely` options
    print("The list of correct words you wanted to type maybe from:")
    print(spell.candidates(word))
  return correction
  
class Chat(object):
    def __init__(self, pairs, reflections={}):
        self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
        self._reflections = reflections
        self._regex = self._compile_reflections()

    def _compile_reflections(self):
        sorted_refl = sorted(self._reflections, key=len, reverse=True)
        return re.compile(
            r"\b({0})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE
        )

    def _substitute(self, str):
      return self._regex.sub(
            lambda mo: self._reflections[mo.string[mo.start() : mo.end()]], str.lower()
        )
    def _wildcards(self, response, match):
        pos = response.find("%")
        while pos >= 0:
            num = int(response[pos + 1 : pos + 2])
            response = (
                response[:pos]
                + self._substitute(match.group(num))
                + response[pos + 2 :]
            )
            pos = response.find("%")
        return response

    def wikipedia_data(self, input):
      reg_ex = re.search('tell me about (.*)', input)
      try:
        if reg_ex:
            topic = reg_ex.group(1)
            topic1 = spellCheck(topic)
            if len(topic1)>0:
                #print('Wiki search was done on '+wk.suggest(topic1))
                print("Wiki search was done on "+topic1)
                wiki = wk.summary(topic1, sentences = 3)
                return wiki
            else:
              #print('Wiki search was done on '+wk.suggest(topic))
              wiki = wk.summary(topic, sentences = 3)
              return wiki
      except Exception as e:
            print("No content has been found")
        
    def respond(self, str):
      for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)  # pick a random response
                resp = self._wildcards(resp, match)  # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == "?.":
                    resp = resp[:-2] + "."
                if resp[-2:] == "??":
                    resp = resp[:-2] + "?"
                return resp


    def converse(self, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try:
                user_input = input("You>")
            except EOFError:
                print(user_input)
            if "tell me about" in user_input:
                #spell_checker(user_input)
                print(self.wikipedia_data(user_input))
            else:
                while user_input[-1] in "!.":
                    user_input = user_input[:-1]
                spellCheck(user_input)
                print("CB> ",self.respond(user_input))
    
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today ?",]
    ],
     [
        r"what is your name ?",
        ["My name is Chatty and I'm a chatbot ?",]
    ],
    [
        r"how are you ?",
        ["I'm doing good\nHow about You ?",]
    ],
    [
        r"sorry (.*)",
        ["Its alright","Its OK, never mind",]
    ],
    [
        r"i (.*) (good|great|well|fine)",
        ["Nice to hear that","Alright :)",]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there", "Hi, I am glad that you are talking to me"]
    ],
    [
        r"(.*) age?",
        ["I'm a computer program dude\nSeriously you are asking me this?",]
        
    ],
    [
        r"what (.*) want ?",
        ["Make me an offer I can't refuse",]
        
    ],
    [
        r"(.*) created ?",
        ["Prajnya created me using Python's NLTK library ","top secret ;)",]
    ],
    [
        r"(.*) (location|city) ?",
        ['Riverside, California',]
    ],
    [
        r"(.*) weather in (.*)?",
        ["Weather in %2 is awesome like always","Too hot man here in %2","Unpredictible weather man here in %2"]
    ],
    [
        r"i work in (.*)?",
        ["%1 is an Amazing company, I have heard about it. But they are in huge loss these days.",]
    ],
[
        r"(.*)raining in (.*)",
        ["No rain since last week here in %2","Damn its raining too much here in %2"]
    ],
    [
        r"how (.*) health(.*)",
        ["I'm a computer program, so I'm always healthy ",]
    ],
    [
        r"(.*) (sports|game) ?",
        ["I'm a very big fan of Football",]
    ],
    [
        r"who (.*) (moviestar|actor)?",
        ["Brad Pitt"]
],
    [
        r"quit",
        ["Bye take care. See you soon :) ","It was nice talking to you. See you soon :)"]
],
[
        r"bye",
        ["Not so soon","Are you sure you want to leave me?","Type 'quit' to end this chat"]
],
[
        r"thank you",
        ["You are welcome :)", "I am glad that I could help you!"]
],
  [
        r".*",
        ["I did not understand you. Can you repeat your question?"]
  ],

]
def chatty():
        print("CB> Hi, I'm Chatty and I chat alot ;) \nPlease type lowercase English language to start a conversation. Type quit to leave. \nIf you want answers from wikipedia, start your query with 'tell me about' ")
        chat = Chat(pairs, reflections)
        chat.converse()
        

if __name__ == "__main__":
    chatty()
