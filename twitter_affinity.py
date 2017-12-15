#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 13:08:31 2017

"""

import csv
from datetime import datetime
import json
from twitter_functions import * # these are the functions I wrote for you.
from pprint import pprint
from collections import Counter

#  INSERT THE STARTING USER OR BUSINESS AS A STRING IN THE LIST BELOW
business = ['insert_twitter_user_here']

#  The next cell holds your Twitter authorization credentials. 
#  Then it calls a function that initializes your connection to Twitter. 
# =============================================================================
# 
# =============================================================================

#auth= {"consumer_key": "",
#       "consumer_secret": "",
#       "access_key": "",
#       "access_secret": ""
#       }

api = initialize_twitter(auth)

#  Now you set the handle (or handles) that represent one group or topic on 
#  Twitter. These should be in a list. The output file name (`ofile_name`) is 
#  determined based on today's date and the first element in the list. 
#  Feel free to modify. 


#  change the value in the [] start the friends of the followers data pull
#  the user is the original that we are interested in
starting_user = business # my first group

ofile_name = (datetime.today().strftime("%Y%m%d") + "_" + 
             starting_user[0] + "_" + #  Just take the first one 
                                      #  if there are multiple
             "followers.txt")

# =============================================================================
# 
# =============================================================================

# We'll now go lookup the full information on your starting user(s). 
starting_user_id = []

# All records will be a dictionary with the twitter ID as the key and 
# a UserRecord as the value. This is a named tuple I created. 
all_records = lookup_users_from_handles(api, starting_user)

# We need the IDs that we're getting followers from in a list. 
for id in all_records : #access the keys, which are ids.
    starting_user_id.append(id)
    
# =============================================================================
#     
# =============================================================================

# How long is it going to take us to pull these followers?
total_followers = 0
for id, rec in all_records.items() :
    total_followers += rec.followers_count
    
print("A complete run with no limits run is " + 
      "going to take {min:.2f} minutes ({hour:.2f} hours)" \
      .format(min=total_followers/5000,
      hour=total_followers/(60*5000)))

# =============================================================================
# 
# =============================================================================

# Now let's pull all the followers of our starting_user
# the function I wrote allows you to cap the number of followers you pull
# and uses the ID to generate the query.
# 
# Note that this pull is subject to rate limiting. You can make 15 calls per
# 15 minute window and each can return 5000 users. 
followers_of_starting = gather_followers(api,
                                         starting_user_id,
                                         follower_limit=None) 
#  Modify this limit if you need to. Set it to "None" to get all   

#  followers_of_starting will be a dictionary with the key being the id(s) 
#  in starting_user_id and the value is a list of all the followers.


# And now we'll "hydrate" these user records. 
# Note that this is going to print a lot of rows to the screen, 
# partially just so you can know it's working.  
for start_id, list_of_followers in followers_of_starting.items() :
    
    # Using a set here instead of a list so that we pull each ID only once.
    ids_to_hydrate = {id for id in list_of_followers if id not in all_records} 
    
    these_records = lookup_users_from_ids(api,ids=ids_to_hydrate)

    for id, rec in these_records.items() :
        all_records[id] = rec
        
with open('/Users/ryanjellesed/Desktop/fall_2017/' \
          'Applied-Data-Analytics-BMKT-670/' \
          'Twitter Follower Pull-20171107/' \
          'twitter_affinity_project/' \
          'affinity_project_friends/' + ofile_name,'w') as ofile :
    write_user_rec_headers(ofile)
    for id, rec in all_records.items() :
        write_user_rec(ofile, rec)
                    
# =============================================================================
#  end of follower pull for the original user      
# =============================================================================
# 
#  code for pulling friends of followers
#     
# =============================================================================
#  Import the output file from above.
#  Get the friend ids from each line.
#  Read them into a list to be used in the find friends function below as the 
#  starting users.      
# =============================================================================

#  path to the followers file that was created for the original user
path = '/Users/ryanjellesed/Desktop/fall_2017/' \
       'Applied-Data-Analytics-BMKT-670/' \
       'Twitter Follower Pull-20171107/' \
       'twitter_affinity_project/affinity_project_friends/'

#  open the starting user output file created above
with open(path + ofile_name,'r') as f:
    #  skip the headers
    next(f)
    #  skip the original user 
    next(f)
    #  initialize a list to store 
    followers_of_original = []
    
    for idx, line in enumerate(f):
        delim_troubles = csv.Sniffer().sniff(line)
        line = line.strip()
#        line = line.split(delim_troubles.delimiter)
        line = line.split('\t')

#        line = [faux.replace("'", "") for faux in line]
#        line = [faux.replace('"', '') for faux in line]
            
#        friends_of_hanes_followers.append(line[0])
#        print(line[2])
#        print(type(line[2]))
        followers_of_original.append(line[0])
#        if idx > 10:
#            break

len(followers_of_original)
for idx, line in enumerate(followers_of_original):
    print(line)
    if idx > 10:
        break
# =============================================================================
# 
# =============================================================================

starting_user = followers_of_original # list of users that follow the user

#  set the ouput file name for the friends of the followers
ofile_name = (datetime.today().strftime("%Y%m%d") + "_" + 
             business[0] + "_" + #  Just take the first one 
                                 #  if there are multiple
             "friends_of_followers.txt")

# =============================================================================
# 
# =============================================================================

# We'll now go lookup the full information on starting user(s). 
starting_user_id = []

# All records will be a dictionary with the twitter ID as the key and 
# a UserRecord as the value. This is a named tuple I created. 

all_records = lookup_users_from_handles(api, starting_user)

#  filter all_records for friend_count > 1000 or <5000, in other words
#  any follower of the original with between 1k and 5k 'friends'
#  store those followers in a new dict called modified_friends
modified_friends = {}
for k, line in all_records.items():
    if line[6] > 1000 and line[6] < 5000:
        modified_friends[k] = line
        
#  print the new length of all_records after removing records w/less than 1000
#  or more than 5000 friends
        
len(all_records)
len(modified_friends)

# We need the IDs that we're getting 'friends' from in a list. 
for id in modified_friends : #access the keys, which are ids.
    starting_user_id.append(id)

len(starting_user_id)
       
# =============================================================================
#     
# =============================================================================

# How long is it going to take us to pull these friends?
total_friends = 0
for id, rec in modified_friends.items() :
    total_friends += rec.friends_count
    
print("A complete run with no limits run is " + 
      "going to take {min:.2f} minutes ({hour:.2f} hours)"\
      .format(min=total_friends/5000,
                hour=total_friends/(60*5000)))

# =============================================================================
# 
# =============================================================================
# Now let's pull all the friends of our followers
# the function allows you to cap the number of followers you pull
# and uses the ID to generate the query.
# 
# Note that this pull is subject to rate limiting. You can make 15 calls per
# 15 minute window and each can return 5000 users. 
friends_of_followers = gather_friends(api,
                                         starting_user_id,
                                         friend_limit=None) 
#  Modify this limit if you need to. Set it to "None" to get all   
#  friends_of_followers will be a dictionary with the key being the id(s) 
#  in starting_user_id and the value is a list of all the followers.

#  make Counter of all the friends of the followers

friend_list = []
for k, line in friends_of_followers.items():
    for id in line:
        friend_list.append(id)
friend_counter = Counter(friend_list)

print(len(friend_counter))          
print(friend_counter)
print(len(friend_list))
#friend_counter[713057557187682305]    
Counter(friend_counter).most_common(10)  

# =============================================================================
# Hydrate the friend user records
# =============================================================================
# And now we'll "hydrate" these user records. 
# Note that this is going to print a lot of rows to the screen, 
# partially just so you can know it's working.  
for start_id, list_of_friends in friends_of_followers.items() :
    
    # Using a set here instead of a list so that we pull each ID only once.
    ids_to_hydrate = {id for id in list_of_friends if id not in all_records} 
    
    these_records = lookup_users_from_ids(api,ids=ids_to_hydrate)

    for id, rec in these_records.items() :
        all_records[id] = rec
        
# =============================================================================
#  make friends of follower file 
# =============================================================================

with open(path + 'friends_of_' + business[0] + '_followers' + '.txt','w') as f:
    for k, line in friends_of_followers.items():
        for idx, friend in enumerate(line):
#                friend.strip()
#                friend.split(',')
            f.write(str(k) + "\t" + str(friend) + "\n")

#  make friend set()
#  set of all the friends of the followers
friend_set = set()
for k, line in friends_of_followers.items():
    for idx, friend in enumerate(line):
        friend_set.add(friend)
#print(len(friend_set))

# =============================================================================
# 
# =============================================================================

#  create dictionary to hold affinity scores, names, screen names and follower count
affinity_dict = defaultdict(list)

#  if the follower count is greater than 0 add follower to affinity_dict
for id, rec in all_records.items() :
    if rec.followers_count > 0:
        affinity_dict[id] = rec.name,rec.screen_name, friend_counter[id],rec.followers_count, (friend_counter[id]/rec.followers_count)  
          
#  len(friends_of_followers_dict)           
len(affinity_dict)

#  make and write a file holding the names, screen names, follower counts and 
#  calculated affinity scores
with open(path + 'affinity_scores_for_' + business[0] + '.txt', 'w')as outfile:
    header = [
              "name", 
              "username", 
              "friend of follower count", 
              "followers", 
              "affinity"
              ]
    
    outfile.write("\t".join(header) + "\n")
    for key, line in affinity_dict.items():
#        line = line.strip()
#        line = line.split(',')
#        print(str(line))
        outfile.write("\t".join(str(x) for x in line) + "\n")
        
           