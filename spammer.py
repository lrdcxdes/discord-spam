from discum import Client as BaseClient
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)


class Client(BaseClient):
    def __init__(self, *args, **kwargs):
        global clients_len
        super().__init__(*args, **kwargs)
        clients_len += 1
        self.index: int = clients_len


clients_len = 0


def join_guild(client: Client, guild: str):
    result = client.joinGuild(guild)
    # noinspection PyUnresolvedReferences
    logging.info(
        f'[{client.index}] Joined to guild "{guild}" ({client.index}/{clients_len})'
    )
    try:
        return result.json()["guild"]["id"]
    except KeyError:
        logging.error(f"[{client.index}] Error joining to guild {guild}")


def leave_guild(client: Client, guild_id: int):
    client.leaveGuild(guild_id)
    # noinspection PyUnresolvedReferences
    logging.info(
        f'[{client.index}] Left from guild "{guild_id}" ({client.index}/{clients_len})'
    )


def send_message(client: Client, channel: str, message: str):
    client.sendMessage(channel, message)
    # noinspection PyUnresolvedReferences
    logging.info(
        f'[{client.index}] Sent message "{message}" to channel "{channel}" ({client.index}/{clients_len})'
    )


def spam(client: Client, guild: str, channel: str, message: str):
    guild_id = join_guild(client, guild)
    send_message(client, channel, message)
    leave_guild(client, guild_id)


def main(guild: str, channel: str, message: str):
    for client in clients:
        try:
            spam(client, guild, channel, message)
        except Exception as e:
            logging.error(f"[{client.index}] {e}")


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if len(args) < 2:
        print(f'Usage: python spammer.py <invite_code> <channel_id> "<message>"')
        sys.exit(1)
    invite_code = args[0]
    channel_id = args[1]
    if not channel_id.isdigit():
        print("Channel ID must be a number")
        sys.exit(1)

    tokens = open("tokens.txt").read().splitlines()
    if "# Write your discord tokens in this file" in tokens:
        tokens.remove("# Write your discord tokens in this file")
    if len(tokens) == 0:
        logging.error("[-] No tokens found. Exiting.")
        exit()

    clients = [Client(token=token, log=False) for token in tokens]

    logging.info(f"{clients_len} clients loaded")

    guild_ = invite_code.split("/")[-1]

    main(
        guild=guild_,
        channel=channel_id,
        message=args[2] if len(args) > 2 else "Путин хуйло ебаное!",
    )
