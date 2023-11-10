import json


class Formatter:
    __MAX_LEN = 4000

    @classmethod
    def _trim_text(cls, text):
        if len(text) > cls.__MAX_LEN:
            text = text[:cls.__MAX_LEN] + '<...>'
        return text

    @classmethod
    def format_message(cls, data):
        json_str = json.dumps(data, ensure_ascii=False)
        text = json.loads(json_str)
        content = cls._trim_text(text['content'])
        return f"⚠️ <b><a href='{text['url']}'>{text['title']}</a></b>\n\n{content}"
