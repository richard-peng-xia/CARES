# CARES: A Comprehensive Benchmark of Trustworthiness in Medical Vision Language Models

*A comprehensive evaluation of trustworthiness in medical large large vision language models.* [[Paper](https://arxiv.org/abs/2406.06007)] [[Project](https://cares-ai.github.io)]<br>

<div align=left>
<img src=asset/overview.png width=100% />
</div>

## Overview
This repo contains the source code of CARES. This study aims to assist researchers in gaining a better understanding of the reliable capabilities, limitations, and potential risks associated with deploying these advanced Medical Large Vision Language Models (Med-LVLMs). For further details, please refer to our paper.

*Peng Xia, Ze Chen, Juanxi Tian, Yangrui Gong, Ruibo Hou, Yue Xu, Zhenbang Wu, Zhiyuan Fan, Yiyang Zhou, Kangyu Zhu, Wenhao Zheng, Zhaoyang Wang, Xiao Wang, Xuchao Zhang, Chetan Bansal, Marc Niethammer, Junzhou Huang, Hongtu Zhu, Yun Li, Jimeng Sun, Zongyuan Ge, Gang Li, James Zou, Huaxiu Yao.*

This project is organized around the following five primary areas of trustworthiness, including:

1. Trustfulness

2. Fairness

3. Safety

4. Privacy

5. Robustness

## Project Structure
```
.
├── LICENSE
├── README.md
├── asset
│   └── overview.png
├── data
│   ├── HAM10000
│   │   ├── HAM10000_factuality.jsonl
│   │   └── images
│   ├── Harvard-FairVLMed
│   │   ├── fundus_factuality.jsonl
│   │   └── images
│   ├── IU-Xray
│   │   ├── images
│   │   └── iuxray_factuality.jsonl
│   ├── MIMIC-CXR
│   │   ├── mimic-cxr-jpg
│   │   └── mimic_factuality.jsonl
│   ├── OL3I
│   │   ├── OL3I_factuality.jsonl
│   │   └── images
│   ├── OmniMedVQA
│   │   ├── images
│   │   └── omnimedvqa_factuality.jsonl
│   └── PMC-OA
│       ├── images
│       └── pmcoa_factuality.jsonl
├── model
│   ├── LLaVA-Med
│   ├── Med-Flamingo
│   ├── MedVInT
│   └── RadFM
└── src
    ├── eval
    ├── modify_inputfile.py
    └── modify_inputfile.sh
```

## Getting Started
### Data Source
For certain datasets, you need firstly apply for the right of access and then download the dataset.

- [MIMIC-CXR](https://physionet.org/content/mimic-cxr-jpg/2.0.0/)
- [IU-Xray](https://drive.google.com/file/d/1c0BXEuDy8Cmm2jfN0YYGkQxFZd2ZIoLg/view) (Thanks to [R2GenGPT](https://github.com/wang-zhanyu/R2GenGPT) for sharing the file)
- [Harvard-FairVLMed](https://ophai.hms.harvard.edu/datasets/harvard-fairvlmed10k/)
- [OL3I](https://stanfordaimi.azurewebsites.net/datasets/3263e34a-252e-460f-8f63-d585a9bfecfc)
- [HAM10000](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/DBW86T)
- [PMC-OA](https://huggingface.co/datasets/axiong/pmc_oa)
- [OmniMedVQA](https://github.com/OpenGVLab/Multi-Modality-Arena)

### Test Files
Modify the format of the input files according to the requirements of different tasks or models. You need to set the input and output file paths yourself. The key is the selection of the model and task type. The models to choose from include `'llava-med', 'med-flamingo', 'medvint', 'radfm'`. The task options are `'uncertainty', 'jailbreak-1', 'jailbreak-2', 'jailbreak-3', 'overcautiousness-1', 'overcautiousness-2', 'overcautiousness-3', 'toxicity', 'privacy-z1', 'privacy-z2', 'privacy-f1', 'privacy-f2','robustness'`.

Then modify the variables in the script, and finally, execute the bash script.

` bash src/modify_inputfile.sh
`

### Evaluation Models
The medical large vision-language models involved include [LLaVA-Med](https://github.com/microsoft/LLaVA-Med/tree/v1.0.0), [Med-Flamingo](https://github.com/snap-stanford/med-flamingo), [MedVInT](https://github.com/xiaoman-zhang/PMC-VQA), and [RadFM](https://github.com/chaoyi-wu/RadFM). These need to be deployed based on their respective repositories in the corresponding `model` paths.

## Schedule

- [✅] Release the VQA data.

- [ ] Release the evaluation code.

## License

This project is licensed under the CC BY 4.0 - see the LICENSE file for details.

## Citation

```bibtex
@article{xia2024cares,
  title={CARES: A Comprehensive Benchmark of Trustworthiness in Medical Vision Language Models},
  author={Xia, Peng and Chen, Ze and Tian, Juanxi and Gong, Yangrui and Hou, Ruibo and Xu, Yue and Wu, Zhenbang and Fan, Zhiyuan and Zhou, Yiyang and Zhu, Kangyu and others},
  journal={arXiv preprint arXiv:2406.06007},
  year={2024}
}
```
