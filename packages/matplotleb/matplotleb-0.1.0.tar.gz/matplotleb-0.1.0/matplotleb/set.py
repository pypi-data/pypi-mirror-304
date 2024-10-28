ALLCHAR= set()
VOWEL=set()
CONSONANTS=set()
NEW={'C','O','M','P','U','T','E','R'}
input_chars=input("Enter a set of character(without spaces):")
vowel_set={'A','E','I','O','U'}
for char in input_chars.upper():
    ALLCHAR.add(char)
    if char in vowel_set:
        VOWEL.add(char)
    else:
        CONSONANTS.add(char)
print(f"Number of elements in ALLCHAR:{len(ALLCHAR)}")
print(f"Number of elements in VOWEL:{len(VOWEL)}")
print(f"Number of elements in CONSONANTS:{len(CONSONANTS)}")
print(f"Number of elements in NEW:{len(NEW)}")
combined_set=VOWEL.union(CONSONANTS)
print(f"Combined set of VOWEL & CONSONANTS:{combined_set}")
common_elements=NEW.intersection(VOWEL)
print(f"Common elements NEW & VOWEL:{common_elements}")
NEWCOPY=NEW.copy()
print(f"ELEMENTS OF NEWCOPY:{NEWCOPY}")

if NEWCOPY:
    removed_element=NEWCOPY.pop()
    print(f"Removed element from NEWCOPY:{removed_element}")
    print(f"Elements of NEWCOPY after removal:{NEWCOPY}")
NEW.clear()
print(f"Elements of NEW after clearing:{NEW}")
del VOWEL
print("Vowel set has been deleted")
try:
    print(f"VOWEL after Deletion:{VOWEL}")
except NameError as e:
    print(e)
