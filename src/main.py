from telethon import TelegramClient
import datetime

API_ID = 'aboba'#secret
API_HASH = 'abiba'#secret

client = TelegramClient('tispom', api_id=API_ID, api_hash=API_HASH)


# function to get time offset
def get_time_offset(n: int) -> datetime.datetime:
    offset = datetime.datetime.today() - datetime.timedelta(n)
    print('since this data all messages will be parsed', offset)
    return offset


# main function
async def main():
    print('Print Name of Channel that will be parsed')
    b = True

    while b is True:
        channel_name = input()
        async for dialog in client.iter_dialogs():
            # print(dialog.name, 'has ID', dialog.id)
            if channel_name == dialog.name:
                print("found it hooray")
                b = False
                break
        if b is True:
            print("no such channel, try again")
    print("now, print number of days, program will parse channel and get data for the last N days")
    number_of_days = input()
    try:
        number_of_days = int(number_of_days)
    except ValueError:
        print('empty or wrong value, using default 7 days')
        number_of_days = 7

    offset = get_time_offset(number_of_days)
    document_name = 'data_%s_%s-%s.txt' % (channel_name, offset.date(), str(datetime.datetime.today().date()))
    with open(document_name, 'a') as f:
        greeting = "DATA FROM %s to %s\n" % (offset.date(), str(datetime.datetime.today().date()))
        f.write(greeting)
        async for message in client.iter_messages(channel_name, offset_date=offset, reverse=True):
            if message.photo:
                continue
            msg = str(message.text)
            # cp1251 encode/decode special for windows because without it there are some issues about emoji`s
            msg = msg.encode('cp1251', errors='replace').decode('cp1251')

            f.write(msg)
            f.write('\n')

        response = 'All the stuff is done, parsed %s channel data for %d days' % (channel_name, number_of_days)
        await client.send_message('me', response)
with client:
    client.loop.run_until_complete(main())
