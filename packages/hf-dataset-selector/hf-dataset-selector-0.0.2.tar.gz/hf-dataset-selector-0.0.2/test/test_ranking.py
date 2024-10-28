from hfselect import Dataset, compute_task_ranking

dataset = Dataset.from_hugging_face(name="glue",
                                    split="train",
                                    text_col=["premise", "hypothesis"],
                                    label_col="label",
                                    is_regression=False,
                                    subset="mnli",
                                    num_examples=1000,
                                    seed=42)

task_ranking = compute_task_ranking(
    dataset=dataset,
    model_name="bert-base-multilingual-uncased"
)

print(task_ranking)