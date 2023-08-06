# Optibot

> Create splinters like this

```
{{ optiid("splinter1") }}

{{ optitask("model") }}
{{ optitask("train") }}
{{ optitask("classification") }}

{{ optiimport("from sklearn.ensemble import RandomForestClassifier")}}

{{ optivar("model")}}
{{ optivar("X")}}
{{ optivar("y")}}

{{ optiparam("n_estimators", "int", min=0, max=100) }}
{{ optiparam("random_state", "float", min=0, max=40000) }}

---

# Train a Lasso model with alpha=0.1
{{model}} = RandomForestClassifier(n_estimators={{n_estimators}}, random_state={{random_state}})
{{model}}.fit({{X}}, {{y}})


```

> Use them in scripts templates like this

```
import numpy as np
{{ imports() }}

# Load data from CSV file using NumPy
data = np.loadtxt("data.csv", delimiter=",")

# Split the data into features (X) and labels (y)
features = data[:, :-1]
labels = data[:, -1]

# Train a classifier
{{ splinter("train", "model.train.classification", X="features", y="labels", model="clf") }}

# Test the trained classifier
score = clf.score(features, labels)
print("Accuracy: {:.2f}%".format(score * 100))

```

> Generate random scripts with them

```
from src.optibot.core.optibot import OptiBot

bot = OptiBot()
bot.preload_splinters_from_path("./templates/splinters/*")
bot.preload_templates_from_path("./templates/scripts/*")
bot.compile()

for x in range(10):
    subject = list(bot.generate_script())

    with open(f"subject_{x + 1}.py", "w") as fp:
        fp.write(bot.render("simple.jinja", subject))

```
