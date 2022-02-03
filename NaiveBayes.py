#Jeremiah Hennessy 4108453
from scipy.io import arff
import pandas as pd
import pickle

def occurences(value, tests, index):
    count = 0
    for i in range(0, len(tests)):
        if bytes(value, encoding = 'ascii') == tests[i][index]:
            count += 1
    return count

def occurence_relation(value, tests, index, outcome, outcome_row_index):
    count = 0
    for i in range(0, len(tests)):
        if bytes(value, encoding = 'ascii') == tests[i][index] and bytes(outcome, encoding = 'ascii') == tests[i][outcome_row_index]:
            count += 1
    return count

def sub_attribute_relation(sub_attribute, tests, index, sub_attr_values, outcomes, outcome_row_index):
    for x in outcomes:
        sub_attr_values.append(occurence_relation(sub_attribute, tests, index, x, outcome_row_index))

def test(case, prob, metadata):
    index = 0
    outcome_index = 0
    outcome_possibilities = 0
    for x in metadata:
        outcome_index += 1
    
    for x in metadata:
        index += 1
        if index == outcome_index:
            outcome_possibilities = len(meta[x][1])
            outcome_string = x

    outcome_probs = []
    for x in range(0, outcome_possibilities):
        outcome_probs.append(1)
        index = 0
        for y in metadata:
            if index == outcome_index-1:
                outcome_probs[x] *= prob[outcome_index-1][0][x]
                break
            for z in range(0, len(metadata[y][1])):
                if case[index] == bytes(metadata[y][1][z], encoding = 'ascii'):
                    outcome_probs[x] *= prob[index][z][x]
            index += 1

    greatest_index = 0
    greatest_prob = outcome_probs[0]
    for x in range(0, len(outcome_probs)):
        if outcome_probs[x] > greatest_prob:
            greatest_prob = outcome_probs[x]
            greatest_index = x
                
    return metadata[outcome_string][1][greatest_index]

flag = 1
choice = ''
while flag:
    print("""Please choose a menu option by entering the corresponding number:
        1. Train Naive Bayes Classifier
        2. Test Trained Model File by Entering a Test File
        3. Test Trained Model File by Entering Manual Test Case
        4. Exit""""")
    choice = input()
    if choice == '1':
        file_name = input("Please enter the name of an arff file for training without the extension .arff(ex. weather.nominal):")
        data, meta = arff.loadarff((file_name + ".arff"))

        outcome_row_index = 0
        for x in meta:
            outcome_row_index += 1
        
        spot_check = 0
        for x in meta:
            spot_check += 1
            if spot_check == outcome_row_index:
                outcome_string = x

        outcome_row_index -= 1
    
        data_index = 0
        sub_attr_values = []
        attr_values = []
        values = []
        spot_check = 0
        for x in meta:
            if spot_check != outcome_row_index:
                for y in range(0, len(meta[x][1])):
                    sub_attribute_relation(meta[x][1][y], data, data_index, sub_attr_values, meta[outcome_string][1], outcome_row_index)
                    attr_values.append(sub_attr_values)
                    sub_attr_values = []
                values.append(attr_values)
                attr_values = []
                data_index += 1
                spot_check += 1

        outcome_count = []
        for x in range(0, len(meta[outcome_string][1])):
            outcome_count.append(occurences(meta[outcome_string][1][x], data, outcome_row_index))
    
        sub_attr_ratios = []
        attr_ratios = []
        ratios = []
        for x in range(0, len(values)):
            for y in range(0, len(values[x])):
                for z in range(0, len(values[x][y])):
                    sub_attr_ratios.append(float(values[x][y][z])/outcome_count[z])
                attr_ratios.append(sub_attr_ratios)
                sub_attr_ratios = []
            ratios.append(attr_ratios)
            attr_ratios = []
        
        for x in range(0, len(outcome_count)):
            sub_attr_ratios.append(float(outcome_count[x])/len(data))
        attr_ratios.append(sub_attr_ratios)
        ratios.append(attr_ratios)

        print(ratios)

        output_file = open((file_name + ".bin"), "wb")
        pickle.dump(ratios, output_file)
        output_file.close()
        
    elif choice == '2':
        file_name = input("Please enter the name of the model file without the extension(ex. weather.nominal)")
        input_file = open((file_name + ".bin"), "rb")
        ratios = pickle.load(input_file)
        input_file.close()
    
        file_name = input("Please enter the name of an arff file for testing without the extension .arff(ex. weather.nominal):")
        data, meta = arff.loadarff((file_name + ".arff"))
        
        outcome_index = 0
        for x in meta:
            outcome_index += 1
        outcome_index -= 1
        
        predict = []
        real = []
        for x in range(0, len(data)):
            predict.append(bytes(test(data[x], ratios, meta), encoding = 'ascii'))
            real.append(data[x][outcome_index])
        
        actual = pd.Series(real, name='Actual')
        prediction = pd.Series(predict, name='Predictions')
        matrix = pd.crosstab(actual, prediction)
        accuracy_matrix = matrix/matrix.sum(axis=1)
        print(accuracy_matrix)

    elif choice == '3':
        file_name = input("Please enter the name of the model file without the extension(ex. weather.nominal)")
        input_file = open((file_name + ".bin"), "rb")
        data, meta = arff.loadarff((file_name + ".arff"))
        ratios = pickle.load(input_file)
        input_file.close()
        
        outcome_index = 0
        for x in meta:
            outcome_index += 1
        outcome_index -= 1
        
        flag2 = 1
        while flag2:
            data = [str(x) for x in input("Please enter a manual case separating each attribute by a space and make sure it matches the trained data(ex. rainy hot high FALSE:").split()]
            if len(data) == outcome_index:
                predict = test(data, ratios, meta)
                print("The prediction is",predict)
                
                more = input("Add another case enter 1(any other entry will show current results entered):")
                if more != '1':
                    flag2 = 0

    elif choice == '4':
        flag = 0

