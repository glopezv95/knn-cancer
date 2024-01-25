import matplotlib.pyplot as plt

from functions import test_knn, generate_knn_line
from data import df

checklist = []
combinations = range(1, 4)

for combination in combinations:
    t = test_knn(
        dataframe = df,
        drop_columns = ['diagnosis', 'type'],
        y = 'diagnosis',
        n_columns = combination,
        max_k = 16)
    
    checklist.append(t)
    
accuracy_dict = {i:checklist[i-1]['best_accuracy'] for i in combinations}
k_dict = {i:checklist[i-1]['best_k'] for i in combinations}

fig, axes = plt.subplots(nrows = 1, ncols = 2)

axes[0].bar([str(i) for i in accuracy_dict.keys()], accuracy_dict.values())
axes[0].set_ylim(min(accuracy_dict.values()) - .05, max(accuracy_dict.values()) + .05)

axes[1].bar([str(i) for i in k_dict.keys()], k_dict.values())
axes[1].set_ylim(min(k_dict.values()) - 1, max(k_dict.values()) + 1)

selected_combination = 1
selected_accuracy = checklist[selected_combination - 1]['best_accuracy']
selected_k = k_dict[selected_combination]
selected_columns = list(checklist[selected_combination - 1]['best_combination'])