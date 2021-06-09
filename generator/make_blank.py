from yake import KeywordExtractor

def Create_Blank(text, blankNum, keyword_duplicate):
    wantedNumber = int(blankNum)
    print(type(keyword_duplicate))
    print(keyword_duplicate)

    if keyword_duplicate:
        kw_extractor = KeywordExtractor(lan="en", n=1, top=wantedNumber)
        keywords = kw_extractor.extract_keywords(text=text)
        keywords = [x for x, y in keywords]
        for i in keywords:
            text = text.replace(i, "__________")
    else:
        kw_extractor = KeywordExtractor(lan="en", n=1, top=wantedNumber)
        keywords = kw_extractor.extract_keywords(text=text)
        keywords = [x for x, y in keywords]
        print(keywords)
        for i in keywords:
            text = text.replace(i, "__________", 1)

    return text
