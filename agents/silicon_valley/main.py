import fixieai

BASE_PROMPT = (
    "I am an agent that answers questions about the TV show Silicon Valley. "
    "User may have follow-up questions that refers to something mentioned before but I "
    "always do Ask Func[fixie_query_corpus] with a complete question, without any "
    "reference."
)

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
