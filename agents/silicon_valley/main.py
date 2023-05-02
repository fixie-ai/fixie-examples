import fixieai

BASE_PROMPT = (
    "I am an agent that answers questions about the TV show Silicon Valley. "
    "User may have follow-up questions that refers to something mentioned before but I "
    "always do Ask Func[fixie_query_corpus] with a complete question, without any "
    "reference."
)

# FEW_SHOTS = """
# Q: Who was Gilfoyle played by?
# Ask Func[fixie_query_corpus]: Who was Gilfoyle played by?
# Func[fixie_query_corpus] says: Gilfoyle was played by Martin Starr.
# A: Gilfoyle was played by Martin Starr.
#
# Q: In which season did Jian-Yang make the Hot Dog app?
# Ask Func[fixie_query_corpus]: In which season did Jian-Yang make the Hot Dog app?
# Func[fixie_query_corpus] says: Jian-Yang made the SeeFood app, which only recognized pictures of hot dogs, in Season 4, Episode 4.
# A: Jian-Yang made the SeeFood app, which only recognized pictures of hot dogs, in Season 4, Episode 4.
# Q: How did it go?
# Ask Func[fixie_query_corpus]: How did Jing-Yang's Hot Dog app go?
# Func[fixie_query_corpus] says: Jian-Yang's Hot Dog app was acquired by Periscope.
# A: Jian-Yang's Hot Dog app was acquired by Periscope.
# """
FEW_SHOTS = []

URLS = [
    "https://en.wikipedia.org/wiki/Silicon_Valley_(TV_series)",
    "https://en.wikipedia.org/wiki/Silicon_Valley_(season_1)",
    "https://en.wikipedia.org/wiki/Silicon_Valley_(season_2)",
    "https://en.wikipedia.org/wiki/Silicon_Valley_(season_3)",
    "https://en.wikipedia.org/wiki/Silicon_Valley_(season_4)",
    "https://en.wikipedia.org/wiki/Silicon_Valley_(season_5)",
    "https://en.wikipedia.org/wiki/Silicon_Valley_(season_6)",
]

CORPORA = [fixieai.DocumentCorpus(urls=URLS)]
agent = fixieai.CodeShotAgent(
    BASE_PROMPT,
    FEW_SHOTS,
    CORPORA,
    conversational=True,
)
