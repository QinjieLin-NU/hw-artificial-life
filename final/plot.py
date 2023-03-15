import matplotlib.pyplot as plt
import seaborn as sns
import os

env_names = ["terrain"] #["obstacle", "step", "terrain",  "bumper"]
seeds = [3333] #[1111, 2222, 3333, 4444, 5555]
population_size = 20

for env_name in env_names:
  fitness_list = {}
  folder = f"./data/{env_name}"
  for s in seeds:
    children = os.listdir(f"{folder}/seed{s}")
    seed_fitness_list = []
    tmp_list = []
    _ = children.remove('bodybest') if 'bodybest' in children else None
    sorted_children = sorted(children, key=lambda x: int(x.replace("body","")))
    for (i,c) in enumerate(sorted_children):
      file_name = f"{folder}/seed{s}/{c}/best_fitness.txt"
      with open(file_name, 'r') as f:
        fitness = float(f.read())
      if (i+1)%population_size == 0:
        tmp_list.append(fitness)
        seed_fitness_list.append(max(tmp_list))
        max_index = tmp_list.index(max(tmp_list))
        print(f"{env_name}, seed {s}, maximum folder: {sorted_children[max_index]}, maximum index {max_index}, maximum value {max(tmp_list)}")
      else:
        tmp_list.append(fitness)
    fitness_list[s] = seed_fitness_list
  # print(fitness_list)
  sns.set_theme()
  for k in fitness_list:
    sns.lineplot(fitness_list[k],label=k)
  plt.title(f"{env_name}")
  plt.ylabel("Best Fitness"), plt.xlabel("Generation"), plt.show(), plt.legend()