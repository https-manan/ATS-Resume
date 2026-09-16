---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:3713
- loss:CosineSimilarityLoss
base_model: sentence-transformers/all-mpnet-base-v2
widget:
- source_sentence: Frontend Specialist bringing over 9 years of industry experience
    along with a verified Bachelors degree. Expert competencies cover React.js, Next.js,
    TypeScript, and Tailwind CSS. Proven success track record in refactoring legacy
    CSS into atomic design state containers.
  sentences:
  - Seeking a skilled Deep Learning Scientist to join our growing team. Key responsibilities
    include optimizing neural network tensor layers and inference latency pathways.
    Must be fully comfortable handling tools like Kubeflow, Triton Inference Server,
    Model Drift Tracking, and Docker in a fast-paced environment.
  - Seeking a skilled Senior Machine Learning Engineer to join our growing team. Key
    responsibilities include optimizing neural network tensor layers and inference
    latency pathways. Must be fully comfortable handling tools like Kubeflow, Triton
    Inference Server, Model Drift Tracking, and Docker in a fast-paced environment.
  - Seeking a skilled Senior Machine Learning Engineer to join our growing team. Key
    responsibilities include optimizing neural network tensor layers and inference
    latency pathways. Must be fully comfortable handling tools like PyTorch, Distributed
    TensorFlow, CUDA tuning, and Linux systems in a fast-paced environment.
- source_sentence: 'Machine Learning Specialist with 4 years working across active
    teams. Demonstrated technical execution and history background includes: Statistical
    Modeling, GenAI, K8s, Containerization. Seeking an engineering position to scale
    architectural patterns.'
  sentences:
  - 'We are looking for a Senior ML Engineer with a minimum of 8+ years of experience.
    The core technical stack requirements involve deep knowledge in: Python, Statistical
    Modeling, Artificial Intelligence, Container Orchestration Engine, Docker, AWS
    Cloud Platform. Must be highly capable of executing product deliverables in a
    fast paced workspace environment.'
  - 'We are looking for a Site Reliability Engineer with a minimum of 6+ years of
    experience. The core technical stack requirements involve deep knowledge in: Containerization,
    K8s, AWS, Terraform, Python3. Must be highly capable of executing product deliverables
    in a fast paced workspace environment.'
  - 'We are looking for a AI Infrastructure Architect with a minimum of 6+ years of
    experience. The core technical stack requirements involve deep knowledge in: Py3
    Engine, ML, GenAI, Container Orchestration Engine, Docker, AWS. Must be highly
    capable of executing product deliverables in a fast paced workspace environment.'
- source_sentence: React Architect bringing over 3 years of industry experience along
    with a verified Bachelors degree. Expert competencies cover Redux Toolkit, Webpack,
    JavaScript, and HTML5/CSS3. Proven success track record in optimizing client-side
    rendering vitals and component architectures.
  sentences:
  - Seeking a skilled Senior Machine Learning Engineer to join our growing team. Key
    responsibilities include building real-time feature stores and tracking continuous
    inference degradation. Must be fully comfortable handling tools like Kubeflow,
    Triton Inference Server, Model Drift Tracking, and Docker in a fast-paced environment.
  - Seeking a skilled Distributed Systems Software Architect to join our growing team.
    Key responsibilities include authoring secure distributed services capable of
    managing millions of requests concurrently. Must be fully comfortable handling
    tools like Golang programming, gRPC layers, Kubernetes orchestration, and PostgreSQL
    profiling in a fast-paced environment.
  - Seeking a skilled Mobile Systems App Engineer to join our growing team. Key responsibilities
    include building highly responsive mobile applications featuring custom touch
    gestures. Must be fully comfortable handling tools like React Native modules,
    native bridge architectures, and offline mobile synchronization in a fast-paced
    environment.
