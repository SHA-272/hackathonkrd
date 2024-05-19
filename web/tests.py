import videostream_extractor, classificator

urls = [
    "https://www.youtube.com/watch?v=liNSvgaMjTc",
    "https://www.youtube.com/watch?v=CHYlH9pPYxU",
    "https://www.youtube.com/watch?v=0a-a8GMe090",
    "https://www.youtube.com/watch?v=7124jZIZauI",
    "https://www.youtube.com/watch?v=n1zw9aoTqpk&list=PL5ayj0VlpHfPP4UVyg4WRwlNf5e3nlyAo",
    "https://www.youtube.com/watch?v=NlCzS5Y1G4o&list=PLQs3W11UxdHbyuaBD-uSmLsGq5pm-6uPl&index=3",
    "https://www.youtube.com/watch?v=cN7XXLyb1Fo",
    "https://www.youtube.com/watch?v=ZgKcRIITHRY",
    "https://www.youtube.com/watch?v=8wn9x40ze_w",
    "https://www.youtube.com/watch?v=yO9RkL1W01U",
    "https://www.youtube.com/watch?v=d_YNOOUjeHw",
    "https://www.youtube.com/watch?v=PhaPiPl_Zm8",
    "https://www.youtube.com/watch?v=kAC1nwja5po",
    "https://www.youtube.com/watch?v=K2hl-zy67Ec",
    "https://www.youtube.com/watch?v=Lbj5C-Sw2_A",
    "https://www.youtube.com/watch?v=xhNv476tAs8",
    "https://www.youtube.com/watch?v=Lt_HUzZUDHw",
    "https://nuum.ru/clips/2137212-bombicheskuiu-devochku-v-topy-srochno-top-rekomendatsii",
    "https://nuum.ru/videos/1540924-shikarnaia-podborka-ochen-smeshnykh-anekdotov-top-14",
    "https://nuum.ru/channel/krasivo/clips/2137178--ofis-rabota-krasivaia-top-podpiska-vzaimno",
    "https://nuum.ru/channel/krasivo/clips/2121447--leto-muzyka-plate-vzaimno-podpiska",
    "https://rutube.ru/video/aa6e284ccace8e57567c17905b9e60a2/",
]

import cv2, json
text = ''
with open('res.txt', 'w') as f:
    for url in urls:
        try:
            v_url = videostream_extractor.get_video_stream(url)
            cap = cv2.VideoCapture(v_url)
            res = classificator.classify_video(cap)
            max_value = 0
            max_category = ''
            for category, values in res.items():
                if values[1] > max_value:
                    max_value = values[1]
                    max_category = category
            json_string = json.dumps(res)
            s = url + '\t\t' + max_category + '\t\t' + json_string + '\n'
            text += s
            print(s)
        except Exception as e:
            print(e)

    f.write(text)
