from collections import defaultdict
import pandas as pd



def build_groups(final_cohen_df):  #from plot_cohen_d
    #sort the DataFrame by Cohen's d in ascending order
    sorted_cohen_df = final_cohen_df.sort_values(by='Cohen_d', key=abs)

    state_groups = []
    assigned_states = set()

    for _, row in sorted_cohen_df.iterrows():
        if row['Cohen_d'] >= 2:
            continue

        state1 = row['State1']
        state2 = row['State2']

        # Skip if both states are already assigned
        if state1 in assigned_states and state2 in assigned_states:
            continue

        group_found = False

        # Check if either state is in any existing group
        for group in state_groups:
            if state1 in group['States'] or state2 in group['States']:
                if state1 not in group['States']:
                    group['States'].append(state1)
                    assigned_states.add(state1)
                if state2 not in group['States']:
                    group['States'].append(state2)
                    assigned_states.add(state2)
                
                group_found = True
                break

        # If no group was found, create a new one
        if not group_found:
            state_groups.append({'States': [state1, state2]})
            assigned_states.update([state1, state2])

    print("State Groups:")
    print("-" * 50)
    for group in state_groups:
        states = ", ".join(group['States'])
        print(f"States: {states}")
        print("-" * 50)

    double_check(state_groups)

    return state_groups


def double_check(state_groups):
    #list of all 50 U.S. states
    us_states_list = [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
        'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 
        'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 
        'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 
        'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 
        'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 
        'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 
        'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 
        'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
    ]

    #flatten the list of states and count occurrences
    state_occurrences = defaultdict(int)
    for group in state_groups:
        for state in group['States']:
            state_occurrences[state] += 1

    states_in_multiple_groups = {state for state, count in state_occurrences.items() if count > 1}

    #check for missing and extra states
    grouped_states = set(state_occurrences.keys())
    missing_states = set(us_states_list) - grouped_states
    extra_states = grouped_states - set(us_states_list)

    print("Summary of State Groups Check:")
    print("-" * 40)

    if missing_states:
        print("Missing States (not included in state_groups):")
        for state in sorted(missing_states):
            print(f" - {state}")
    else:
        print("All 50 states are included in state_groups.")

    print("\n" + "-" * 40)

    if extra_states:
        print("Extra States (invalid entries in state_groups):")
        for state in sorted(extra_states):
            print(f" - {state}")
    else:
        print("No extra states found in state_groups.")

    print("\n" + "-" * 40)

    if states_in_multiple_groups:
        print("States Present in Multiple Groups:")
        for state in sorted(states_in_multiple_groups):
            print(f" - {state}")
    else:
        print("No states are present in multiple groups.")

    print("-" * 40)
    
    return