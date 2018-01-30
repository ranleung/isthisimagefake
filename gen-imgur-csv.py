import pandas as pd
import os
import sys
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

COUNT = int(sys.argv[1])
CSV_OUTPUT_PATH = sys.argv[2]

def Main():
    client_id = os.environ.get('IMGUR_CLIENT_ID')
    client_secret = os.environ.get('IMGUR_CLIENT_SECRET')
    client = ImgurClient(client_id, client_secret)

    imgur_df = pd.DataFrame(columns=['title', 'description', 'img_type', 'url', 'datetime'])
    page = 1
    force_stop = False
    error = None

    while imgur_df.shape[0] < COUNT and not force_stop:
        try:
            print 'Current Count', imgur_df.shape[0]
            tags = client.gallery_tag('photoshop_battles',sort='all', window='time', page=page)

            if tags.items is None:
                force_stop = True
                break

            for item in tags.items:
                if hasattr(item, 'type') and item.type == 'image/jpeg':
                    if passes_imgur_filter(item.title, item.description):
                        data = [
                            item.title,
                            item.description,
                            item.type,
                            item.link,
                            item.datetime
                        ]
                        imgur_df.loc[item.id] = data


                if hasattr(item, 'images') and len(item.images) > 0:
                    for images in item.images:
                            if images['type'] == 'image/jpeg':
                                if passes_imgur_filter(images['title'], images['description']):
                                    data = [
                                        images['title'],
                                        images['description'],
                                        images['type'],
                                        images['link'],
                                        images['datetime']
                                    ]
                                    imgur_df.loc[images['id']] = data

            print 'page', page
            page += 1

        except ImgurClientError as e:
            force_stop = True
            error = {
                'message': e.error_message,
                'code': e.status_code
            }
            print(e.error_message)
            print(e.status_code)


    imgur_df.to_csv(CSV_OUTPUT_PATH, encoding='utf-8', index=True)
    print "Total: ", imgur_df.shape[0]
    print "Output to ", CSV_OUTPUT_PATH

def passes_imgur_filter(title, desc):
    if desc and desc.lower().find("original") != -1:
        return False
    if title and title.lower().find("original") != -1:
        return False
    return True


if __name__ == '__main__':
    Main()
