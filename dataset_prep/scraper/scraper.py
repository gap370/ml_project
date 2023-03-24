import requests, sys, time, os, argparse, csv
from datetime import date

# List of simple to collect features
snippet_features = ["title",
                    "publishedAt",
                    "channelId",
                    "channelTitle",
                    "categoryId"]

# Any characters to exclude, generally these are things that become problematic in CSV files
unsafe_characters = ['\n', '"']

# Used to identify columns, currently hardcoded order
header = ["video_id"] + snippet_features + ["trending_date", "tags", "views per day", "likes per day", "dislikes per day",
                                            "comments per day", "thumbnail_link",
                                            "rating", "description", "trending"]

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def date_diff(date1, date2):

    date1_split = date1.split('-')
    date2_split = date2.split('-')

    d1 = date(int(date1_split[0]), int(date1_split[1]), int(date1_split[2]))
    d2 = date(int(date2_split[0]), int(date2_split[1]), int(date2_split[2]))
    delta = d2 - d1

    return delta.days + 1

def get_dislikes_rating(video_id):

    request_url = f"https://returnyoutubedislikeapi.com/votes?videoId={video_id}"

    proxies = { 
              "http"  : "http://richweiwei:Richweiwei500k@pr.oxylabs.io:7777", 
              "https" : "http://richweiwei:Richweiwei500k@pr.oxylabs.io:7777"
            }

    request = requests.get(request_url, proxies=proxies)

    return request.json()["dislikes"], request.json()["rating"]


def setup(api_path, code_path):
    with open(api_path, 'r') as file:
        api_key = file.readline()

    with open(code_path) as file:
        country_codes = [x.rstrip() for x in file]

    return api_key, country_codes


def prepare_feature(feature):
    # Removes any character from the unsafe characters list and surrounds the whole item in quotes
    for ch in unsafe_characters:
        feature = str(feature).replace(ch, "")
    return f'"{feature}"'


def api_request(cate, next_page_token):
    print('new request')
    if (next_page_token != '&'):
        request_url = f"https://www.googleapis.com/youtube/v3/search?pageToken={next_page_token}&part=id,snippet&publishedAfter=2022-12-15T00:00:00Z&publishedBefore=2023-03-15T00:00:00Z&videoCategoryId={cate}&relevanceLanguage=en&type=video&maxResults=50&key={api_key}"
    #request_url = f"https://www.googleapis.com/youtube/v3/search?part=id,snippet&relatedToVideoId={row[0]}&type=video&maxResults=50&key={api_key}"
    else:
        request_url = f"https://www.googleapis.com/youtube/v3/search?part=id,snippet&publishedAfter=2022-12-15T00:00:00Z&publishedBefore=2023-03-15T00:00:00Z&videoCategoryId={cate}&relevanceLanguage=en&type=video&maxResults=50&key={api_key}"
    request = requests.get(request_url)
    #print(request.json())
    related_list = request.json()["items"]
    try:
        next_token = request.json()["nextPageToken"]
    except:
        next_token = 'x'

    return related_list, next_token


    # for i in range(len(related_list)):
    #     related_vid = related_list[i]
    #     vid_id = related_vid["id"]["videoId"]
    #     title = related_vid["snippet"]["title"]

    #     if (not isEnglish(title)):
    #         continue

    #     pub_date = related_vid["snippet"]["publishedAt"][:-10]
    #     if vid_id in id_set:
    #         continue

    #     #print(row[2], pub_date, date_diff(row[2], pub_date))
    #     if date_diff(row[2], pub_date) < -60:
    #         continue

    #     request_url = f"https://www.googleapis.com/youtube/v3/videos?id={vid_id}&part=id,statistics,snippet&key={api_key}"
    #     request = requests.get(request_url)
    #     hit = 1
    #     break;

        

    # if hit == 0:
    #     print('no same range')
    #     # print(row[0])
    #     #vid_id = related_list[0]["id"]["videoId"]
    #     #request_url = f"https://www.googleapis.com/youtube/v3/videos?id={vid_id}&part=id,statistics,snippet&key={api_key}"
    #     #request = requests.get(request_url)
    #     for i in range(len(related_list)):
    #         related_vid = related_list[i]
    #         vid_id = related_vid["id"]["videoId"]
    #         title = related_vid["snippet"]["title"]

    #         if (not isEnglish(title)):
    #             continue

    #         pub_date = related_vid["snippet"]["publishedAt"][:-10]
    #         if vid_id in id_set:
    #             continue

    #         #print(row[2], pub_date, date_diff(row[2], pub_date))

    #         request_url = f"https://www.googleapis.com/youtube/v3/videos?id={vid_id}&part=id,statistics,snippet&key={api_key}"
    #         request = requests.get(request_url)
    #         hit = 1
    #         break;
    
    # if hit == 0:
    #     print('wrong')
    #     print(row[0])

    #     return 0
        
    #print(len(request.json()["items"]))


    # Builds the URL and requests the JSON from it
    #request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet{page_token}chart=mostPopular&regionCode={country_code}&maxResults=50&key={api_key}"
    #request_url = f"https://www.googleapis.com/youtube/v3/search?part=id,snippet{page_token}&relatedToVideoId=5rOiW_xY-kc&type=video&maxResults=50&key={api_key}"
    #request_url = f"https://www.googleapis.com/youtube/v3/videos?id=xwtdhWltSIg&part=id,statistics,snippet&key={api_key}"
    
    #request = requests.get(request_url)

    #print(request.json()['items'])
    #print(len(request.json()['items']))
    #if request.status_code == 429:
    #    print("Temp-Banned due to excess requests, please wait and continue later")
    #    sys.exit()

    #return request.json()


