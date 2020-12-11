
# 0 Download MaChAmp + embeddings
./scripts/0.prep.dabert.sh

# Fetch Reddit data from PushshiftIO
python3 -m pip install --user -r ./requirements.txt
python3 ./scripts/get_reddit.py

# Merge double annotation layer to 1
python3 scripts/gen_mh.py

# Train all MaChAmp models 
python3 scripts/1.train.prep.py > 1.train.sh
chmod +x 1.train.sh
./1.train.sh

# Run all MaChAmp models on all dev sets
python3 scripts/2.dev.pred.py > 2.pred.sh
chmod +x 2.pred.sh
./2.pred.sh
# hack, somehow machamp outputs an internally used token; replace
sed -i "s;@@PADDING@@;O;g" predictions/*/*

# Download normalization model+data
./scripts/3.norm.prep.sh

# Run 10-fold normalization for both Twitter and Arto data
python3 scripts/3.norm.runKfold.py > 3.norm.sh
chmod +x 3.norm.sh
./3.norm.sh

# Merge normalization and NE annotatioin for both predicted and gold norm.
./scripts/4.norm2ne.run.sh

# Merge double annotation layer to 1
python3 scripts/gen_mh.py

# Run NER on normalized data
python3 scripts/5.normNe.pred.py > 5.pred.sh
chmod +x 5.pred.sh
./5.pred.sh

# Train learning curve models
python3 scripts/6.learningc.train.py > 6.train.sh
chmod +x 6.train.sh
./6.train.sh

# Predict learning curve on all domains
python3 scripts/6.learningc.pred.py > 6.pred.sh
chmod +x 6.pred.sh
./6.pred.sh

# Run prediction on test set for selected models
python3 scripts/7.test.pred.py > 7.pred.sh
chmod +x 7.pred.sh
./7.pred.sh

