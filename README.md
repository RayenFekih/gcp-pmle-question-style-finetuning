# GCP PMLE Question Style Fine-Tuning

This project explores whether supervised fine-tuning can teach a language model to generate Google Professional Machine Learning Engineer (PMLE) style certification questions.

## Goal

Given topic notes or Google Cloud documentation, generate:

- Realistic business scenarios
- Multiple-choice questions
- Plausible distractors
- One best answer
- Explanations

The focus is on learning question style rather than memorizing existing exam content.

## Planned Steps

- [ ] Collect and clean source questions
- [ ] Create training dataset
- [ ] Fine-tune a model
- [ ] Compare base vs fine-tuned outputs
- [ ] Evaluate question quality