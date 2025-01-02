import pandas as pd

def printdataframe(message, rows):
    df = pd.DataFrame()  # Create an empty DataFrame
    df['Column One'] = [message] * rows  # Repeat the message
    return df

def main():
    outputdf = printdataframe("Hello", 5)
    print(outputdf)

if __name__ == "__main__":
    main()
