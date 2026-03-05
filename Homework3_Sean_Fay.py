# Homework 3
# Author: Sean Fay
# Date: 02/04/2026

print("Highway Number Interpreter")
print("Enter 0 or any number > 999 to exit")

while True:
    print("\n" + "="*40)
    highway = int(input("Enter a highway number (1-999): "))
    
    if highway <= 0 or highway > 999:
        print(f"Interstate {highway}: Invalid highway number. Exiting program.")
        break
    elif highway <= 99:
        if highway % 2 == 0:
            direction = "east/west"
        else:
            direction = "north/south"
        print(f"Interstate {highway} runs {direction}.")
    else:
        primary = highway % 100  
        if primary % 2 == 0:
            primary_direction = "east/west"
        else:
            primary_direction = "north/south"
        print(f"Interstate {highway} is an auxiliary highway serving I-{primary}, which runs {primary_direction}.")