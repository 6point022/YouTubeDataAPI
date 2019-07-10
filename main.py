from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from youtubeCategories import getYouTubeCategory
from time import sleep
import matplotlib.pyplot as plt



CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)

credentials = flow.run_console()

# Program asks for authorization after the above statement, use refreshToken (but how?) to get rid of it

youtube = build('youtube', 'v3', credentials = credentials)

request  = youtube.videos().list(part = 'snippet', myRating = 'like', maxResults = 50)
likedVideos = request.execute()
likedVideos['pageInfo']
likedVideos['pageInfo']['resultsPerPage']

countByCategoryId = {}
countByChannelTitle = {}

for video in likedVideos['items']:
	catId = video['snippet']['categoryId']
	if catId in countByCategoryId:
		countByCategoryId[catId] += 1
	else:
		countByCategoryId[catId] = 1
	channelTitle = video['snippet']['channelTitle']
	if channelTitle in countByChannelTitle:
		countByChannelTitle[channelTitle] += 1
	else:
		countByChannelTitle[channelTitle] = 1

count = 1

while 'nextPageToken' in likedVideos.keys():
	count += 1
	print('page', count)
	likedVideos['pageInfo']
	request  = youtube.videos().list(part = 'snippet', myRating = 'like', maxResults = 50, pageToken = likedVideos['nextPageToken'])
	likedVideos = request.execute()
	for video in likedVideos['items']:
		catId = video['snippet']['categoryId']
		if catId in countByCategoryId:
			countByCategoryId[catId] += 1
		else:
			countByCategoryId[catId] = 1
		channelTitle = video['snippet']['channelTitle']
		if channelTitle in countByChannelTitle:
			countByChannelTitle[channelTitle] += 1
		else:
			countByChannelTitle[channelTitle] = 1	
	sleep(1)		

print('nextPageToken' in likedVideos.keys())

x = []
y = []
# for catId in countByCategoryId.keys():
# 	x.append(getYouTubeCategory(catId))

# y = list(countByCategoryId.values())

for channelTitle in countByChannelTitle.keys():
	if countByChannelTitle[channelTitle] > 5:
		x.append(channelTitle)	
		y.append(countByChannelTitle[channelTitle])

# y = list(countByChannelTitle.values())

print(x, y)

plt.xticks(rotation = 90)
plt.bar(x, y)
plt.tight_layout()
# plt.xlabel('Video category')
plt.xlabel('YouTube Channels')
plt.ylabel('No. of videos (from the last 1000 liked videos)')
# plt.title("Channels I Watch")
plt.show()
