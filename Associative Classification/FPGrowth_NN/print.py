rules = {('Feature (3,) : 0-2', 'Feature (5,) : 1'): (('Feature (9,) : no-recurrence-events',), 0.175, 0.05060145646460862, 0.8333333333333334),
         ('Feature (3,) : 6-8', 'Feature (5,) : 2'): (('Feature (9,) : no-recurrence-events',), 0.025, 0.05060145646460862, 0.8333333333333334),
         ('Feature (2,) : 10-14', 'Feature (3,) : 0-2', 'Feature (5,) : 2'): (('Feature (9,) : no-recurrence-events',), 0.05, 0.04694363908573077, 1.0)}

def extract_features_to_print(rule_features):
    return_str = ""

    for i in range(len(rule_features)):
        f = rule_features[i]
        index = 0
        current = f[9]
        number = ""
        while current != ',':
            number += f[9+index]
            index += 1
            current = f[9+index]

        index = 9+ len(number) + 5
        number = int(number)

        value = ''
        while index < len(f):
            value += f[index]
            index += 1

        return_str += "[Feature "+str(number)+" : "+value+" ],"
    return_str = return_str[:-1]
    return return_str

def printRules(rules):
    counter = 1
    for rule in rules:
        if counter < 51:
            antecedant = rule
            consequent = rules.get(rule)[0]
            ig = rules.get(rule)[1]
            confidence = rules.get(rule)[2]
            support = rules.get(rule)[3]

            ante_str = extract_features_to_print(antecedant)
            conse_str = extract_features_to_print(consequent)
            print("Rule",counter,":",ante_str,"=>",conse_str)
            print("Information Gain:",ig, "Confidence:",confidence,"Support:",support,'\n')

            counter += 1
        else:
            break
        #print('\n')

f = ('Feature (301,) : 0-2', 'Feature (50,) : 1')
#extract_features_to_print(f)
printRules(rules)