def get_tags(tags_list):
    # Takes a list of tags, prepares each tag and joins them into a string by the pipe character
    return prepare_feature("|".join(tags_list))


def get_videos(items):
    lines = []
    for video in items:
        comments_disabled = False
        ratings_disabled = False

        # We can assume something is wrong with the video if it has no statistics, often this means it has been deleted
        # so we can just skip it
        if "statistics" not in video:
            continue

        # A full explanation of all of these features can be found on the GitHub page for this project
        video_id = prepare_feature(video['id'])

        # Snippet and statistics are sub-dicts of video, containing the most useful info
        snippet = video['snippet']
        statistics = video['statistics']

        # This list contains all of the features in snippet that are 1 deep and require no special processing
        features = [prepare_feature(snippet.get(feature, "")) for feature in snippet_features]

        features[1] = features[1][1:-1][:-10]
        days = date_diff(features[1], str(date.today()))


        # The following are special case features which require unique processing, or are not within the snippet dict
        description = snippet.get("description", "")
        thumbnail_link = snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        thumbnail_link = thumbnail_link.replace('default.jpg', 'hqdefault.jpg')
        trending_date = -1 #time.strftime("%y.%d.%m")
        tags = get_tags(snippet.get("tags", ["[none]"]))
        view_count = round(int(statistics.get("viewCount", 0)) / days, 3)

        # This may be unclear, essentially the way the API works is that if a video has comments or ratings disabled
        # then it has no feature for it, thus if they don't exist in the statistics dict we know they are disabled
        try:
            likes = round(int(statistics['likeCount']) / days, 3)
        except:
            likes = 0

        dislikes = None
        while (dislikes == None):
            try:
                dislikes, rating = get_dislikes_rating(video_id[1:-1])
            except KeyboardInterrupt:
                sys.exit()
            except:
                print("retry")

        dislikes = round(dislikes / days, 3)
        rating = round(rating, 3)

        trending_or_not = 0

        if 'commentCount' in statistics:
            comment_count = round(int(statistics['commentCount']) / days, 3)
        else:
            comments_disabled = True
            comment_count = 0

        # Compiles all of the various bits of info into one consistently formatted line
        line = [video_id] + features + [prepare_feature(x) for x in [trending_date, tags, view_count, likes, dislikes,
                                                                       comment_count, thumbnail_link, rating, description, trending_or_not]]
        lines.append(",".join(line))
    return lines


def get_pages(file_name, next_page_token="&"):
    country_data = [",".join(header)] + []

    id_set = set()

    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = 0

        for row in csv_reader:
            if (row_count != 0):
                id_set.add(row[0])
            row_count += 1

    with open("US_youtube_nontrending_data.csv", "r", encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = 0

        for row in csv_reader:
            if (row_count != 0):
                id_set.add(row[0])

            row_count += 1

    with open("US_youtube_nontrending_data.csv", "a+", encoding='utf-8') as file:
        
        #file.write(f"{country_data[0]}\n")
        row_count = 1

        #cate = [2, 1, 10, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]
        cate = [29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]
        j = 0

        while (row_count < 1000000):

            while (next_page_token != 'x'):
                
                video_data_page, next_page_token = api_request(cate[j], next_page_token)
                for i in range(len(video_data_page)):

                    related_vid = video_data_page[i]
                    vid_id = related_vid["id"]["videoId"]
                    title = related_vid["snippet"]["title"]

                    if (not isEnglish(title)):
                        continue

                    if vid_id in id_set:
                        continue

                    request_url = f"https://www.googleapis.com/youtube/v3/videos?id={vid_id}&part=id,statistics,snippet&key={api_key}"
                    request = requests.get(request_url)
        
                    id_set.add(vid_id)

                    country_data += get_videos(request.json()['items'])
                    file.write(f"{country_data[-1]}\n")
                    #file.write(f"{get_videos(video_data_page['items'])}\n")    
                
                    row_count += 1
                    print(row_count)
            next_page_token = '&'
            j += 1
            


    # # Because the API uses page tokens (which are literally just the same function of numbers everywhere) it is much
    # # more inconvenient to iterate over pages, but that is what is done here.
    # while next_page_token is not None:
    #     # A page of data i.e. a list of videos and all needed data
    #     video_data_page = api_request(next_page_token, file_name)

    #     # Get the next page token and build a string which can be injected into the request with it, unless it's None,
    #     # then let the whole thing be None so that the loop ends after this cycle
    #     next_page_token = video_data_page.get("nextPageToken", None)
    #     next_page_token = f"&pageToken={next_page_token}&" if next_page_token is not None else next_page_token

    #     # Get all of the items as a list and let get_videos return the needed features
    #     items = video_data_page.get('items', [])
    #     country_data += get_videos(items)

    #return country_data


# def write_to_file(country_code, country_data):

#     print(f"Writing {country_code} data to file...")

#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     with open(f"{output_dir}/{time.strftime('%y.%d.%m')}_{country_code}_videos.csv", "w+", encoding='utf-8') as file:
#         for row in country_data:
#             file.write(f"{row}\n")


def get_data(file_name):
    for country_code in country_codes:
        get_pages(file_name)
        # country_data = [",".join(header)] + get_pages(file_name)
        #write_to_file(country_code, country_data)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--key_path', help='Path to the file containing the api key, by default will use api_key.txt in the same directory', default='api_key.txt')
    parser.add_argument('--country_code_path', help='Path to the file containing the list of country codes to scrape, by default will use country_codes.txt in the same directory', default='country_codes.txt')
    parser.add_argument('--output_dir', help='Path to save the outputted files in', default='output/')

    args = parser.parse_args()

    output_dir = args.output_dir
    api_key, country_codes = setup(args.key_path, args.country_code_path)

    get_data("US_youtube_trending_data_trim.csv")

