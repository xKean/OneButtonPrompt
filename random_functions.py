import random
def common_dist(insanitylevel):
    return (random.randint(1, 5)<insanitylevel or insanitylevel >= 10)

def normal_dist(insanitylevel):
    return (random.randint(1, 10)<insanitylevel or insanitylevel >= 10)

def uncommon_dist(insanitylevel):
    return (random.randint(1, 15)<insanitylevel or insanitylevel >= 10)

def rare_dist(insanitylevel):
    roll = (random.randint(1, 30)<insanitylevel or insanitylevel >= 10)
    if(roll):
        print("adding something rare to the prompt")
    return roll

def legendary_dist(insanitylevel):
        roll = (random.randint(1, 50)<insanitylevel)
        if(roll):
            print("Nice! adding something legendary to the prompt")
        return roll

def unique_dist(insanitylevel):
        roll = (random.randint(1, 75)<insanitylevel)
        if(roll):
            print("Critical hit! Something unique has been added to the prompt")
        return roll

def novel_dist(insanitylevel):
        roll = (random.randint(1, 500)<insanitylevel)
        if(roll):
            print("Uh, something novel has been added to the prompt. Interesting.")
        return roll

def generateRandomNegative():
    opt_negative ="ng_deepnegative_v1_75t, "

    if random.random() < .5:
        opt_negative+= "nrealfixer, nfixer,"
    if random.random() < .5:
        opt_negative+= "rmadanegative"

    print("Negativ: "+ opt_negative)
    return opt_negative

def generateRandomModel():
    randNum = random.randrange(5)
    if randNum == 0:
        model = 'colorful_v26'
    elif randNum == 1:
        model = 'lyriel_v14'
    elif randNum == 2:
        model = 'revAnimated_v122'
    elif randNum == 3:
        model = 'rmadaMergeSD21768_v70'
    elif randNum == 4:
        model = 'ultrm_v10'
    else:
        model = 'rmadaMergeSD21768_v70'

    print("Model: "+ model)
    return model

def generateRandomRatio():
    randNum = random.randrange(5)
    if randNum == 0:
        return "portrait"
    elif randNum == 1:
        return "wide"
    elif randNum == 2:
        return "ultrawide"
    elif randNum == 3:
        return "square"
    else:
        return "normal"
