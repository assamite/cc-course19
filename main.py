"""Main function unifying all the group's creators.

The groups should only contribute to their own folder (and in some cases to resources-folder), but not to this file.
"""

import argparse
import importlib
import json
import os
import sys

#from resources.sample_inputs import SAMPLE_INPUTS, build_sample_input
import inputs
import page


def get_input_arguments(use_samples):
    """Get input arguments given to all groups' creators.
    """
    return inputs.get_input(use_samples)


def get_page_layout(creators):
    domains = []
    for creator in creators:
        domains.append(creator.domain)
    return ['word', 'word']


def get_outputs(input_args, n_artifacts_per_creator, creators):
    """Create 'a page' of the book.
    """
    # TODO: Clean out the code and make it simpler.
    all_artifacts = []
    n_imagepaths = 0
    group_outputs = {}
    kwargs = {'title': "",
            'poem': "",
            'imagepath1': "",
            'imagepath2': "",
            'imagepath3': "",
            'imagepath4': ""
            }

    print()
    for name, creator in creators:
        domain = creator.domain
        print("Generating for {} ({})...".format(name, domain))
        if name == 'group_picasso':
            artifacts = creator.create(*input_args, n_artifacts_per_creator)
        else:
            artifacts = creator.create(*input_args, n_artifacts_per_creator, group_outputs=group_outputs)
        group_outputs[name] = artifacts
        if domain == 'word':
            kwargs['title'] = artifacts[0][0]
        elif domain == 'poetry':
            kwargs['poem'] = artifacts[0][0]
        elif domain == 'image':
            if n_imagepaths == 0:
                kwargs['imagepath1'] = artifacts[0][0]
            if n_imagepaths == 1:
                kwargs['imagepath2'] = artifacts[0][0]
            if n_imagepaths == 2:
                kwargs['imagepath3'] = artifacts[0][0]
            if n_imagepaths == 3:
                kwargs['imagepath4'] = artifacts[0][0]
            n_imagepaths += 1

        print("Output of {} ({}): {}\n".format(name, domain, artifacts))
        all_artifacts.append((name, domain, artifacts))
    #print("All returned artifacts: {}".format(all_artifacts))
    page.create_page(**kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a book using all creators defined in the config.")
    parser.add_argument('-c', dest='config_file',  default='main_config.json',
                        help='Path to the main config file.')
    parser.add_argument('-p', dest='pages', default=10, type=int,
                        help='Number of "pages" to create. A single page contains artifacts from several domains.')
    parser.add_argument('-s', dest='use_samples', default=1, type=int,
                        help="1: use input samples (see resources/sample_inputs), 0: use full set of possible inputs.")

    args = parser.parse_args()
    n_pages = args.pages
    config = json.load(open(args.config_file))
    folders = config['folders']

    group_creators = []
    n_artifacts_per_creator = 1

    # Initialize each group's creator
    for group_folder in folders:
        sys.path.append(os.path.join(os.path.dirname(__file__), group_folder))
        group_config = json.load(open(os.path.join(group_folder, 'config.json')))
        module_name = group_config['module_name']
        class_name = group_config['class_name']
        domain = group_config['domain']
        group_kwargs = group_config['init_kwargs']

        # Dynamically import the main-module from the group's folder and the class specified in the config.
        print("Initializing '{}' ({})...".format(group_folder, domain))
        group_module = importlib.import_module("{}.{}".format(group_folder, module_name))
        group_class = getattr(group_module, class_name)
        class_instance = group_class(**group_kwargs)
        group_creators.append([group_folder, class_instance])
        print()

    # Run each groups creator for a number of times specified in command line.
    for i in range(n_pages):
        input_args = get_input_arguments(args.use_samples)
        print("Producing outputs for page {}/{} with input: {}".format(i+1, n_pages, input_args))
        get_outputs(input_args, n_artifacts_per_creator, group_creators)

