import vk_api
import argparse
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


parser = argparse.ArgumentParser(description='Input path to a model')
parser.add_argument("community_id", type=str)
parser.add_argument("cnt", type=int)
args = parser.parse_args()


def main():
    login, password = "", ""
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    vk = vk_session.get_api()

    try:
        communityId = int(args.community_id)
    except ValueError:
        communityId = vk.utils.resolveScreenName(screen_name=args.community_id)["object_id"]
    print(communityId)

    try:
        wall = vk.wall.get(owner_id=-communityId, count=args.cnt)
    except Exception:
        print("bruh")

    posts = wall["items"][1:]

    with open("TEXT.txt", "w", encoding="utf-8") as f:
        for post in posts:
            f.write(post["text"])
            f.write('\n')


if __name__ == '__main__':
    main()
