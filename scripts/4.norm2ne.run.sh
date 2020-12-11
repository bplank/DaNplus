# arto gold
python3 scripts/4.norm2ne.split.py data/norm/arto.norm data/norm/arto.norm.dev data/norm/arto.norm.test 336
python3 scripts/4.norm2ne.merge.py data/da_arto_dev.tsv data/norm/arto.norm.dev > data/da_arto_dev_goldNorm.tsv
python3 scripts/4.norm2ne.merge.py data/da_arto_test.tsv data/norm/arto.norm.test > data/da_arto_test_goldNorm.tsv

# arto pred
python3 scripts/4.norm2ne.split.py data/norm/arto.norm.out data/norm/arto.norm.out.dev.out data/norm/arto.norm.out.test.out 336
python3 scripts/4.norm2ne.merge.py data/da_arto_dev.tsv data/norm/arto.norm.out.dev.out > data/da_arto_dev_predNorm.tsv
python3 scripts/4.norm2ne.merge.py data/da_arto_test.tsv data/norm/arto.norm.out.test.out > data/da_arto_test_predNorm.tsv


# For twitter not the whole normalization data is annotated for NE, so we need to match them
# twitter gold
python3 scripts/4.norm2ne.find.py data/da_twitter_dev.tsv data/norm/twitter.norm > data/da_twitter_dev_goldNorm.tsv
python3 scripts/4.norm2ne.find.py data/da_twitter_test.tsv data/norm/twitter.norm > data/da_twitter_test_goldNorm.tsv

# twitter pred
cut -f 1 data/norm/twitter.norm > tmp
paste tmp data/norm/twitter.norm.out | sed "s;^	$;;g" > tmp2
mv tmp2 data/norm/twitter.norm.out
rm tmp
python3 scripts/4.norm2ne.find.py data/da_twitter_dev.tsv data/norm/twitter.norm.out > data/da_twitter_dev_predNorm.tsv
python3 scripts/4.norm2ne.find.py data/da_twitter_test.tsv data/norm/twitter.norm.out > data/da_twitter_test_predNorm.tsv

