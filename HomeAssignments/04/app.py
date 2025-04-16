def main():
    anton = 21  # Anton's age is given as 21 years old
    beth = 6 + anton  # Beth is 6 years older than Anton
    chen = 20 + beth  # Chen is 20 years older than Beth
    drew = chen + anton  # Drew is as old as Chen's age plus Anton's age
    ethan = chen  # Ethan is the same age as Chen

    # Print ages with exact formatting
    print("Anton is " + str(anton))
    print("Beth is " + str(beth))
    print("Chen is " + str(chen))
    print("Drew is " + str(drew))
    print("Ethan is " + str(ethan))

if __name__ == '__main__':
    main()