#!/Python27/python
import cgi
import nltk 
import twitterbridge

print "Content-type: text/html"
print
print """<html><head>
<link href='//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css' rel='stylesheet'>
</head><body>aaa"""

# Identify srarting node of Social Graph
request = cgi.FieldStorage()
screenName = request.getvalue("twitter_user")
screenName = screenName if screenName else "ArifSiddiqi1" 

#insert the usernames of real twitter users seperated by "%2C" for training data
realScreenNames=''
#insert the usernames of fake twitter users seperated by "%2C" for training data
fakeScreenNames=''

results1 = twitterbridge.getUsers(realScreenNames)
results2 = twitterbridge.getUsers(fakeScreenNames)

jsonResults1 = results1.json()
jsonResults2 = results2.json()

training = []

for node in jsonResults1:

	trainingNode = (dict(ScreenName = node["screen_name"],
		Location = node["location"],
		Followercount = node["followers_count"],
		Friendscount = node["friends_count"],
		Listedcount = node["listed_count"],
		Profileimage = node["profile_image_url"],
		Geoenabled = node["geo_enabled"],
		Defaultprofileimage = node["default_profile_image"],
		numberofstatuses = node["statuses_count"]), 'ham') 
	training.append(trainingNode)

for node in jsonResults2:

	trainingNode = (dict(ScreenName = node["screen_name"],
		Location = node["location"],
		Followercount = node["followers_count"],
		Friendscount = node["friends_count"],
		Listedcount = node["listed_count"],
		Profileimage = node["profile_image_url"],
		Geoenabled = node["geo_enabled"],
		Defaultprofileimage = node["default_profile_image"],
		numberofstatuses = node["statuses_count"]), 'spam') 
	training.append(trainingNode)	

# Train the classifier with training data
classifier = nltk.classify.NaiveBayesClassifier.train(training)
print sorted(classifier.labels())

# Declare an empty array for testData
testData = []

# Fetch Followers from Graph API
results = twitterbridge.getFollowers(screenName, "-1")
jsonResults = results.json()
print jsonResults

# Place Follower attributes into testArray
for node in jsonResults['users']:
	# Assign attributes to testNode
	testNode = (dict(ScreenName = node["screen_name"],
		Location = node["location"],
		Followercount = node["followers_count"],
		Friendscount = node["friends_count"],
		Listedcount = node["listed_count"],
		Profileimage = node["profile_image_url"],
		Geoenabled = node["geo_enabled"],
		Defaultprofileimage = node["default_profile_image"],
		numberofstatuses = node["statuses_count"]))
	# Append testNode to testData
	testData.append(testNode)

# Run naive bayesian classifier on testData
print classifier.batch_classify(testData)


# Display classification results in an HTML table
# Print <table> and <th> for table headers
print """
<table class="table table-striped">
<tr>
  <th>Spam</th>
  <th>Ham</th>
  
</tr>
"""
for pdist in classifier.batch_prob_classify(testData):
	# print table row <tr> and <td> tags 
	
    print('<tr><td>%.4f</td><td>%.4f</td></tr>' % (pdist.prob('spam'), pdist.prob('ham')))
    #print('%.4f %.4f' % (pdist.prob('spam'), pdist.prob('ham')))

# print table end tag
print """
</table>
</body></html>
"""



