import requests
import re
import argparse
import sys
import time
from tqdm import tqdm


def iterate_and_find(text):
    lst = []
    all_iterations(lst,text,0,"")
    return lst

def all_iterations(lst, text, i, s):
    if i >= len(text):
        lst.append(s)
        return
    
    currentChar = text[i:i+1]

    if (currentChar == "0"):
        for letter in ["o","O","0"]:
            s += letter
            all_iterations(lst,text,i+1,s)
            s = s[:-1]
        return

    if (currentChar == "1"):
        for letter in ["i","l","L","I","1"]:
            s += letter
            all_iterations(lst,text,i+1,s)
            s = s[:-1]
        return
    s += currentChar
    all_iterations(lst,text,i+1,s)


def get_some_variations(original_list):
    variations = []
    for singleWord in original_list:
        variations.extend(variate(singleWord, '_'))
    lst = [i for i in variations]
    for singleWord in lst:
        variations.extend(variate(singleWord, '.'))

    lst = [i for i in variations]
    for singleWord in lst:
        variations.extend(variate(singleWord, '-'))

    return variations

    


def variate(original_string, char):
    lst = []
    items = [char for char in original_string]
    bits  = len(items) - 1

    for n in range(1, int(2**bits)):
        lst.append(''.join(items[i] + (char if n & (1<<i) else '') for i in range(bits)) + items[-1])


    realLst = []
    for word in lst:
        if (word.count(char) < 2):
            realLst.append(word)
    return realLst


def checkExists(name):
    urlToCheck = "https://pypi.org/project/" + name
    response = requests.get(urlToCheck)
    if (response.status_code == 200):
        print("Taken pypi package name - by " + str(name))
        return True
    return False


def analyze(name):
    superNormalized = (re.sub("[-._]","", re.sub("[iIlL]", "1", re.sub("[oO]", "0", name)))).lower()
    if checkExists(superNormalized):
        print("SORRY, taken by " + superNormalized)
        return
    if checkExists(name.lower()):
        print("SORRY, taken by " + str(name.lower()))
        return
    lst = iterate_and_find(superNormalized)
    

    ans = (get_some_variations(lst))
    found = False
    for i in tqdm(range(0,len(ans)-1), desc ="Progress: "):

        if (checkExists(ans[i])):
            found = True
            break
    if (found):
        print("SORRY ABOUT THAT")
    else:
        print("DID NOT FIND A COLLISION- you **might** be good to go!")


def main():
    parser = argparse.ArgumentParser(
        prog='Package Name CLI',
        description='CLI to quickly determine validity of pypi package name')
    parser.add_argument('-n', '--name',
        help="Name you wish to quickly test") 
    parser.add_argument('-i', '--intense',
                    action='store_true')  # on/off flag
    
    invalidURLs = ["requirements", "requirements.txt", "package_name", "<package_name>", "package-name", "<package-name>"]
    
    parsed = parser.parse_args()
        
    name = parsed.name
    urlToCheck = "https://pypi.org/project/" + name

    pattern = re.compile(r'^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$', re.IGNORECASE)
    if not bool(pattern.match(name)):
        print("Your name does not match the naming conventions. Please see https://packaging.python.org/en/latest/specifications/name-normalization/")
        return

    response = requests.get(urlToCheck)
    if (parser.parse_args().name in invalidURLs):
        print("Invalid pypi package name")
    elif (response.status_code == 200):
        print("Taken pypi package name")
    elif (response.status_code != 404):
        print("Status code: " + str(response.status_code))
    else:
        if not (parsed.intense):
            print("Looks good!")
        else:
            print("Not found through basic measures. Engaging in intense search.")
            time.sleep(.5)
            analyze(name)

if __name__ == "__main__":
    main()