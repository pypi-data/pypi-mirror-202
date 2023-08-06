import random
import os
from termcolor import colored
from PIL import Image
import pyttsx3
import speech_recognition as speach
import webbrowser
import time
from datetime import datetime
import sys

now = datetime.now()


def wait(seconds, pos=0):
    multiply = [1, 60, 3600, 86400]
    time.sleep(seconds*multiply[pos])


def times():
    return time.time()


def time_now():
    return now.strftime("%H:%M:%S")


def second_now():
    return now.strftime("%S")


def minute_now():
    return now.strftime("%M")


def hour_now():
    return now.strftime("%H")


def date_now():
    return now.strftime("%d/%m/%Y")


def day_now():
    return now.strftime("%d")


def month_now():
    return now.strftime("%m")


def year_now():
    return now.strftime("%Y")


speech = pyttsx3.init()


def textToSpeach(text="", volume=50, voiceId=0, rate=125):
    volume = volume/100
    speech.setProperty('rate', rate)
    speech.setProperty('volume', volume)
    voices = speech.getProperty('voices')
    speech.setProperty('voice', voices[voiceId].id)
    speech.say(text)
    speech.runAndWait()


def speechToText(error=0):

    recog = speach.Recognizer()

    with speach.Microphone() as source:
        recog.adjust_for_ambient_noise(source)
        audio = recog.listen(source)
        try:
            return recog.recognize_google(audio)

        except Exception as e:
            if error == 1:
                return str(e)
            else:
                return "error"


def searchOnWeb(a):
    url1 = ""
    for letter in a:
        if letter == " ":
            url1 += "+"
        elif letter == "+":
            url1 += "%2B"
        elif letter == "/":
            url1 += "%2F"
        else:
            url1 += letter
    url = f"https://www.google.com/search?q={url1}"
    webbrowser.open(url)


def randomNumber(minimum=0, maximum=9, times=1):
    if times == 1:
        return random.randint(minimum, maximum)
    elif times < 1:
        return None
    else:
        result = []
        count = 0
        while count < times:
            random_number = random.randint(minimum, maximum)
            result.append(random_number)
            count += 1
        return result


def randomLetters(lower=1, upper=1, sign=0, times=1):
    lower_L = "qwertyuiopasdfghjklzxcvbnm"
    upper_L = "QWERTYUIOPASDFGHJKLZXCVBNM"
    sign_L = "!#$%&/()=[]}{«»~^+*¨|:.;,-_<>"
    letters = ""
    if lower == 1:
        letters += lower_L
    if upper == 1:
        letters += upper_L
    if sign == 1:
        letters += sign_L
    max_lenth = len(letters) - 1
    if times == 1:
        max_lenth = len(letters) - 1
        ran_num = random.randint(0, max_lenth)
        result = letters[ran_num]

    elif times < 1:
        result = None
    else:
        count = 0
        result = []
        while count < times:
            ran_num = random.randint(0, max_lenth)
            ran_let = letters[ran_num]
            result.append(ran_let)
            count += 1
    return result


def randomChoice(listForRandomChoice):
    lenth = len(listForRandomChoice)
    if lenth == 1:
        return listForRandomChoice[0]
    elif lenth < 1:
        return None
    elif lenth == 2:
        return random.choice(listForRandomChoice)
    else:
        return random.choices(listForRandomChoice)[0]


def onPosition(toPositionList,  position=0):
    return toPositionList[position]


def fromPositionToPosition(positionList, start=0, end=0):
    return positionList[start:end]


def fromPositionToEnd(positionList, start=0):
    return positionList[start::]


def fromStartToPosition(positionList, end=0):
    return positionList[0:end+1]


def addOnList(List, value):
    List.append(value)
    return List


def setOnList(List, position, value):
    List[position] = value
    return List


def addOnListOnPosition(List, position, value):
    List.insert(position, value)
    return List


def removeFromPositionOnList(List, position=0):
    List.pop(position)
    return List


def removeFromList(List, value):
    List.remove(value)
    return List


def clearList(List):
    List.clear()
    return List


def findOnDictionary(Dictionary, name):
    return Dictionary[name]


def setValueOnDictionary(Dictionary, name, value):
    dictionary = Dictionary.update({name: value})
    return dictionary


