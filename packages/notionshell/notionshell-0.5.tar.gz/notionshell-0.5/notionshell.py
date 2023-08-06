import argparse
import json
import os
import sys

import notion_client

PARSER = argparse.ArgumentParser(description="Command line wrapper for notion")
PARSER.add_argument("--json", action="store_true", default=False)

parsers = PARSER.add_subparsers(dest="command")
db = parsers.add_parser("database")
db_parsers = db.add_subparsers(dest="db_command")
db_list = db_parsers.add_parser("list")
db_page = db_parsers.add_parser("page")
db_page.add_argument("id")

page_parsers = parsers.add_parser("page")
page_subparsers = page_parsers.add_subparsers(dest="page_command")
page_text = page_subparsers.add_parser("text")
page_text.add_argument("id")
append_text = page_subparsers.add_parser("append")
append_text.add_argument("id")


def json_print(data):
    print(json.dumps(data))


class Run:
    def __init__(self, client, args):
        self.client = client
        self.args = args

    def main(self):
        args = self.args
        client = self.client
        if args.command == "db" and args.db_command == "list":
            response = client.search(filter={"value": "database", "property": "object"})
            for result in response["results"]:
                if args.json:
                    json_print(result)
                else:
                    db = DatabaseData(result)
                    print(db.id, db.title)
        elif args.command == "db" and args.db_command == "pages":
            response = client.databases.query(database_id=args.id)
            for result in response["results"]:
                self.print_page(result)
        elif args.command == "page" and args.page_command == "text":
            response = client.blocks.children.list(block_id=args.id)
            for result in response["results"]:
                print(result)
        elif args.command == "page" and args.page_command == "overwrite":
            response = client.blocks.children.list(block_id=args.id)
            for result in response["results"]:
                print(result)
        elif args.command == "page" and args.page_command == "append":
            print("Input page text (C-d when finished):")
            text = sys.stdin.read()
            response = client.blocks.children.append(
                block_id=args.id,
                children=[
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": text},
                                }
                            ],
                        },
                    }
                ],
            )

    def print_page(self, page):
        if self.args.json:
            print(json.dumps(page))
        else:
            data = PageData(page)
            print(data.id, data.title)


class DatabaseData:
    # Like page data but for notion dbs
    def __init__(self, data):
        self.data = data

    @property
    def id(self):
        return self.data["id"]

    @property
    def title(self):
        titles = self.data["title"]
        if titles:
            return titles[0]["text"]["content"]
        else:
            return "NONE"


class PageData:
    def __init__(self, data):
        self.data = data

    @property
    def id(self):
        return self.data["id"]

    @property
    def title(self):
        titles = self.data["properties"]["Name"]["title"]
        if titles:
            return titles[0]
        else:
            return "NONE"


def main():
    args = PARSER.parse_args()
    client = notion_client.Client(auth=os.environ["NOTION_API_KEY"])
    Run(client, args).main()


if __name__ == "__main__":
    main()
