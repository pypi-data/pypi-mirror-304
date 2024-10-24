# irisml-tasks-training

This is a package for IrisML training-related tasks.

See [irisml repository](https://github.com/microsoft/irisml) for the detail of irisml framework.

## Tasks

### train
Train a pytorch model. A model object must have "criterion" and "predictor" property. See the documents for the detail. Returns a trained model.

### predict
Run inference with a given pytorch model. Returns prediction results.

### append_classifier
Append a classifier layer to an encoder model.

### benchmark_model
Benchmark a given model.

### build_classification_prompt_dataset
Convert a multiclass classification Image Dataset into a dataset with text prompts.

### build_zero_shot_classifier
Build a classifier FC layer from text features. See the CLIP repo for the detail.

### create_classification_prompt_generator
Create a prompt generator for classification task.

### export_onnx
Trace a pytorch model and export it as ONNX using torch.onnx.export(). Throws an exception if it couldn't export. Returns an exported onnx model.

### evaluate_accuracy
Calculate top1 accuracy for given prediction results. It supports only image classification results.

### evaluate_detection_average_precision
Calculate mAP for object detection results.

### get_targets_from_dataset
Get a list or a tensor of targets from a Dataset.

### get_subclass_dataset
Given a list of class ids, extract the sub-dataset of those classes.

### make_feature_extractor_model
Make a new model to extract intermediate features from the given model. Use the predict task to run the extractor model.

### make_image_text_contrastive_model
Make a new model to run image-text contrastive training like CLIP.

### make_image_text_transform
Make a transform function that can be used for a contrastive training

### make_oversampled_dataset
Oversample from a dataset and return a new dataset

### split_image_text_model
Extract image_model and text_model from a image-text model.

### sample_few_shot_dataset
Sample few-shot dataset from given a shot number and random seed.

### train_with_gradient_cache
Train a pytorch model using gradient cache. Useful for training a large contrastive model.

# Available plugins for train task.
- amp
- clip_grad_norm
- ema
- log_summary
- log_tensorboard
- progressbar

# Interfaces for training and prediction
The tasks in this package expects the following interfaces

Notations
- ```input```: An input object for a single example. For example, an image tensor.
- ```target```: A ground truth for a single example.
- ```inputs_batch```: A batch of ```input```.
- ```targets_batch```: A batch of ```target```

## Model

```python
class Model(torch.nn.Module):
    def training_step(self, inputs_batch, targets_batch):  # Returns {'loss': loss_tensor}
        pass
```
A model for training must implement training_step() method. The trainer will provide inputs and targets to the method. It must return a dictionary containing 'loss' entry.

```python
class Model(torch.nn.Module):
    def prediction_step(self, inputs_batch):  # Returns prediction results
        pass 
```
Similarily, a model for prediction must have 'prediction_step()' method. Inputs will be provided to this method and it must return prediction results.

For most of the case, a model implements both methods, training_step() and prediction_step().

## Dataset
The trainer accepts an instance of torch.utils.data.Dataset class. For each index, it must return a tuple (raw_input, target). Curretly, `raw_input` must be a RGB PIL Image object.

## Transform
A transform function must return (input, target) given (raw_inputs, target).

# Inputs and targets formats
## Multiclass Image classification
- input: A float tensor [3, H, W] that represents a RGB image. Its value range is [0-1].
- inputs_batch: A float tensor [N, 3, H, W] if all inputs have the same shape. Otherwise, a list of input.
- target: an integer tensor that represents a class index.
- targets: An integer tensor [N, 1].

## Multilabel Image Classification
- inputs, inputs_batch: Same with above
- taget: An integer tensor [num_classes]. Its value is 0 (negative) or 1 (positive).
- targets_batch: An integer tensor [N, num_classes]

## Object Detection
- inputs, inputs_batch: Same with above
- target: A float tensor [num_boxes, 5]. Each bounding box is represented as [class_index, x0, y0, x1, y1]. x0, y0, x1, y1 is relative coordinates of the left, top, right, bottom of the box. 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1.
- targets_batch: A list of targets

## Image Segmentation
- inputs, inputs_batch: Same with above
- target: A float tensor [num_classes, H, W]. Its value is 0 (negative) or 1 (positive) for each pixel on the sample.
- targets: A float tensor [N, num_classes, H, W]

## CLIP Zero-shot classifier build
build_zero_shot_classifier task has a different interface. It doesn't require a Model instance. Instead, it requires two tensors, text_features and text_labels. 
- text_features: A float tensor [N, feature_size].
- text_labels: An integer tensor[N, 1] that represents a class index for each text.