def addValueOnDictionary(Dictionary, name, value):
    dictionary = Dictionary[name] = value
    return dictionary


def removeValueOnDictionary(Dictionary, name):
    dictionary = Dictionary.pop(name)
    return dictionary


def clearDictionary(Dictionary):
    dictionary = Dictionary.clear()
    return dictionary


def rotateImage(image, save_as="dont_save", rotate=0):
    images = Image.open(image)
    images_r = images.rotate(60)
    images_r.show()
    if save_as != "dont_save":
        images_r.save(save_as)


def cropImage(image, save_as="dont_save", Top=0, Bottom=0, Left=0, Right=0):
    images = Image.open(image)
    image_f = images.crop((Left, Top, Right, Bottom))
    image_f.show()
    if save_as != "dont_save":
        image_f.save(save_as)


def flipImage(image, save_as="dont_save", flip=0):
    images = Image.open(image)
    if flip == 0 or flip == 1:
        if flip == 0:
            images = images.transpose(Image.FLIP_LEFT_RIGHT)
        elif flip == 1:
            images = images.transpose(Image.FLIP_TOP_BOTTOM)
        images.show()
        if save_as != "dont_save":
            images.save(save_as)


def resizeImage(image, save_as="dont_save", width=0, height=0):
    if width != 0 and height != 0:
        images = Image.open(image)
        images_r = images.resize((width, height))
        images_r.show()
        if save_as != "dont_save":
            images_r.save(save_as)


def isEqualTo(a, b):
    if a == b:
        return True
    else:
        return False


def isNotEqualTo(a, b):
    if a != b:
        return True
    else:
        return False


def isLowerThan(a, b):
    if a < b:
        return True
    else:
        return False


def isGreaterThan(a, b):
    if a > b:
        return True
    else:
        return False


def isIn(item, a):
    if item in a:
        return True
    else:
        return False


def isNotIn(item, a):
    if item not in a:
        return True
    else:
        return False


def isLowerOrEqualTo(a, b):
    if a <= b:
        return True
    else:
        return False


def isGreaterOrEqualTo(a, b):
    if a >= b:
        return True
    else:
        return False


def checkA_And_B(a, b):
    if a and b:
        return True
    else:
        return False


def checkA_Or_B(a, b):
    if a or b:
        return True
    else:
        return False


def checkNeitherA_NeitherB(a, b):
    if not a and not b:
        return True
    else:
        return False


def checkOnlyA_or_OnlyB(a, b):
    if a and not b or b and not a:
        return True
    else:
        return False


def calculate(calculation=""):
    error = False
    all_operations = "+-*/"
    all_number = "1234567890."
    all_digit = all_operations+all_number
    if calculation == "":
        return "0"
    else:
        operations = ""
        for digit in calculation:
            if digit not in all_digit:
                error = True
        if error:
            return "error"
        else:
            calculation2 = ""
            for operator in calculation:
                if operator in all_operations:
                    operations += operator + " "
                    calculation2 += " "
                else:
                    calculation2 += operator
            calculation2 = calculation2.split(" ")
            operations2 = operations.split(" ")
            if "" in calculation2:
                calculation2.remove("")
            if "" in operations2:
                operations2.remove("")
            operating = 0
            operations3 = []
            if len(calculation2)-1 == len(operations2):
                for now_All_operator in operations2:
                    if now_All_operator == "*":
                        calculation2[operating] = str(float(calculation2[operating])*float(calculation2[operating+1]))
                        calculation2.pop(operating+1)
                        operating -= 1
                    elif now_All_operator == "/":
                        calculation2[operating] = str(float(calculation2[operating]) / float(calculation2[operating + 1]))
                        calculation2.pop(operating+1)
                        operating -= 1
                    else:
                        operations3.append(now_All_operator)
                    operating += 1
                operating = 0
                for now_All_operator in operations3:
                    if now_All_operator == "+":
                        calculation2[operating] = str(float(calculation2[operating])+float(calculation2[operating+1]))
                        calculation2.pop(operating+1)
                        operating -= 1
                    elif now_All_operator == "-":
                        calculation2[operating] = str(float(calculation2[operating]) - float(calculation2[operating + 1]))
                        calculation2.pop(operating+1)
                        operating -= 1
                    operating += 1
                return calculation2[0]
            else:
                return "error"


