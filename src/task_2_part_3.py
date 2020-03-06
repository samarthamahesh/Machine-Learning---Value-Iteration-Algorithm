gamma = 0.1
delta = 0.0000000001

SHOOT = 0
DODGE = 1
RECHARGE = 2

MDhealthLen = 5
ArrowLen = 4
StaminaLen = 3

penalty = -2.5

iteration = 0

statespace = [[[0 for i in range(StaminaLen)] for j in range(ArrowLen)] for k in range(MDhealthLen)]
newstatespace = [[[0 for i in range(StaminaLen)] for j in range(ArrowLen)] for k in range(MDhealthLen)]
for i in range(ArrowLen):
    for j in range(StaminaLen):
        statespace[0][i][j] = 10
        newstatespace[0][i][j] = 10

while(1):
    maxDiff = -1
    print("iteration="+str(iteration))
    for i in range(ArrowLen):
        for j in range(StaminaLen):
            print("("+str(0)+","+str(i)+","+str(j)+"):-1=[0.000]")
    for MDhealth in range(1, MDhealthLen):
        for arrow in range(ArrowLen):
            for stamina in range(StaminaLen):
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
                            if stamina == StaminaLen-1:
                                if arrow == ArrowLen-1:
                                    utility = 0.8*statespace[MDhealth][arrow][stamina-1] + 0.2*statespace[MDhealth][arrow][stamina-2]
                                else:
                                    utility = 0.8*0.8*statespace[MDhealth][arrow+1][stamina-1] + 0.8*0.2*statespace[MDhealth][arrow][stamina-1] + 0.2*0.8*statespace[MDhealth][arrow+1][stamina-2] + 0.2*0.2*statespace[MDhealth][arrow][stamina-2]
                            else:
                                if arrow == ArrowLen-1:
                                    utility = statespace[MDhealth][arrow][stamina-1]
                                else:
                                    utility = 0.8*statespace[MDhealth][arrow+1][stamina-1] + 0.2*statespace[MDhealth][arrow][stamina-1]
                            if utility > maxUtility:
                                maxUtility = utility
                                maxAction = "DODGE"
                    elif action == RECHARGE:
                        if stamina == StaminaLen-1:
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
                print("("+str(MDhealth)+","+str(arrow)+","+str(stamina)+"):"+maxAction+"=["+str(round(newUtility, 3))+"]")
    statespace = newstatespace
    iteration += 1
    if maxDiff > delta:
        print("\n\n")
    else:
        break