- source_sentence: 'Deep Learning Practitioner with 7 years working across active
    teams. Demonstrated technical execution and history background includes: Python3,
    Predictive AI, Artificial Intelligence, Container Orchestration Engine, Containerization,
    AWS. Seeking an engineering position to scale architectural patterns.'
  sentences:
  - 'We are looking for a Quantitative Analytics Expert with a minimum of 8+ years
    of experience. The core technical stack requirements involve deep knowledge in:
    Py3 Engine, PgSQL, Predictive AI, GenAI, Cloud Infrastructure (AWS). Must be highly
    capable of executing product deliverables in a fast paced workspace environment.'
  - 'We are looking for a AI Infrastructure Architect with a minimum of 5+ years of
    experience. The core technical stack requirements involve deep knowledge in: Py3
    Engine, Statistical Modeling, Artificial Intelligence, K8s, Containerization,
    AWS. Must be highly capable of executing product deliverables in a fast paced
    workspace environment.'
  - 'We are looking for a Senior Data Scientist with a minimum of 3+ years of experience.
    The core technical stack requirements involve deep knowledge in: Python3, Postgres,
    Statistical Modeling, Artificial Intelligence, Amazon Web Services. Must be highly
    capable of executing product deliverables in a fast paced workspace environment.'
- source_sentence: DevOps Site Reliability Engineer bringing over 6 years of industry
    experience along with a verified Bachelors degree. Expert competencies cover Jenkins
    pipelines, Docker container networks, and GitHub Actions. Proven success track
    record in building end-to-end continuous deployment orchestration pipelines.
  sentences:
  - 'We are looking for a Quantitative Analytics Expert with a minimum of 3+ years
    of experience. The core technical stack requirements involve deep knowledge in:
    Python, Relational DB Engine, ML, Artificial Intelligence, Amazon Web Services.
    Must be highly capable of executing product deliverables in a fast paced workspace
    environment.'
  - Seeking a skilled MLOps Infrastructure Architect to join our growing team. Key
    responsibilities include optimizing neural network tensor layers and inference
    latency pathways. Must be fully comfortable handling tools like PyTorch, Distributed
    TensorFlow, CUDA tuning, and Linux systems in a fast-paced environment.
  - Seeking a skilled SecOps Infrastructure Engineer to join our growing team. Key
    responsibilities include enforcing strict identity isolation boundaries and zero-trust
    cloud network rules. Must be fully comfortable handling tools like VPC network
    isolation rules, Web Application Firewalls (WAF), and transit gateways in a fast-paced
    environment.
pipeline_tag: sentence-similarity
library_name: sentence-transformers
metrics:
- pearson_cosine
- spearman_cosine
model-index:
- name: SentenceTransformer based on sentence-transformers/all-mpnet-base-v2
  results:
  - task:
      type: semantic-similarity
      name: Semantic Similarity
    dataset:
      name: ats val
      type: ats-val
    metrics:
    - type: pearson_cosine
      value: 0.9756155665502572
      name: Pearson Cosine
    - type: spearman_cosine
      value: 0.9194362827875835
      name: Spearman Cosine
---

# SentenceTransformer based on sentence-transformers/all-mpnet-base-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2). It maps sentences & paragraphs to a 768-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) <!-- at revision e8c3b32edf5434bc2275fc9bab85f82640a19130 -->
- **Maximum Sequence Length:** 384 tokens
- **Output Dimensionality:** 768 dimensions
- **Similarity Function:** Cosine Similarity
- **Supported Modality:** Text
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'MPNetModel'})
  (1): Pooling({'embedding_dimension': 768, 'pooling_mode': 'mean', 'include_prompt': True})
  (2): Normalize({})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```
Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'DevOps Site Reliability Engineer bringing over 6 years of industry experience along with a verified Bachelors degree. Expert competencies cover Jenkins pipelines, Docker container networks, and GitHub Actions. Proven success track record in building end-to-end continuous deployment orchestration pipelines.',
    'Seeking a skilled SecOps Infrastructure Engineer to join our growing team. Key responsibilities include enforcing strict identity isolation boundaries and zero-trust cloud network rules. Must be fully comfortable handling tools like VPC network isolation rules, Web Application Firewalls (WAF), and transit gateways in a fast-paced environment.',
    'We are looking for a Quantitative Analytics Expert with a minimum of 3+ years of experience. The core technical stack requirements involve deep knowledge in: Python, Relational DB Engine, ML, Artificial Intelligence, Amazon Web Services. Must be highly capable of executing product deliverables in a fast paced workspace environment.',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 768]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.6519, 0.4802],
#         [0.6519, 1.0000, 0.4726],
#         [0.4802, 0.4726, 1.0000]])
```
<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

