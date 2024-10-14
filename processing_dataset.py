import pandas as pd
from sklearn.preprocessing import StandardScaler

def prepare_dataset(df):
    df['sex'] = df['sex'].map({'female': 0, 'male': 1})
    df['smoker'] = df['smoker'].map({'no': 0, 'yes': 1})
    df['region'] = df['region'].map({
        'southwest': 0,
        'southeast': 1,
        'northwest': 2,
        'northeast': 3
    })    
    return df


def scale_dataset(df, y_column):
    y = df[y_column]
    X = df.drop(columns=[y_column])
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
    scaled_df[y_column] = y.values
    
    return scaled_df


df = pd.read_csv("data/insurance.csv")
df = prepare_dataset(df)
df.to_csv("data/insurance-unscaled.csv", index = False)