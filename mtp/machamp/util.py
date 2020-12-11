import os
import copy
import glob
import logging
from datetime import datetime

from allennlp.commands.train import train_model_from_file
from allennlp.common import Params
from allennlp.models.archival import load_archive

from machamp.predictor import MachampPredictor
from allennlp.commands.predict import _PredictManager

logger = logging.getLogger(__name__)

def merge_configs(params_config_path, datasets_config_path):
    params_config = Params.from_file(params_config_path)
    datasets_config = Params.from_file(datasets_config_path)

    # to support reading from multiple files we add them to the datasetreader constructor instead
    # the following ones are there just here to make allennlp happy
    params_config['train_data_path'] = 'TRAINPLACEHOLDER'
    params_config['validation_data_path'] = 'DEVPLACEHOLDER'

    params_config['dataset_reader']['datasets'] = datasets_config.as_dict()

    ordered_stuff = {}
    new_decoders = {}
    for dataset in datasets_config:
        for task in datasets_config[dataset]['tasks']:
            # start out with default decoder
            task_decoder = copy.deepcopy(params_config['model']['decoders']['default'].as_dict())

            # add task_type defaults
            task_type = datasets_config[dataset]['tasks'][task]['task_type']
            if task_type not in params_config['model']['decoders']:
                tasks_list = [task_str for task_str in params_config['modeĺ']['decoders']]
                del tasks_list['default']
                logger.error('Task type ' + task_type + " is not supported, please use one of " + str(tasks_list))
            task_decoder.update(params_config['model']['decoders'][task_type].as_dict())

            # add anything that is defined in dataset_config
            task_decoder.update(datasets_config[dataset]['tasks'][task].as_dict())

            # add name of task to task itself (used to log metrics)
            task_decoder['task'] = task

            # Used to create an ordered list later
            ordered_stuff[task] = [task_decoder['order'], task_type]

            # remove items only used in datareader, and items save in ordered_stuff
            for item in ['column_idx', 'task_type', 'order']:
                if item in task_decoder:
                    del task_decoder[item]
            new_decoders[task] = task_decoder 

        if 'max_sents' not in datasets_config[dataset] and params_config['model']['default_max_sents'] != 0:
            params_config['dataset_reader']['datasets'][dataset]['max_sents'] = params_config['model']['default_max_sents']
    if 'default_max_sents' in params_config['model']:
        del params_config['model']['default_max_sents']

    params_config['model']['decoders'] = new_decoders

    # Used in the machamp model to decide which order to use
    # generate ordered lists, which make it easier to use in the machamp model
    ordered_tasks = []
    ordered_task_types = []
    no_padding = []
    for label, idx in sorted(ordered_stuff.items(), key=lambda item: item[1]):
        ordered_tasks.append(label)
        ordered_task_types.append(ordered_stuff[label][1])
        if ordered_stuff[label][1] == 'dependency':
            no_padding.append(label + '_rels')
            no_padding.append(label + '_head_indices')
        else:
            no_padding.append(label)
        #TODO, might want to add seq2seq here as well?
    params_config['model']['tasks'] = ordered_tasks
    params_config['model']['task_types'] = ordered_task_types
    params_config['vocabulary'] = {'non_padded_namespaces': ['dataset']}
    #params_config['vocabulary'] = {'non_padded_namespaces': no_padding + ['dataset', 'src_tokens']}

    return params_config


def train(config, name, resume):
    now = datetime.now()
    serialization_dir = 'logs/' + name + '/' + now.strftime("%Y.%m.%d_%H.%M.%S") + '/'
    if resume:
        serialization_dir = name
    if not os.path.isdir(serialization_dir):
        os.makedirs(serialization_dir)

    config_path = serialization_dir + 'config.json'
    config.to_file(config_path)

    train_model_from_file(config_path,
                        serialization_dir,
                        file_friendly_logging=True,
                        force=(not resume), 
                        recover=resume)
    if os.path.isfile(serialization_dir + 'vocabulary/.lock'):
        os.remove(serialization_dir + 'vocabulary/.lock')
    return serialization_dir

def predict_model_with_archive(predictor: str, params: Params, archive: str,
                               input_file: str, output_file: str, batch_size: int = None):

    if 'cuda_device' in params['trainer']:
        cuda_device = params['trainer']['cuda_device']
        from allennlp.common.checks import check_for_gpu
        check_for_gpu(cuda_device)
        archive = load_archive(archive, cuda_device=cuda_device)
    else:
        archive = load_archive(archive)

    for item in archive.config.duplicate():
        archive.config.__delitem__(item)
    for item in params:
        archive.config[item] = params.as_dict()[item]

    predictor = MachampPredictor.from_archive(archive, predictor)

    if batch_size == None:
        batch_size = params['data_loader']['batch_sampler']['batch_size']

    manager = _PredictManager(predictor,
                              input_file,
                              output_file,
                              batch_size,
                              print_to_console=False,
                              has_dataset_reader=True)
    manager.run()

