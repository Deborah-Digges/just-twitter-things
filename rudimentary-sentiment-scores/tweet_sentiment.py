import sys
import json

#argv[1] - file mapping words to scores
#argv[2] - tweet file(obtained using streaming api)


# construct a map from word to sentiment score
def build_sent_map(sent_file):
    sent_map = {}
    pairs = map(lambda x: x.split(), sent_file.read().split('\n'))
    for pair in pairs:
        if len(pair) > 2:
            key = ""
            for i in range(len(pair) - 1):
                key += pair[i]
            sent_map[key] = int(pair[-1])
        else:    
            sent_map[pair[0]] = int(pair[1])
    return sent_map 

# remove hashtags, urls, user_mentions, trends, symbols
def strip(tweet):
    index_pairs = []    
    for entity_type in tweet['entities']:
        for entity in tweet['entities'][entity_type]:
            index_pairs.append(entity['indices'])
    index_pairs.sort()

    text = tweet['text'].strip()
    stripped_tweet = ""
    start = 0
    end = None
    for pair in index_pairs:
        end = int(pair[0])           
        stripped_tweet += text[start:end]
        start = pair[1]
        end = pair[1]

    if end:
        stripped_tweet += text[end:]
    tweet['text'] = stripped_tweet
    return tweet

# construct the score of each tweet
def sentiment_score(tweet, sent_map):
    score = 0
    for word in tweet['text'].split():
        score += sent_map.get(word, 0)
    tweet['sent_score'] = score
    return tweet


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
   
    tweets = [json.loads(line) for line in tweet_file]
    sent_map = build_sent_map(sent_file)

    tweets = map(lambda x: sentiment_score(x, sent_map), map(strip, tweets))

    for tweet in tweets:
        print tweet['text'], tweet['sent_score']

if __name__ == '__main__':
    main()
