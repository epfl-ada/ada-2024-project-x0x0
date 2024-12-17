import matplotlib.pyplot as plt

def state_scatter_plot(ratings_comparison):
    
    plt.figure(figsize=(12, 8))

    #dots for better visibility
    plt.scatter(ratings_comparison.index, ratings_comparison['own_beer_avg'], label='Own Ratings', color='blue', s=100, zorder=2)
    plt.scatter(ratings_comparison.index, ratings_comparison['other_states_avg'], label='Other States Ratings', color='orange', s=100, zorder=2)

    #lines connecting the dots for visibility
    for i in range(len(ratings_comparison)):
        plt.plot([ratings_comparison.index[i], ratings_comparison.index[i]], 
                [ratings_comparison['own_beer_avg'][i], ratings_comparison['other_states_avg'][i]], 
                color='gray', linestyle='--')

    plt.xlabel('State')
    plt.ylabel('Average Rating')
    plt.title('Comparison of Own Ratings vs Other States Ratings')
    plt.xticks(rotation=90)
    plt.ylim(0,5)
    plt.legend()
    plt.tight_layout()

    plt.show()