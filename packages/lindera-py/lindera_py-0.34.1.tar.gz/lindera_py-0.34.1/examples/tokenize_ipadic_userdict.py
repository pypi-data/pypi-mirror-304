from pathlib import Path

from lindera import load_dictionary  # type: ignore
from lindera import Tokenizer, load_user_dictionary

project_root = Path(__file__).resolve().parent.parent


def main():
    dictionary = load_dictionary("ipadic")
    user_dictionary_path = str(
        project_root / Path("./resources/ipadic_simple_userdic.csv")
    )
    user_dictionary = load_user_dictionary(user_dictionary_path, "ipadic")
    tokenizer = Tokenizer("normal", dictionary, user_dictionary)

    text = "関西国際空港限定トートバッグを東京スカイツリーの最寄り駅であるとうきょうスカイツリー駅で買う"
    print(f"text: {text}\n")

    # tokenize the text
    tokens = tokenizer.tokenize(text)

    for token in tokens:
        print(token.text)


if __name__ == "__main__":
    main()
