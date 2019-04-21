
# Group GPRI
## Usage
> *To run use ```python main.py``` from groups main folder, for development remove all the other folders from main_config.json
> *GPU mode 
> If you have a GPU device then select 'Y/y' during initialization. This would load BigGAN (512x512) module on your GPU.

* Universal Style Transfer
## Credits 
> * https://github.com/eridgd/WCT-TF (tensorflow version)
## Running a pre-trained model

> *Download VGG19 model: `bash gpri/gpri_helper/style_help/models/download_vgg.sh`
> *Download checkpoints for the five decoders: `bash gpri/gpri_helper/style_help/models/download_models.sh`
> *Place the downloaded models into the models folder

[pre-trained model](https://storage.googleapis.com/download.magenta.tensorflow.org/models/arbitrary_style_transfer.tar.gz)
and extract the file(s) to this folder

