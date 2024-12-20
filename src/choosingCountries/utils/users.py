import matplotlib.pyplot as plt
import pandas as pd

def plot_users(users):
    
    users = users.dropna(subset=['location'])
    print("Number of users with known locations:", users.shape[0])


    user_counts = users.groupby('location').size().reset_index(name='total_users')
    user_counts = user_counts[user_counts['total_users'] >= 100]
    user_counts = user_counts.sort_values(by='total_users', ascending=False)
    user_counts['color'] = user_counts['location'].apply(lambda x: 'red' if x.startswith('United States,') else 'blue')

    plt.figure(figsize=(8, 5))
    plt.bar(user_counts['location'], user_counts['total_users'], color=user_counts['color'], )
    plt.xlabel('Location')
    plt.ylabel('Total Users')

    red_patch = plt.Line2D([0], [0], color='red', lw=4, label='United States')
    blue_patch = plt.Line2D([0], [0], color='blue', lw=4, label='Other Countries')
    plt.legend(handles=[red_patch, blue_patch], bbox_to_anchor=(1, 1), frameon=False)

    plt.title('Total number of users by location (>100 users)')
    plt.xticks([])
    plt.tight_layout()
    plt.show()
    
    return