def userInput(prompt=""):
    user = input(prompt)
    return user


def inputNumber(prompt=""):
    user = int(input(prompt))
    return user


def inputDecimal(prompt=""):
    user = float(input(prompt))
    return user


def inputBool(prompt=""):
    user = bool(input(prompt))
    return user


def output(result=""):
    print(result)


def outputLower(result=""):
    print(result.lower())


def outputUpper(result=""):
    print(result.upper())


def toLetter(result):
    return str(result)


def toLower(result=""):
    return result.lower()


def toUpper(result=""):
    return result.upper()


def toNumber(result="", a=0):
    if a == 0:
        return int(result)
    else:
        if "." in result:
            return float(result)
        else:
            return int(result)


def toDecimal(result=""):
    return float(result)


def toBool(result=""):
    return result


def Type(result):
    type1 = str(type(result))
    if type1 == "<class 'str'>":
        return "Letter"
    elif type1 == "<class 'int'>":
        return "Number"
    elif type1 == "<class 'float'>":
        return "Decimal"
    elif type1 == "<class 'bool'>":
        return "Boolean"
    elif type1 == "<class 'list'>":
        return "List"
    elif type1 == "<class 'dict'>":
        return "Dictionary"
    elif type1 == "<class 'tuple'>":
        return "Tuple"
    else:
        return type1


def outputInSameLine(result="", end=""):
    print(result, end=end)


def re_output(result=""):
    result = str(result)
    sys.stdout.write('\r' + result)


def clear():
    os.system('CLS')


def outputColor(text="", colour="white"):
    print(colored(text, colour))


def changeTextColor(text="", colour="white"):
    return colored(text, colour)


def Bot(ask="", talk=0, allowSearch=0, microphone=0):
    greeting = ["Hello", "Hi"]
    greeting_ask = ["hello", "hi"]
    user_main_question = ["who are you", "what is your name"]
    user_main_question_answer = ["I am here to help you", "I am a Bot", "I am assistant", "I am your assistant"]
    user_main_question_answer2 = ["if you have any question please ask me", "nice to meet you", "it is my pleasure",
                                  "tell me if you have any question"]
    user_main_question_answer3 = ["I might not be able to answer to all of your question",
                                  "Sorry if my answer arent what you were you looking for..."]
    greeting_question = ["how are you", "I am here to help you", "nice to meet you"]
    user_greeting_question = ["how are you", "nice to meet you"]
    microphone1 = ["You microphone is turned off, ", "Microphone is off, "]
    microphone2 = ["Please turn it on", "Can not listen to you"]
    error1 = ["I am a Bot, ", ""]
    error2 = ["I am trained to answer to your question ", "I am programmed to respond to you ",
              "I am here to help you to answer to your question "]
    error3 = ["but i cant answer to all of them.", "but i am not able to answer to all of them."]
    error4 = ["I try my best to answer them", "Sorry but i am not able to answer to this question"]

    ask = ask.lower()
    result = ""
    if ask == "microphone" and microphone == 1:
        print("Listening...")
        ask = speechToText()
    elif ask == "microphone" and microphone == 0:
        result = f"{random.choice(microphone1)}{random.choice(microphone2)}"
    if ask in greeting_ask:
        result = f"{random.choice(greeting)}, {random.choices(greeting_question)[0]}"
    elif ask in user_main_question:
        result = f"{random.choices(user_main_question_answer)[0]}, {random.choices(user_main_question_answer2)[0]}. {random.choices(user_main_question_answer3)[0]}"
    elif ask[0:9] == "calculate":
        result = calculate(ask[10::])
    elif ask[0:6] == "search":
        if allowSearch == 1:
            searchOnWeb(ask[7::])
        else:
            result = "Sorry cannot open browser"
    else:
        return f"{random.choice(error1)}{random.choices(error2)[0]}{random.choice(error3)}{random.choice(error4)}"

    if talk == 1:
        textToSpeach(result, 100, 1, 125)

    return result


def easyPyLan():
    print("Thanks For Using my library")