## Evaluation

### Metrics

#### Semantic Similarity

* Dataset: `ats-val`
* Evaluated with [<code>EmbeddingSimilarityEvaluator</code>](https://sbert.net/docs/package_reference/sentence_transformer/evaluation.html#sentence_transformers.sentence_transformer.evaluation.EmbeddingSimilarityEvaluator)

| Metric              | Value      |
|:--------------------|:-----------|
| pearson_cosine      | 0.9756     |
| **spearman_cosine** | **0.9194** |

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 3,713 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>label</code>
* Approximate statistics based on the first 100 samples:
  |          | sentence_0                                                                         | sentence_1                                                                         | label                                                           |
  |:---------|:-----------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|:----------------------------------------------------------------|
  | type     | string                                                                             | string                                                                             | float                                                           |
  | modality | text                                                                               | text                                                                               |                                                                 |
  | details  | <ul><li>min: 36 tokens</li><li>mean: 58.07 tokens</li><li>max: 74 tokens</li></ul> | <ul><li>min: 58 tokens</li><li>mean: 66.52 tokens</li><li>max: 76 tokens</li></ul> | <ul><li>min: 0.06</li><li>mean: 0.6</li><li>max: 0.95</li></ul> |
* Samples:
  | sentence_0                                                                                                                                                                                                                                                                                                                          | sentence_1                                                                                                                                                                                                                                                                                                                                                                      | label               |
  |:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------|
  | <code>Digital Marketing Manager bringing over 5 years of industry experience along with a verified Diploma. Expert competencies cover ROAS optimization frameworks, email automation drip sequences, and content strategy. Proven success track record in scaling organic search visibility metrics and ad campaign budgets.</code> | <code>Seeking a skilled Server-Side Developer to join our growing team. Key responsibilities include remediating core latency bottleneck conditions across internal database schemas. Must be fully comfortable handling tools like Java, Spring Boot framework, microservices decoupling, and Apache Kafka streams in a fast-paced environment.</code>                         | <code>0.1442</code> |
  | <code>React Developer with 2 years working across active teams. Demonstrated technical execution and history background includes: Self-taught concepts in ReactJS, Familiar with Node.js, PgSQL, Typed JavaScript. Seeking an engineering position to scale architectural patterns.</code>                                          | <code>We are looking for a Full Stack Developer with a minimum of 5+ years of experience. The core technical stack requirements involve deep knowledge in: JavaScript, React, Node, PostgreSQL, TS, Docker Containers. Must be highly capable of executing product deliverables in a fast paced workspace environment.</code>                                                   | <code>0.2103</code> |
  | <code>Terraform Engineer with 5 years working across active teams. Demonstrated technical execution and history background includes: Basic understanding of OCI Containers, Container Orchestration Engine, Terraform, Basic understanding of Python3. Seeking an engineering position to scale architectural patterns.</code>      | <code>We are looking for a Infrastructure Platform Architect with a minimum of 6+ years of experience. The core technical stack requirements involve deep knowledge in: Containerization, Kubernetes, Cloud Infrastructure (AWS), Infrastructure as Code (IaC), Python3. Must be highly capable of executing product deliverables in a fast paced workspace environment.</code> | <code>0.5575</code> |
* Loss: [<code>CosineSimilarityLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#cosinesimilarityloss) with these parameters:
  ```json
  {
      "loss_fct": "torch.nn.modules.loss.MSELoss",
      "cos_score_transformation": "torch.nn.modules.linear.Identity"
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `num_train_epochs`: 10
- `fp16`: True
- `per_device_eval_batch_size`: 16
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 16
- `num_train_epochs`: 10
- `max_steps`: -1
- `learning_rate`: 5e-05
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_steps`: 0
- `optim`: adamw_torch_fused
- `optim_args`: None
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `optim_target_modules`: None
- `gradient_accumulation_steps`: 1
- `average_tokens_across_devices`: True
- `max_grad_norm`: 1
- `label_smoothing_factor`: 0.0
- `bf16`: False
- `fp16`: True
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `use_cache`: False
- `neftune_noise_alpha`: None
- `torch_empty_cache_steps`: None
- `auto_find_batch_size`: False
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `include_num_input_tokens_seen`: no
- `log_level`: passive
- `log_level_replica`: warning
- `disable_tqdm`: False
- `project`: huggingface
- `trackio_space_id`: None
- `trackio_bucket_id`: None
- `trackio_static_space_id`: None
- `per_device_eval_batch_size`: 16
- `prediction_loss_only`: True
- `eval_on_start`: False
- `eval_do_concat_batches`: True
- `eval_use_gather_object`: False
- `eval_accumulation_steps`: None
- `include_for_metrics`: []
- `batch_eval_metrics`: False
- `save_only_model`: False
- `save_on_each_node`: False
- `enable_jit_checkpoint`: False
- `push_to_hub`: False
- `hub_private_repo`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_always_push`: False
- `hub_revision`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `restore_callback_states_from_checkpoint`: False
- `full_determinism`: False
- `seed`: 42
- `data_seed`: None
- `use_cpu`: False
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `dataloader_prefetch_factor`: None
- `dataloader_multiprocessing_context`: None
- `dataloader_in_order`: True
- `remove_unused_columns`: True
- `label_names`: None
- `train_sampling_strategy`: random
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `ddp_static_graph`: None
- `ddp_backend`: None
- `ddp_timeout`: 1800
- `fsdp`: None
- `fsdp_config`: None
- `deepspeed`: None
- `debug`: []
- `skip_memory_metrics`: True
- `do_predict`: False
- `resume_from_checkpoint`: None
- `local_rank`: -1
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin
- `router_mapping`: {}
- `learning_rate_mapping`: {}
- `warmup_ratio`: None

</details>

### Training Logs
| Epoch  | Step | Training Loss | ats-val_spearman_cosine |
|:------:|:----:|:-------------:|:-----------------------:|
| 1.0    | 233  | -             | 0.8994                  |
| 2.0    | 466  | -             | 0.9142                  |
| 2.1459 | 500  | 0.0174        | -                       |
| 3.0    | 699  | -             | 0.9130                  |
| 4.0    | 932  | -             | 0.9149                  |
| 4.2918 | 1000 | 0.0056        | -                       |
| 5.0    | 1165 | -             | 0.9185                  |
| 6.0    | 1398 | -             | 0.9170                  |
| 6.4378 | 1500 | 0.0041        | -                       |
| 7.0    | 1631 | -             | 0.9181                  |
| 8.0    | 1864 | -             | 0.9194                  |


### Training Time
- **Training**: 6.7 minutes

### Framework Versions
- Python: 3.13.15
- Sentence Transformers: 5.7.0
- Transformers: 5.16.1
- PyTorch: 2.11.0+cu128
- Accelerate: 1.14.0
- Datasets: 4.8.5
- Tokenizers: 0.23.1

## Additional Resources

- [Training and Finetuning Embedding Models with Sentence Transformers](https://huggingface.co/blog/train-sentence-transformers): the end-to-end guide for training or finetuning Sentence Transformer models.
- [Introduction to Matryoshka Embedding Models](https://huggingface.co/blog/matryoshka): variable-size embeddings that can be truncated with minimal quality loss.
- [Binary and Scalar Embedding Quantization for Significantly Faster & Cheaper Retrieval](https://huggingface.co/blog/embedding-quantization): post-training compression of embedding vectors.
- [Multimodal Embedding & Reranker Models with Sentence Transformers](https://huggingface.co/blog/multimodal-sentence-transformers): use text, image, audio, and video models through the same API.
- [Training and Finetuning Multimodal Embedding & Reranker Models with Sentence Transformers](https://huggingface.co/blog/train-multimodal-sentence-transformers): train multimodal embedding models, with a Visual Document Retrieval walkthrough.

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->