import api

# todo
# test by mocking the response from api
async def test_request() -> None:
    successRate = api()
    endpoint = '/api/pos'
    mock_data = {
        "partOfSpeech": "nominal sentence",
        "children": [
            {
            "partOfSpeech": "subject",
            "children": [
                {
                "partOfSpeech": "noun",
                "word": "\u0627\u0644\u0643\u0648\u0628",
                "children": []
                }
            ]},
            {
            "partOfSpeech": "predicate",
            "children": [
                {
                "partOfSpeech": "prepositional phrase",
                "children": [
                    {
                    "partOfSpeech": "prep",
                    "word": "\u0639\u0644\u064a",
                    "children": []
                    },
                    {
                    "partOfSpeech": "noun",
                    "word": "\u0627\u0644\u0637\u0627\u0648\u0644\u0647",
                    "children": []
                    }
                ]}
            ]}
        ]
    }

    assert '' == ''