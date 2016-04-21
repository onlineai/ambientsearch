#!/bin/bash

# English DRUID wiki lookup list
wget http://machinelearning.online/nlp/druid/enwiki_mwe_druid_200_1000_sorted_length.bz2
mv enwiki_mwe_druid_200_1000_sorted_length.bz2 druid_en.bz2

# Experimental German DRUID lookup list
#wget http://machinelearning.online/nlp/druid/denews_mwe_druid_200_1000_scored_sorted_filtered.bz2
#mv denews_mwe_druid_200_1000_scored_sorted_filtered.bz2 druid_de.bz2

# Ambient Search models
wget http://machinelearning.online/ambient_search/simple-enwiki-latest-models.tar.bz2
tar xvfj simple-enwiki-latest-models.tar.bz2
rm simple-enwiki-latest-models.tar.bz2
wget http://machinelearning.online/ambient_search/conversation.tfidf
