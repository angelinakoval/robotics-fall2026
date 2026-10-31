# Visual evaluation

Shared images: 31. Cup detection threshold: 0.3.
NMS overlap: 0.45. Classification cup-score threshold: 0.285.
Foreground threshold: 0.35.

Cup AP50: 0.8362777887074564.
Classification accuracy: 0.3870967741935484, precision: 1.0, recall: 0.05.

Classification maps the ImageNet cup and coffee mug scores to a binary rule. The segmenter predicts class-agnostic salient foreground, evaluated against the desired cup region. These are different output tasks.

Pixel annotations are approximate manually traced visible-cup silhouettes. Independent photos have no pixel labels and are excluded from mask scores. Both-empty masks score 1. Inspect target-present and absent rows separately.

AP50 uses one cup class at IoU 0.50, with a 0.001 proposal score floor. It is not multiclass or multi-IoU COCO mAP. Timings exclude loading, transport and action. See the mission explanation for the student's conclusions.
