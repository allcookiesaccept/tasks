# https://colab.research.google.com/github/searchsolved/search-solved-public-seo/blob/main/search_engine_journal/SEJ_Semantic_Clustering_Tool_by_LeeFootSEO.ipynb
# https://www.searchenginejournal.com/semantic-keyword-clustering-python/437166/#close
import sys
import time
import sys
import pandas as pd
import chardet
import codecs
from detect_delimiter import detect
from sentence_transformers import SentenceTransformer, util

# upload the keyword export
upload = open('cleaned_products.txt', 'r', encoding='utf-8').read().splitlines()

# Set Cluster Accuracy & Minimum Cluster Size
cluster_accuracy = 85  # 0-100 (100 = very tight clusters, but higher percentage of no_cluster groups)
min_cluster_size = 2  # set the minimum size of cluster groups. (Lower number = tighter groups)

# Choose a Sentence Transformer

#transformer = 'all-mpnet-base-v2'  # provides the best quality
transformer = 'all-MiniLM-L6-v2'  # 5 times faster and still offers good quality

# automatically detect the character encoding type
#
# acceptable_confidence = .8
#
# contents = upload
#
# codec_enc_mapping = {
#     codecs.BOM_UTF8: 'utf-8-sig',
#     codecs.BOM_UTF16: 'utf-16',
#     codecs.BOM_UTF16_BE: 'utf-16-be',
#     codecs.BOM_UTF16_LE: 'utf-16-le',
#     codecs.BOM_UTF32: 'utf-32',
#     codecs.BOM_UTF32_BE: 'utf-32-be',
#     codecs.BOM_UTF32_LE: 'utf-32-le',
# }
#
# encoding_type = 'utf-8'  # Default assumption
# is_unicode = False
#
# for bom, enc in codec_enc_mapping.items():
#     if contents.startswith(bom):
#         encoding_type = enc
#         is_unicode = True
#         break
#
# if not is_unicode:
#     # Didn't find BOM, so let's try to detect the encoding
#     guess = chardet.detect(contents)
#     if guess['confidence'] >= acceptable_confidence:
#         encoding_type = guess['encoding']
#
# print("Character Encoding Type Detected", encoding_type)

# automatically detect the delimiter
with open('cleaned_products.txt',encoding='utf-8') as myfile:
    firstline = myfile.readline()
myfile.close()
delimiter_type = detect(firstline)

# create a dataframe using the detected delimiter and encoding type
df = pd.read_table(('cleaned_products.txt'), on_bad_lines='skip', encoding='utf-8', delimiter=delimiter_type)
count_rows = len(df)
if count_rows > 50_000:
  print("WARNING: You May Experience Crashes When Processing Over 50,000 Keywords at Once. Please consider smaller batches!")
print("Uploaded Keyword CSV File Successfully!")
df


# standardise the keyword columns
df.rename(columns={"Search term": "Keyword", "keyword": "Keyword", "query": "Keyword", "query": "Keyword", "Top queries": "Keyword", "queries": "Keyword", "Keywords": "Keyword","keywords": "Keyword", "Search terms report": "Keyword"}, inplace=True)

if "Keyword" not in df.columns:
  print("Error! Please make sure your csv file contains a column named 'Keyword!")

# store the data
cluster_name_list = []
corpus_sentences_list = []
df_all = []

corpus_set = set(df['Keyword'])
corpus_set_all = corpus_set
cluster = True


# Clustering Keywords - This can take a while!

# keep looping through until no more clusters are created

cluster_accuracy = cluster_accuracy / 100
model = SentenceTransformer(transformer)

remaining = 0
while cluster:

    corpus_sentences = list(corpus_set)
    check_len = len(corpus_sentences)

    corpus_embeddings = model.encode(corpus_sentences, batch_size=256, show_progress_bar=True, convert_to_tensor=True)
    clusters = util.community_detection(corpus_embeddings, min_community_size=min_cluster_size, threshold=cluster_accuracy, init_max_size=len(corpus_embeddings))

    for keyword, cluster in enumerate(clusters):
        print("\nCluster {}, #{} Elements ".format(keyword + 1, len(cluster)))

        for sentence_id in cluster[0:]:
            print("\t", corpus_sentences[sentence_id])
            corpus_sentences_list.append(corpus_sentences[sentence_id])
            cluster_name_list.append("Cluster {}, #{} Elements ".format(keyword + 1, len(cluster)))

    df_new = pd.DataFrame(None)
    df_new['Cluster Name'] = cluster_name_list
    df_new["Keyword"] = corpus_sentences_list

    df_all.append(df_new)
    have = set(df_new["Keyword"])

    corpus_set = corpus_set_all - have
    remaining = len(corpus_set)
    print("Total Unclustered Keywords: ", remaining)
    if check_len == remaining:
        break

# make a new dataframe from the list of dataframe and merge back into the orginal df
df_new = pd.concat(df_all)
df = df.merge(df_new.drop_duplicates('Keyword'), how='left', on="Keyword")

# rename the clusters to the shortest keyword in the cluster
df['Length'] = df['Keyword'].astype(str).map(len)
df = df.sort_values(by="Length", ascending=True)

df['Cluster Name'] = df.groupby('Cluster Name')['Keyword'].transform('first')
df.sort_values(['Cluster Name', "Keyword"], ascending=[True, True], inplace=True)

df['Cluster Name'] = df['Cluster Name'].fillna("zzz_no_cluster")

del df['Length']

# move the cluster and keyword columns to the front
col = df.pop("Keyword")
df.insert(0, col.name, col)

col = df.pop('Cluster Name')
df.insert(0, col.name, col)

df.sort_values(["Cluster Name", "Keyword"], ascending=[True, True], inplace=True)
uncluster_percent = (remaining / count_rows) * 100
clustered_percent = 100 - uncluster_percent
print(clustered_percent,"% of rows clustered successfully!")

df.to_csv('Clustered.csv', index=False)
