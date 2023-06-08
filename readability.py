def main():
    text = str(input("Text: "))  # get text from user
    # set variables for later use
    letters = 0
    words = 1
    sentences = 0
    length = len(text)  # calculate the text length
    for i in range(length):
        # if i is a letter, increase letter count by one
        if text[i].isalpha():
            letters += 1
        # if i is a space, increase word count by one
        elif text[i].isspace():
            words += 1
        # if i is punctuation, increase sentence count by one
        elif text[i] == '.' or text[i] == '!' or text[i] == '?':
            sentences += 1

    letter_avg = letters / words * 100
    sentence_avg = sentences / words * 100
    # calculate grade level
    grade_level = round(0.0588 * letter_avg - 0.296 * sentence_avg - 15.8)
    # print grade level
    if grade_level < 1:
        print("Before Grade 1")
    elif grade_level > 1 and grade_level < 16:
        print(f"Grade {grade_level}")
    elif grade_level > 16:
        print("Grade 16+")


main()