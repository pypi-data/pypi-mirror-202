import re as _re
import functools as _functools

def _regex_ParsePattern(pattern:str):
    flagSplitterPos = pattern.rfind("/")
    if pattern[0] != "/" and flagSplitterPos == -1:
        raise Exception("Pattern need to have format of '/pattern/flags'")
    regexPattern = pattern[1:flagSplitterPos]  # remove first slash
    flags = pattern[flagSplitterPos + 1 :]
    flagLookup = {"i": _re.IGNORECASE, "s": _re.DOTALL, "m": _re.MULTILINE}
    activeFlags = []
    for i in flags:
        activeFlags.append(flagLookup[i])

    if _re.DOTALL not in activeFlags and _re.MULTILINE not in activeFlags:
        activeFlags.append(_re.MULTILINE)

    flagParamValue = _functools.reduce(lambda x, y: x | y, activeFlags)
    return (regexPattern, flagParamValue)

def Replace(pattern: str, replacement: str, message:str) -> str:  
    """
    Replace occurences in message

    example:
        result = RegexReplace(r"/hej (.*?) /i", r"bye \\1 or \g<1> ", "hej v1.0 hej v2.2 hejsan v3.3") # result = "bye v1.0 or v1.0 bye v2.2 or v2.2 hejsan v3.3"

    param pattern:
        use format "/regex/flags", allowed flags i=ignorecase, s=dotall
    
    param replacement:
        Specifies what to replace the matches with\n
        Back reference to capture groups with \\1...\\100 or \g<1>...\g<100>

    returns:
        replaced content or same text if not matches
    """
    regexPattern, flagParamValue = _regex_ParsePattern(pattern)
    return  _re.sub(regexPattern, replacement, message, flags=flagParamValue)

def Match(pattern: str, string: str) -> (list[list[str]] | None):  
    """
    finds all matches, default flags is case sensitive and multiline

    example:
        Regex_Match(r"/hej (.*?) /is", "hej v1.0 hej v2.2 hejsan v3.3") --> [['hej v1.0 ', 'v1.0'], ['hej v2.2 ', 'v2.2']]

    param pattern:
        use format "/regex/flags", allowed flags i=ignorecase, s=dotall

    returns:
        None if no matches found
    or
        2d list, where rows are matches, and each col corresponds to the capture groups
        example: [[match1, capture1, capture2][match2, capture1, capture2]]
    """
    flagSplitterPos = pattern.rfind("/")
    if pattern[0] != "/" and flagSplitterPos == -1:
        raise Exception("Pattern need to have format of '/pattern/flags'")
    regexPattern = pattern[1:flagSplitterPos]  # remove first slash
    flags = pattern[flagSplitterPos + 1 :]
    flagLookup = {"i": _re.IGNORECASE, "s": _re.DOTALL, "m": _re.MULTILINE}
    activeFlags = []
    for i in flags:
        activeFlags.append(flagLookup[i])

    if _re.DOTALL not in activeFlags and _re.MULTILINE not in activeFlags:
        activeFlags.append(_re.MULTILINE)

    flagParamValue = _functools.reduce(lambda x, y: x | y, activeFlags)
    iterator = _re.finditer(regexPattern, string, flags=flagParamValue)
    results = []
    for i in iterator:
        matches = []
        matches.append(i.group(0))
        if len(i.groups()) > 0:
            matches = matches + list(i.groups())
        results.append(matches)
    if len(results) == 0:
        return None
    return results  



############################## Archived Snippets, since they are available in this module instead ###############################

#########
# # @prefix _regex_replace
# # @description 

# # returns string with replacements
#  result = _re.sub(r"hej (.*?) ", r"bye \1 or \g<1> ", "hej v1.0 hej v2.2 hejsan v3.3", flags=_re.DOTALL | _re.IGNORECASE) # result = "bye v1.0 or v1.0 bye v2.2 or v2.2 hejsan v3.3" 
#########

#########
# # @prefix _regex_match
# # @description 

# # finds first occurence of a match or None, can be used directly in if statements
# # matched object can be accessed through result[0], captured groups can becalmessed by result[1]...result[100]
# result = _re.search(r"hej (.*?) ", "hej v1.0 hej v2.2 hejsan v3.3", flags=_re.DOTALL | _re.IGNORECASE)  # result[0] = "hej v1.0 ", result[1] = "v1.0"
#########


#########
# # @prefix _regex_match
# # @description 

# #no capture groups returns list of string matches
# result1 = _re.findall(r"hej .*? ", "hej v1.0 hej v2.2 hejsan v3.3", flags=_re.DOTALL | _re.IGNORECASE) # result[0] = "hej v1.0 ", result[1] = "hej v2.2 "
# #one capture group returns list of string capture group matches
# result2 = _re.findall(r"hej (.*?) ", "hej v1.0 hej v2.2 hejsan v3.3", flags=_re.DOTALL | _re.IGNORECASE) # result[0] = "v1.0", result[1] = "v2.2"
# #multiple capture groups returns list in list, where the inner list contains captured group
# result3 = _re.findall(r"(hej) (.*?) ", "hej v1.0 hej v2.2 hejsan v3.3", flags=_re.DOTALL | _re.IGNORECASE) # result[0] = ["hej", "v1.0"], result[1] = ["hej", "v2.2"]
#########