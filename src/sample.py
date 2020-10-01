team = 56
gamma = 0.1
delta = 0.0000000001

SHOOT = 0
DODGE = 1
RECHARGE = 2

MDhealthRange = 2
ArrowRange = 2
StaminaRange = 2

arr = [0.5, 1, 2]
Y = arr[team % 3]
penalty = -10 / Y
penalty = -2.5

iteration = 0

statespace = [[[0 for i in range(StaminaRange)] for j in range(ArrowRange)] for k in range(MDhealthRange)]
newstatespace = [[[0 for i in range(StaminaRange)] for j in range(ArrowRange)] for k in range(MDhealthRange)]

while(1):
    maxDiff = -1
    if iteration == 15:
        break
    print("iteration="+str(iteration))
    for MDhealth in range(1, MDhealthRange):
        for arrow in range(ArrowRange):
            for stamina in range(StaminaRange):
                maxUtility = -100000
                maxAction = ''
                for action in range(3):
                    if action == SHOOT:
                        if arrow == 0 or stamina == 0:
                            continue
                        else:
                            utility = 0.5*statespace[MDhealth-1][arrow-1][stamina-1] + 0.5*statespace[MDhealth][arrow-1][stamina-1]
                            if utility > maxUtility:
                                maxUtility = utility
                                maxAction = "SHOOT"
                    elif action == DODGE:
                        if stamina == 0:
                            continue
                        else:
                            if stamina == StaminaRange-1:
                                if arrow == ArrowRange-1:
                                    utility = 0.8*statespace[MDhealth][arrow][stamina-1] + 0.2*statespace[MDhealth][arrow][stamina-2]
                                else:
                                    utility = 0.8*0.8*statespace[MDhealth][arrow+1][stamina-1] + 0.8*0.2*statespace[MDhealth][arrow][stamina-1] + 0.2*0.8*statespace[MDhealth][arrow+1][stamina-2] + 0.2*0.2*statespace[MDhealth][arrow][stamina-2]
                            else:
                                if arrow == ArrowRange-1:
                                    utility = statespace[MDhealth][arrow][stamina-1]
                                else:
                                    utility = 0.8*statespace[MDhealth][arrow+1][stamina-1] + 0.2*statespace[MDhealth][arrow][stamina-1]
                            if utility > maxUtility:
                                maxUtility = utility
                                maxAction = "DODGE"
                    elif action == RECHARGE:
                        if stamina == StaminaRange-1:
                            utility = statespace[MDhealth][arrow][stamina]
                        else:
                            utility = 0.8*statespace[MDhealth][arrow][stamina+1] + 0.2*statespace[MDhealth][arrow][stamina]
                        if utility > maxUtility:
                            maxUtility = utility
                            maxAction = "RECHARGE"
                newUtility = penalty + gamma * maxUtility
                if abs(newUtility - statespace[MDhealth][arrow][stamina]) > maxDiff:
                    maxDiff = abs(newUtility - statespace[MDhealth][arrow][stamina])
                newstatespace[MDhealth][arrow][stamina] = newUtility
                print("("+str(MDhealth)+","+str(arrow)+","+str(stamina)+"):"+maxAction+"=["+str(newUtility)+"]")
    statespace = newstatespace
    iteration += 1
    if maxDiff >= delta:
        print("\n\n")
