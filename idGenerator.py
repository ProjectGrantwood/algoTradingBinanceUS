def idAlphabet(increment, abc, offset = 0):
    num = offset
    while True:
        if num >= len(abc):
            num = num % len(abc)
        hexnum = str(hex(num))
        yieldValue = abc[num]
        for i in range(2, len(hexnum)):
            yieldValue += hexnum[i]
        yield yieldValue
        num += increment
        

def id():
    abc = 'FibonaccididnotmindthatthelastdayoftheyearhappenedtooccuronaTuesdaythoughthebrilliantarithmeticianwasconcernedaboutthefactthateverbodyincludinghisowndearlybelovedcousinAgnesjustplumbforgotabouthisbiglectureattheUniversityofNaplesontheseventeenthorwasittheeighteenthofOctober'
    num = 1
    abcList = [
        idAlphabet(1, abc, 0),
        idAlphabet(2, abc, 1),
        idAlphabet(5, abc, 2),
        idAlphabet(8, abc, 3),
        idAlphabet(13, abc, 5),
        idAlphabet(21, abc, 8),
        idAlphabet(34, abc, 13)
    ]
    while True:
        newId = ''
        for i in range(0, len(abcList)):
            newId += abcList[i].__next__()
        yield newId
        

idGenerator = id()