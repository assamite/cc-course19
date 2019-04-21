
# Group GPRI
## Usage
>* To run use ```python main.py``` from groups main folder, for development remove all the other folders from main_config.json
### GPU mode 
>* If you have a GPU device then select 'Y/y' during initialization. This would load BigGAN (512x512) module on your GPU.
### CPU mode
>* If you are using CPU mode, put your dummy image in  ``` gpri/images/content``` folder with _0 suffix at the end, or style transfer will not work.

## Universal Style Transfer
### Credits 
> * https://github.com/eridgd/WCT-TF (tensorflow version)
### Running a pre-trained model

> * Download VGG19 model: `bash gpri/gpri_helper/style_help/models/download_vgg.sh`
> * Download checkpoints for the five decoders: `bash gpri/gpri_helper/style_help/models/download_models.sh`
> *Place the downloaded models into the 'style_help/models' folder

