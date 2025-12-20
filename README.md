# Machine Translation Experiments

This repository contains experiments and evaluations for multiple machine translation models.  
The focus is on comparing different architectures using **BLEU score** as the primary evaluation metric.

---

## 🔗 Important Links

- 📄 **Reference**: [TF Tutorial](https://www.tensorflow.org/text/tutorials/nmt_with_attention)
- 💻 **Model Weights**:
  - **Transformer**: [Transformer (Hilsenki) Weights](https://www.kaggle.com/models/yassienwasfy/transformer/)
  - **RNN / LSTM / GRU**: [RNN/ LSTM/ GRU](https://www.kaggle.com/models/yassienwasfy/translation-weights/)


---

## 📊 BLEU Score Comparison

The following table summarizes the BLEU scores obtained by three different models on the same test set.

| Model | Architecture | BLEU Score |
|------|--------------|------------|
| Model 1 | (RNN + Attention) | **20.67** |
| Model 2 | (LSTM + Attention) | **21.47** |
| Model 3 | (LSTM + Attention) | **24.06** |

---

## 🧪 Evaluation Details

- **Metric**: BLEU (SacreBLEU)
