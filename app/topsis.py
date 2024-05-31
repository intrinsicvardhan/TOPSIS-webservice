import pandas as pd
import numpy as np
# import argparse
import os
import sys

def normalize_data(df):
    squared_sums = df.applymap(lambda x: x**2).sum(axis=0)
    normalized_df = df / np.sqrt(squared_sums.replace(0, 1e-10))
    return normalized_df

def multiply_weights(df, weights):
    df_array = df.values
    weights_array = np.array(weights, dtype=np.float64)
    weights_array = weights_array / sum(weights_array)
    result = df_array * weights_array
    result_df = pd.DataFrame(result, columns=df.columns, index=df.index)
    return result_df

def SplusSminus(df, impacts):
    Splus = np.zeros(df.shape[1])
    Sminus = np.zeros(df.shape[1])

    for i, impact in enumerate(impacts):
        if impact == '+':
            Splus[i] = max(df.iloc[:, i])
            Sminus[i] = min(df.iloc[:, i])
        elif impact == '-':
            Splus[i] = min(df.iloc[:, i])
            Sminus[i] = max(df.iloc[:, i])

    return Splus, Sminus

def performance_score(df, Splus, Sminus):
    EDPlus = ((df - Splus) ** 2).sum(axis=1).apply(np.sqrt)
    EDMinus = ((df - Sminus) ** 2).sum(axis=1).apply(np.sqrt)

    df['Topsis Score'] = EDPlus / (EDPlus + EDMinus)
    df['Rank'] = df['Topsis Score'].rank(ascending=False)

    return df

def run_topsis(input_file_path, weights, impacts, output_file_path):
    try:
        df = pd.read_csv(input_file_path)
    except FileNotFoundError:
        print(f'Error: File {input_file_path} not found')
        exit()
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        exit()

    if df.shape[1] < 3:
        print('Data is not suitable for TOPSIS')
        exit()

    assert len(weights) == len(impacts) and len(impacts) == df.shape[1] - 1, "Length of impacts, weights, and columns must be equal"

    allowed_signs = ['+', '-']
    flag = all(value in allowed_signs for value in impacts)

    assert flag, "Impacts can only be negative or positive"

    df_products = df.iloc[:, 0]
    df = df.drop(columns=df.columns[0])
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    df = normalize_data(df)
    df = multiply_weights(df, weights)
    Splus, Sminus = SplusSminus(df, impacts)

    df = performance_score(df, Splus, Sminus)

    df = pd.concat([df_products, df], axis=1)
    result_df = df[[df.columns[0], df.columns[-2], df.columns[-1]]]
    result_df.to_csv(output_file_path, index=False)

    print(f'Results saved to: {output_file_path}')

if __name__ == "__main__":
    # Extract command-line arguments
    input_file_path = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    output_file_path = sys.argv[4]

    # Splitting weights and impacts into lists
    weights = weights.split(',')
    impacts = impacts.split(',')

    run_topsis(input_file_path, weights, impacts, output_file_path)
