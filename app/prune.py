import argparse
import datetime
import imaplib
import os
import sys

def connect_imap(username, password):
    m = imaplib.IMAP4_SSL("imap.gmail.com")  # server to connect to
    print("{0} Connecting to mailbox via IMAP...".format(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
    m.login(username, password)
    return m


def delete_old_mail(m, folder, days_before):
    no_of_msgs = int(m.select(f'"{folder}"')[1][0])
    print("- Found a total of {1} messages in '{0}'.".format(folder, no_of_msgs))

    if not m.state == 'SELECTED':
        return

    before_date = (datetime.date.today() - datetime.timedelta(days_before)).strftime("%d-%b-%Y")  # date string, 04-Jan-2013
    typ, data = m.search(None, '(BEFORE {0})'.format(before_date))  # search pointer for msgs before before_date

    if not data[0] == b'':  # if not empty list means messages exist
        no_msgs_del = data[0].split()[-1].decode()  # last msg id in the list
        print("- Marked {0} messages for removal with dates before {1} in '{2}'.".format(no_msgs_del, before_date, folder))
        m.store(f"1:{no_msgs_del}", '+X-GM-LABELS', '\\Trash')  # move items to the Trash
    else:
        print("- Nothing to remove.")


def empty_folder(m, folder, do_expunge=True):
    print("- Empty '{0}' & Expunge all mail...".format(folder))
    m.select(folder)  # select entire folder
    if m.state == 'SELECTED':

        if folder == '[Gmail]/Bin':
            m.store("1:*", '+FLAGS', '\\Deleted')  # Items in the bin are already in the Trash
        else:
            m.store("1:*", '+X-GM-LABELS', '\\Trash')  # move items to the Trash

        if do_expunge:  # See Gmail Settings -> Forwarding and POP/IMAP -> Auto-Expunge
            m.expunge()  # not need if auto-expunge enabled
        else:
            print("Expunge was skipped.")
    else:
        print("Nothing selected for deletion")

    return


def disconnect_imap(m):
    print("{0} Done. Closing connection & logging out.".format(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
    m.close()
    m.logout()
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prune a Gmail folder via IMAP.')
    parser.add_argument(
        'folder',
        nargs=1,
        help='Folder to remove, e.g. \'[Gmail]/Sent Mail\''
    )

    parser.add_argument(
        'age',
        nargs=1,
        type=int,
        help='Delete email over this many days old'
    )
    args = parser.parse_args()
    age = args.age[0]
    folder = args.folder[0]

    if age < 7:
        print("Age must be greater than 7 days", file=sys.stderr)
        sys.exit(1)

    username = os.environ.get('GMAIL_USER')
    password = os.environ.get('GMAIL_PASS')

    if not (username and password):
        print("Please set GMAIL_USER and GMAIL_PASS environment variables!", file=sys.stderr)
        sys.exit(1)

    m_con = connect_imap(username, password)
    delete_old_mail(m_con, folder, age)
    empty_folder(m_con, '[Gmail]/Bin', do_expunge=True)
    disconnect_imap(m_con)

