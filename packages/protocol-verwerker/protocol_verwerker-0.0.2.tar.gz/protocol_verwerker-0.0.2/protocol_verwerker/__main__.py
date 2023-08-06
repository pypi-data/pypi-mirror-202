from .sequentietabel_generator import generate_sequencetable
from .frequentietabel_generator import generate_frequencetable
import argparse


def main():
    parser = argparse.ArgumentParser(description="Verwerk protocollen tot frequentie- en sequentietabellen.")
    parser.add_argument("tabel",help="Welk type tabel moet gemaakt worden? (Mogelijke argumenten: s(equentie), (f)requentie)") 
    args = parser.parse_args()
    if(args.tabel == "s" or args.tabel == "sequentie"):
        generate_sequencetable()
    elif(args.tabel == "f" or args.tabel == "frequentie"):
        generate_frequencetable()
    else:
        print("Ongeldig argument, probeer het opnieuw")

if __name__ == "__main__":
    main()