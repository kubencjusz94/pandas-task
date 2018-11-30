import pandas as pd
import numpy as np
import matplotlib as plt

#INPUT DATA
budget = 2000000
periods = 12
max_touchpoint = 6
cpp_list = [1000, 1200, 1400, 800, 900, 2000]

#available weeks per Flight input
min_on_air = 2
min_off_air = 3
max_on_air = 4
max_off_air = 5

#creating DataFrame from 'available weeks per Flight' input
dict = {'min': [min_on_air, min_off_air], 'max' : [max_on_air, max_off_air]}
available_weeks_per_flight = pd.DataFrame(data = dict)
available_weeks_per_flight.rename(index ={0:'On-Air', 1:'Off-Air'}, inplace = True)
#print(available_weeks_per_flight)

#creating data DataFrame
dict2 = {'touchpoint': range(1,7), 'cpp': cpp_list}
df = pd.DataFrame(data = dict2)
df.set_index('touchpoint', inplace = True)
#print(df)

#adding 'Rand' column
df = df.assign(rand = lambda x: np.random.random(size = 6))
#df = df.assign(rand = lambda x: [0.86, 0.89, 0.81, 0.68, 0.43, 0.22])

#adding 'Share of Budget' column
sum_rand_col = df.rand.sum()
df = df.assign(share_of_budget = lambda x: 100 * df.rand/sum_rand_col )

sum_shere_of_budg_col = df.share_of_budget.sum()

#adding 'Budget' column
df = df.assign(budget = lambda x: budget*(df.share_of_budget / 100))

sum_budget_col = df.budget.sum()

#adding 'Grps_Total' column
df = df.assign(grps_total = lambda x: df.budget/df.cpp)

sum_grps_total_col = df.grps_total.sum()

#adding 'On Air Weeks per Flight' column
df = df.assign(on_air_weeks_per_flight = lambda x: np.random.choice(range(min_on_air, max_on_air + 1), size = 6))
#df = df.assign(on_air_weeks_per_flight = lambda x: [3, 2, 2, 4, 4, 2])

#adding 'Off Air Weeks Per Flight' column
df = df.assign(off_air_weeks_per_flight = lambda x: np.random.choice(range(min_off_air, max_off_air + 1), size = 6))
#df = df.assign(off_air_weeks_per_flight = lambda x: 6*[3])

#adding 'Flight Weeks' column
df = df.assign(flight_weeks = lambda x: df.on_air_weeks_per_flight + df.off_air_weeks_per_flight)

#adding 'Full Flights' column
df = df.assign(full_flights = lambda x: periods//df.flight_weeks)
print(df)

#adding 'On Air Weeks Total' column
df = df.assign(on_air_weeks_total = lambda x: (df.full_flights * df.on_air_weeks_per_flight + min(df.on_air_weeks_per_flight.iloc[-1], periods % df.flight_weeks.iloc[-1])))

#adding 'GPRs per Week' column
df = df.assign(gprs_per_week = lambda x: df.grps_total / df.on_air_weeks_total)

#creating first algorithm DataFrame
algorithm_step1_df = pd.DataFrame(columns = ['touchpoint'] + range(1, periods+1))
algorithm_step1_df.set_index('touchpoint', inplace = True)

for i in range(max_touchpoint):
    algorithm_step1_df.loc[i+1] = [ j // df.flight_weeks.loc[i+1] for j in range(periods)]
#print(algorithm_step1_df)

#creating second algorithm DataFrame
algorithm_step2_df = pd.DataFrame(columns = ['touchpoint'] + range(1, periods+1))
algorithm_step2_df.set_index('touchpoint', inplace = True)

for k in range(max_touchpoint):
    algorithm_step2_df.loc[k+1] = [((l+1) - algorithm_step1_df.iat[k, l]*df.flight_weeks.loc[k+1]) for l in range(periods)]
#print(algorithm_step2_df)

#creating output DataFrame
output_df = pd.DataFrame(columns = ['touchpoint'] + range(1, periods+1))
output_df.set_index('touchpoint', inplace = True)

for k in range(max_touchpoint):
    for l in range(periods):
        if algorithm_step2_df.iat[k, l] <= df.on_air_weeks_per_flight.loc[k+1]:
            output_df.loc[k+1] = df.gprs_per_week.loc[k+1]
        else: output_df.loc[k+1] = 0
graph = output_df.plot.bar()
