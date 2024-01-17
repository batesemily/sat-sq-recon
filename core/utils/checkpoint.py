'''
Copyright (c) 2023 SLAB Group
Author: Tae Ha "Jeff" Park (tpark94@stanford.edu)
'''

import logging
from os.path import join

import torch

logger = logging.getLogger(__name__)

''' Utility functions for handling model checkpoints '''

def save_checkpoint(states, is_best, is_final, output_dir, filename='checkpoint.pth.tar'):
    torch.save(states, join(output_dir, filename))
    logger.info('   • Checkpoint saved to {}'.format(join(output_dir, filename)))

    if is_best and 'state_dict' in states:
        torch.save(
            states['best_state_dict'],
            join(output_dir, filename.replace('checkpoint', 'model_best'))
        )
        logger.info('   • Best model saved to {}'.format(join(output_dir, 'model_best.pth.tar')))

    if is_final:
        torch.save(
            states['state_dict'],
            join(output_dir, filename.replace('checkpoint', 'model_final'))
        )
        logger.info('   • Final model saved to {}'.format(join(output_dir, 'model_final.pth.tar')))


def load_checkpoint(checkpoint_file, model, optimizer=None, scaler=None, device=torch.device('cpu')):
    # Load checkpoint if it exists
    load_dict = torch.load(checkpoint_file, map_location=device)

    # Load model checkpoint
    model.load_state_dict(load_dict['state_dict'], strict=True)

    # Load optimizer checkpoint
    if optimizer and load_dict['optimizer']:
        optimizer.load_state_dict(load_dict['optimizer'])

        # Load manually to CUDA
        for state in optimizer.state.values():
            for k, v in state.items():
                if isinstance(v, torch.Tensor):
                    state[k] = v.to(device)

    # Load scaler
    if scaler and load_dict['scaler']:
        scaler.load_state_dict(load_dict['scaler'])

    epoch = load_dict['epoch']
    logger.info(f'Checkpoint loaded from {checkpoint_file} at epoch {epoch}')

    # return epoch, load_dict['best_score']
    return epoch