from fileinput import filename
import api
import arrow

DATE_FORMAT = arrow.now().format('YYYYMMDD')
FILENAME = f'inventory_{DATE_FORMAT}.csv'

def main():
    df = api.get_inventory()
    df.to_csv(filename, index=False)
    return df
    
if __name__ == '__main__':
    df = main()
    
    print(df[df['description'].isna()])
