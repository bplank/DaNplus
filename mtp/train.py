import argparse
import copy
import logging
import os

from allennlp.common import Params
from allennlp.common.util import import_module_and_submodules

from machamp import util

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--name", default="", type=str, help="Log dir name")
parser.add_argument("--dataset_config", default="", type=str, help="Configuration file for datasets")
parser.add_argument("--parameters_config", default="configs/params.json", type=str,
                    help="Configuration file for parameters of the model")
parser.add_argument("--device", default=None, type=int, help="CUDA device; set to -1 for CPU")
parser.add_argument("--resume", type=str, help="Resume training with the given model")
#parser.add_argument("--archive_bert", action="store_true", help="Archives the finetuned BERT model after training")
args = parser.parse_args()

if args.dataset_config == '' and not args.resume:
    logger.error('when not using --resume, specifying at least --dataset_config is required')

import_module_and_submodules("machamp")

name = args.name
if name == '':
    name = args.dataset_config
    name = name[name.rfind('/')+1: name.rfind('.') if '.' in name else len(name)]

if args.resume:
    train_params = Params.from_file(args.resume + '/config.json')
else:
    train_params = util.merge_configs(args.parameters_config, args.dataset_config)

if args.device is not None:
    train_params['trainer']['cuda_device'] = args.device
    # the config will be read twice, so for --resume we want to overwrite the config file
    if args.resume:
        train_params.to_file(args.resume + '/config.json')

if args.resume:
    name = args.resume
serialization_dir = util.train(train_params, name, args.resume)

# now loads again for every dataset, = suboptimal
for dataset in train_params['dataset_reader']['datasets']:
    dataset_params = train_params.duplicate()
    dev_file = dataset_params['dataset_reader']['datasets'][dataset]['validation_data_path']
    dev_pred = os.path.join(serialization_dir, dataset + '.dev.out')
    datasets = copy.deepcopy(dataset_params['dataset_reader']['datasets'])
    for iter_dataset in datasets:
        if iter_dataset != dataset:
            del dataset_params['dataset_reader']['datasets'][iter_dataset]
    util.predict_model_with_archive("machamp_predictor", dataset_params,
                                    serialization_dir + '/model.tar.gz', dev_file, dev_pred)
