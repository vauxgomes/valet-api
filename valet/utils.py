#!/usr/bin/env python3

# Author: Vaux Gomes
# Contact: vauxgomes@gmail.com
# Version: 1.0

# Modules
import pandas as pd

# Constants
def load_data(data_path, columns):
    # Leitura
    df = pd.read_csv(data_path)

    # Removendo os espaços das colunas
    df.rename(columns={col: col.strip() for col in df.columns}, inplace=True)

    # Removendo colunas
    drop_cols = [col for col in df.columns if col not in columns]
    X = df.drop(columns=drop_cols, axis='columns')

    return X