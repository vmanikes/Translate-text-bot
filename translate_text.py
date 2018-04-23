import traceback

import boto3

translate_client = boto3.client("translate")

def close_bot(fulfillment_state, message, content_type="PlainText"):
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": {
                "contentType": content_type,
                "content": message
            }
        }
    }


def handler(event, context):
    if event.get("currentIntent").get("name") == "translate_bot":
        languages = {
            "arabic"    : "ar",
            "chinese"   : "zh",
            "french"    : "fr",
            "german"    : "de",
            "portuguese": "pt",
            "spanish"   : "es"
        }
        if event.get("currentIntent").get("slots").get("text") is not None and event.get("currentIntent").get("slots").get("lang") is not None:
            text = event.get("currentIntent").get("slots").get("text")
            lang = event.get("currentIntent").get("slots").get("lang").lower()

            try:
                response = translate_client.translate_text(
                    Text=text,
                    SourceLanguageCode="auto",
                    TargetLanguageCode=languages[lang]
                )

                return close_bot("Fulfilled", "{} to {} is {}".format(text, lang.title(), response.get("TranslatedText")))

            except Exception as e:
                print(traceback.format_exc())
                return close_bot("Failed",
                          "We are unable to translate your text. Try our supported languages Arabic (ar), Chinese (Simplified) (zh), French (fr), German (de), Portuguese (pt) and Spanish (es)")

        else:
            return close_bot("Failed",
                      "We are unable to translate your text. Try our supported languages Arabic (ar), Chinese (Simplified) (zh), French (fr), German (de), Portuguese (pt) and Spanish (es)")
