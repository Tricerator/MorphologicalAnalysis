#!/usr/bin/python

myDict = {}
dictCounts = {}


def parseFile(fileName):
    verbs = {}
    nouns = {}
    adverbs = {}
    adjectives = {}
    rest = {}

    finalDict = {}

    with open(fileName) as file_in:
        for line in file_in:
            if len(line) > 0:
                words = line.replace('\n', '').split("\t")

                #  eliminuji prazdne radky
                if len(words) != 2:
                    continue
                # Z povahy nemciny neprovedu prevod na mala pismena, vsechna podsatna jmena zacinaji v. pismenem

                lowerWord = words[0].lower()

                if lowerWord in myDict:
                    dictCounts[lowerWord] = dictCounts[lowerWord] + 1
                    if words[1] not in myDict[lowerWord]:
                        myDict[lowerWord].append(words[1])
                else:
                    dictCounts[lowerWord] = 1
                    myDict[lowerWord] = [words[1]]

                category = words[1].split("|")
                if category[0] == "VERB":
                    if not (lowerWord in verbs):
                        verbs[lowerWord] = [words[1]]
                    else:
                        if not (words[1] in verbs[lowerWord]):
                            verbs[lowerWord].append(words[1])
                elif category[0] == "NOUN":
                    if not (lowerWord in nouns):
                        nouns[lowerWord] = [words[1]]
                    else:
                        if not (words[1] in nouns[lowerWord]):
                            nouns[lowerWord].append(words[1])
                elif category[0] == "ADV":
                    if not (lowerWord in adverbs):
                        adverbs[lowerWord] = [words[1]]
                    else:
                        if not (words[1] in adverbs[lowerWord]):
                            adverbs[lowerWord].append(words[1])
                elif category[0] == "ADJ":
                    if not (lowerWord in adjectives):
                        adjectives[lowerWord] = [words[1]]
                    else:
                        if not (words[1] in adjectives[lowerWord]):
                            adjectives[lowerWord].append(words[1])
                else:
                    if not (lowerWord in rest):
                        rest[lowerWord] = [words[1]]
                    else:
                        if not (words[1] in rest[lowerWord]):
                            rest[lowerWord].append(words[1])

    workWithAdverbs(adverbs)
    workWithNouns(nouns)
    workWithVerbs(verbs)
    workWithAdjectives(adjectives)

    finalDict = adverbs
    for i in nouns:
        if i in finalDict:
            for j in nouns[i]:
                finalDict[i].append(j)
        else:
           finalDict[i] = nouns[i]
    for i in verbs:
        if i in finalDict:
            for j in verbs[i]:
                finalDict[i].append(j)
        else:
           finalDict[i] = verbs[i]
    for i in adjectives:
        if i in finalDict:
            for j in adjectives[i]:
                finalDict[i].append(j)
        else:
           finalDict[i] = adjectives[i]

    f = open("../lexicon.txt", "w+")
    for i in finalDict:
        f.write(i + "\t\n")
        for j in finalDict[i]:
           f.write("\t" + j +"\n")

def workWithVerbs(dictVerbs):
    verbs = dictVerbs
    for word in verbs:
        found = False
        for pref in ["ver", "ge", "be", "er", "ent", "emp", "zer"]:
            if word.startswith(pref) and len(word) > 5:
                found = True
                verbs[word] = [item + "|pref=insepar" for item in verbs[word]]
                break
        if found:
            continue
        for pref in ["ab", "an", "auf", "aus", "bei", "mit", "nach", "statt", "vor", "zu", "fort", "los", "nieder",
                     "vorbei", "weg", "zurück", "zusammen"]:
            if word.startswith(pref):
                found = True
                verbs[word] = [item + "|pref=separ" for item in verbs[word]]
                break

    return verbs


def workWithNouns(dictNouns):


    nouns = dictNouns
    for i in nouns:
        for j in nouns[i]:
            if "Case=Nom" in j and j.endswith("Sing") and "PlType" not in i:
                if i + "s" in nouns:
                    nouns[i] = [item + "|PlType=s" for item in nouns[i]]
                    nouns[i + "s"] = [item + "|PlType=s" for item in nouns[i + "s"]]
                    break
                elif i + "en" in nouns:
                    nouns[i] = [item + "|PlType=en" for item in nouns[i]]
                    nouns[i + "en"] = [item + "|PlType=en" for item in nouns[i + "en"]]
                    break
                elif i + "e" in nouns:
                    nouns[i] = [item + "|PlType=e" for item in nouns[i]]
                    nouns[i + "e"] = [item + "|PlType=e" for item in nouns[i + "e"]]
                    break
                elif i + "er" in nouns:
                    nouns[i] = [item + "|PlType=er" for item in nouns[i]]
                    nouns[i + "er"] = [item + "|PlType=er" for item in nouns[i + "er"]]
                    break
                elif i + "n" in nouns:
                    nouns[i] = [item + "|PlType=n" for item in nouns[i]]
                    nouns[i + "n"] = [item + "|PlType=n" for item in nouns[i + "n"]]
                    break

    return nouns


def workWithAdjectives(dictAdjectives):
    adjectives = dictAdjectives

    return adjectives


def workWithAdverbs(dictAdverbs):
    adverbs = dictAdverbs

    for i in adverbs:

        if i.endswith("erweise"):
            adverbs[i] = [item + "|type=Gen" for item in adverbs[i]]
    return adverbs


def printDict(someDict):
    for i in someDict:
        print(str(i) + "\t" + str(someDict[i]))


parseFile("de-tagged.txt")
