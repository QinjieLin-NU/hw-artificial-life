import matplotlib.pyplot as plt
import seaborn as sns
import os

seeds = [4575, 11887, 25072, 30830, 43602]
population_size = 20

fitness_list = {}
for s in seeds:
  children = os.listdir(f"./data/seed{s}")
  seed_fitness_list = []
  tmp_list = []
  for (i,c) in enumerate(children):
    file_name = f"./data/seed{s}/{c}/best_fitness.txt"
    with open(file_name, 'r') as f:
      fitness = float(f.read())
    if (i+1)%population_size == 0:
      seed_fitness_list.append(max(tmp_list))
    else:
      tmp_list.append(fitness)
  fitness_list[s] = seed_fitness_list
# print(fitness_list)
sns.set_theme()
for k in fitness_list:
  sns.lineplot(fitness_list[k],label=k)
plt.ylabel("Best Fitness"), plt.xlabel("Generation"), plt.show(), plt.legend()