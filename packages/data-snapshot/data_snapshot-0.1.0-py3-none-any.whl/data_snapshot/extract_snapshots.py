import os
from pathlib import Path
from typing import Optional

import torch
from pdf2image import convert_from_path
from PIL import Image
from tqdm.auto import tqdm
from transformers import AutoModelForCausalLM, AutoProcessor


class ExtractSnapshot:
    def __init__(
        self,
        output_dir: str | Path,
        model: AutoModelForCausalLM | str,
        device: Optional[str] = None,
    ):
        if isinstance(output_dir, str):
            output_dir = Path(output_dir)

        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)

        if isinstance(model, str):
            self.load_model(model, device)
        else:
            self.model = model
            self.processor = AutoProcessor.from_pretrained(
                model.name_or_path, trust_remote_code=True, device_map=model.device
            )

    def pdf_to_image(self, pdf_path: str | Path):
        images = convert_from_path(pdf_path)

        return images

    def tf_id_detection(self, image: Image):
        prompt = "<OD>"
        inputs = self.processor(text=prompt, images=image, return_tensors="pt")
        inputs.to(self.model.device)

        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            do_sample=False,
            num_beams=3,
        )
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
        annotation = self.processor.post_process_generation(
            generated_text, task="<OD>", image_size=(image.width, image.height)
        )
        return annotation["<OD>"]

    def save_image_from_bbox(self, image: Image, annotation: dict, page: int, output_dir: str | Path):
        # the name should be page + label + index
        for i in range(len(annotation["bboxes"])):
            bbox = annotation["bboxes"][i]
            label = annotation["labels"][i]
            x1, y1, x2, y2 = bbox
            cropped_image = image.crop((x1, y1, x2, y2))

            save_path = os.path.join(output_dir, label, f"page_{page:03}_{label}_{i:03}.png")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            cropped_image.save(save_path)

    def load_model(self, model_id: str, device: str | None = None):
        if device is None:
            if torch.cuda.device_count() > 0:
                device = "cuda:0"
            else:
                device = "cpu"

        self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, device_map=device)
        self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True, device_map=device)
        print("Model loaded: ", model_id)

    def pdf_to_table_figures(
        self,
        pdf_path: str | Path,
        model_id: str | None = None,
        device: str | None = None,
        force: bool = False,
    ):
        if self.model is None and model_id is None:
            raise ValueError("Please provide a model_id")

        pdf_path = Path(pdf_path)

        output_dir = self.output_dir / pdf_path.stem
        success_flag = output_dir / "success.txt"

        if success_flag.exists() and not force:
            print("Already extracted")
            return

        # Remove the success flag
        if success_flag.exists():
            success_flag.unlink()

        images = self.pdf_to_image(pdf_path)

        print(f"PDF loaded. Number of pages: {len(images)}")

        if self.model is None:
            self.load_model(model_id, device)

        print("=====================================")
        print("start saving cropped images")
        for page, image in enumerate(images, start=1):
            annotation = self.tf_id_detection(image)
            self.save_image_from_bbox(image, annotation, page, output_dir)
            print(f"Page {page} saved. Number of objects: {len(annotation['bboxes'])}")

        success_flag.touch()

        print("=====================================")
        print("All images saved to: ", output_dir)

    def dir_pdfs_to_table_figures(
        self,
        pdf_dir: str | Path,
        model_id: str | None = None,
        device: str | None = None,
        force: bool = False,
    ):
        pdf_dir = Path(pdf_dir)
        pdf_paths = sorted(pdf_dir.glob("*.pdf"))

        for pdf_path in tqdm(pdf_paths, desc="Processing PDFs"):
            self.pdf_to_table_figures(pdf_path, model_id, device, force)

        print("All PDFs processed")

    @staticmethod
    def extract_all_from(
        pdf_dir: str | Path,
        output_dir: str | Path,
        model_id: str | None = "yifeihu/TF-ID-large",
        device: str | None = None,
        force: bool = False,
    ):
        extractor = ExtractSnapshot(output_dir, model_id, device)
        extractor.dir_pdfs_to_table_figures(pdf_dir, model_id, device, force)


if __name__ == "__main__":
    from fire import Fire

    Fire(ExtractSnapshot.extract_all_from)
