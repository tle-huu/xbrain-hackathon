import re
import csv


def prepare_slack(answer):

    # Build Code for slack
    change_code = re.compile('</?code>')
    answer = re.sub(change_code, ' ` ', answer)

    # Build hyperlinks for slack
    remove_href = re.compile("<a[^>]+href=\"(.*?)\"[^>]*>(.*)?</a>")
    answer = re.sub(remove_href, r'\g<1>', answer)

    # Remove tags for slack
    clean_tag = re.compile('<.*?>')
    answer = re.sub(clean_tag, '', answer)

    # Change Special Characters for Slack
    amp_clean = re.compile('&(?!amp;)')
    answer = re.sub(amp_clean, "&amp;", answer)
    lt_clean = re.compile('<')
    answer = re.sub(lt_clean, "&lt;", answer)
    gt_clean = re.compile('>')
    answer = re.sub(gt_clean, "&gt;", answer)

    return answer

if __name__ == "__main__":
    with open('answershtml.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        row = csv_reader.__next__()
        row = csv_reader.__next__()
        row = csv_reader.__next__()
        row = csv_reader.__next__()
        row = csv_reader.__next__()
        row = csv_reader.__next__()
        row = csv_reader.__next__()

        row = csv_reader.__next__()
        row = csv_reader.__next__()

        print(row['text'])
        print()
        print("----------------------------------------------------------")
        print()
        print(prepare_slack(row['text']))

