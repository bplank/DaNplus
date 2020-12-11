# Download DA-BERT
wget https://www.dropbox.com/s/19cjaoqvv2jicq9/danish_bert_uncased_v2.zip?dl=1 -O danish_bert_uncased_v2.zip
unzip danish_bert_uncased_v2.zip

# Convert DA-BERT
# OLD VERSION:
#pytorch_transformers bert danish_bert_uncased_v2/bert_model.ckpt danish_bert_uncased_v2/bert_config.json danish_bert_uncased_v2/pytorch_model.bin

# NEW VERSION
transformers-cli convert --model_type bert --tf_checkpoint danish_bert_uncased_v2/bert_model.ckpt --config danish_bert_uncased_v2/bert_config.json --pytorch_dump_output danish_bert_uncased_v2/pytorch_model.bin

# move to right location
mkdir -p configs
mkdir -p configs/archive
mv danish_bert_uncased_v2 configs/archive/
rm danish_bert_uncased_v2.zip

## Download MaChAmp
#git clone https://github.com/machamp-nlp/machamp.git mtp
#cd mtp 
#git reset --hard eaedd45

