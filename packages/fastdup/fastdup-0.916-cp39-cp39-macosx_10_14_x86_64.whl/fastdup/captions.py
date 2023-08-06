
from fastdup.sentry import fastdup_capture_exception
from fastdup.definitions import MISSING_LABEL
from fastdup.galleries import fastdup_imread
from tqdm import tqdm
import cv2

def generate_labels(filenames, kwargs):
    try:
        from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
        import torch
    except Exception as e:
        fastdup_capture_exception("Auto generate labels", e)
        print("For auto captioning images need to install transforms and torch packages using `pip install transformers torch`")
        return [MISSING_LABEL]*len(filenames)

    try:
        from PIL import Image
        model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        max_length = 16
        num_beams = 4
        gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

        images = []
        for image_path in tqdm(filenames):
            i_image = fastdup_imread(image_path, None, kwargs=kwargs)
            if i_image is not None:
                i_image = cv2.cvtColor(i_image, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(i_image)
                images.append(im_pil)
            else:
                images.append(None)

        pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(device)
        output_ids = model.generate(pixel_values, **gen_kwargs)

        preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        preds = [pred.strip() for pred in preds]
        return preds
    except Exception as e:
        fastdup_capture_exception("Auto caption image", e)
        return [MISSING_LABEL]*len(filenames)

def generate_blip_labels(filenames, kwargs):

    try:
        from transformers import BlipProcessor, BlipForConditionalGeneration
        from PIL import Image
    except Exception as e:
        fastdup_capture_exception("Auto generate labels", e)
        print("For auto captioning images need to install transforms and torch packages using `pip install transformers`")
        return [MISSING_LABEL] * len(filenames)

    try:
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
        preds = []
        for image_path in tqdm(filenames):
            i_image = fastdup_imread(image_path, None, kwargs=kwargs)
            if i_image is not None:
                i_image = cv2.cvtColor(i_image, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(i_image)
                inputs = processor(im_pil, return_tensors="pt")
                out = model.generate(**inputs)
                preds.append((processor.decode(out[0], skip_special_tokens=True)))
            else:
                preds.append(MISSING_LABEL)
        return preds

    except Exception as e:
        fastdup_capture_exception("Auto caption image blip", e)
        return [MISSING_LABEL]*len(filenames)


def generate_vqa_labels(filenames, text, kwargs):
    try:
        from transformers import ViltProcessor, ViltForQuestionAnswering
        from PIL import Image
    except Exception as e:
        fastdup_capture_exception("Auto generate labels", e)
        print(
            "For auto captioning images need to install transforms and torch packages using `pip install transformers`")
        return [MISSING_LABEL] * len(filenames)

    try:
        preds = []
        processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        for image_path in tqdm(filenames):
            i_image = fastdup_imread(image_path, None, kwargs=kwargs)
            if i_image is not None:
                i_image = cv2.cvtColor(i_image, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(i_image)
                encoding = processor(im_pil, text, return_tensors="pt")

                # forward pass
                outputs = model(**encoding)
                logits = outputs.logits
                idx = logits.argmax(-1).item()
                preds.append(model.config.id2label[idx])
            else:
                preds.append(MISSING_LABEL)

        return preds

    except Exception as e:
        fastdup_capture_exception("Auto caption image vqa", e)
        return [MISSING_LABEL]*len(filenames)