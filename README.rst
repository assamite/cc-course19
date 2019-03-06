Computational Creativity Course, Spring 2019
############################################

The main repository for group projects.

Each group should *fork* this project, contribute to the forked project (by cloning it locally for each group member)
and then do *pull requests* to this project a couple of times during the course.

Relevant links:

    * `Fork a repo<https://help.github.com/en/articles/fork-a-repo>`_
    * `About pull requests<https://help.github.com/en/articles/about-pull-requests>`_
    * `Creating a pull request from a fork<https://help.github.com/en/articles/creating-a-pull-request-from-a-fork>`_

The first pull request:
=======================

Create your first pull request after:
    # You have forked the repo
    # Made a folder into the repo with your group name

        * Change the group name to match Python module naming, e.g. group "We Are the Best" should have folder "we_are_the_best"

    # Copied contents of the either one of the pre-existing group examples to your folder
    # Changed (the class name and the module name if you so wish and) ``self.domain`` of your creator.
    # Reflected the class name and module name changes to your-group-folder/config.json
    # Changed your creator's ``create``-function to return (dummy) artifact(s) in your domain. That is, the returned
      artifact may pre-exist in your folder.

        * Titles should return ``str``.
        * Poems should return ``str``.
        * Images should return absolute paths to the generated images, either in 'png' or 'jpg' format.
        * Music should return absolute path to either 'wav' (compressed formats are discussable if needed) or to
          an image file of the generated sheet music in 'png' or 'jpg' format.
        * The return format of other domains should be discussed with the course staff.

    # Remember to add the metadata dictionary containing 'evaluation' keyword with (dummy) value to each returned artifact.
    # Check that the code is working by running ``main.py`` using main config file (check ``main_config.json`` but
      create another one for testing purposes) containing only your own folder.

Please make your first pull request before Wed 20.3. 23.59


Get the code running
====================

    # Fork the repo in github (once per group)
    # Clone your forked repo (for each group member)
    # Install Python 3.6+
    # Create python virtual environment in your cloned repo's root using: ``python3.6 -m env``
    # Activate virtualenv using: ``source env/bin/activate``
    # Install general requirements: ``pip install -r requirements.txt``

Now you should be able to run the two example groups using ``python main.py`` and see some output (and definetely not
any errors).

Anytime you want to work on the code, you need to run step 5. again. You can exit the virtual environment by typing
``deactivate``. You can also configure your IDE, e.g. `PyCharm<https://www.jetbrains.com/pycharm/>`_, to use virtual
environment.


Adding your own dependencies
============================

It is possible (and probable) that you want to add your own code dependencies to your group's project. Generally, all
libraries which can be installed using 'pip' can be used. We just need to coordinate between groups that each group
uses the same version of the library.

Add any extra dependencies to ``your_group_folder/requirements.txt` (create one if it does not exist). The course
staff will merge them from time to time to the root folder's ``requirements.txt`` based on the pull requests.

If you need to use any libraries which are not found from 'pip', then first evaluate how crucial it would be for your
project and contact the course staff if it turns out to be really needed. We will see what we can do. However, as the
project's idea is simply to demonstrate computational creativity techniques in practice, the general requirements should
be kept to minimum.







