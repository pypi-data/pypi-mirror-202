### Implement program "userlex"
# userlex parse "text"
import argparse
import json

from userlex.social_media import SocialMedia

if __name__ == "__main__":
    # set up argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('command', metavar='COMMAND', nargs='?', default=None)
    parser.add_argument('text', metavar='TEXT', nargs='?', default=None)
    r = SocialMedia.parse("text")
    # print as JSON to console
    print(json.dumps(r, indent=4, sort_keys=True))
    args = parser.parse_args()
    if args.command == "parse":
        r = SocialMedia.parse(args.text)
        # print as JSON to console
        print(json.dumps(r, indent=4, sort_keys=True))
