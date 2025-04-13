# ESC Data Visualizer
# Processes and plots telemetry data from tester code output

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

df0 = pd.read_csv('Efficiency-GaN.csv')
df1 = pd.read_csv('Efficiency-Si.csv')
df2 = pd.read_csv('Step-GaN.csv')
df3 = pd.read_csv('Step-Si.csv')
df4 = pd.read_csv('Step-GaN-Zoomed.csv')
df5 = pd.read_csv('Step-Si-Zoomed.csv')
df6 = pd.read_csv('Si_GaN_Step_Response_Derivative-Comparison_Zoomed.csv')

print("Read data")
df_efficiency = pd.DataFrame({'Si - TPH2R104PL': df1['Relative-Efficiency-Si'],'GaN - EPC2302': df0['Relative-Efficiency-GaN']})
#print(df_efficiency)
df_step = pd.DataFrame({'Si - TPH2R104PL': df3['ERPM-Si'],'GaN - EPC2302': df2['ERPM-GaN']})
delta = 0.030 # 30ms Telemetry
df_step_derivative = pd.DataFrame({'Si - TPH2R104PL': df3['ERPM-Si'],'GaN - EPC2302': df2['ERPM-GaN']})
df_step_derivative['Si - TPH2R104PL'] = df_step_derivative['Si - TPH2R104PL'].diff() / delta
df_step_derivative['GaN - EPC2302'] = df_step_derivative['GaN - EPC2302'].diff() / delta
df_step_derivative.fillna(0, inplace=True)  # Or use other method like forward fill
df_zoomed_step = pd.DataFrame({'Si - TPH2R104PL': df5['ERPM-Si'],'GaN - EPC2302': df4['ERPM-GaN']})

df_efficiency.to_csv('Si_GaN_Efficiency_Comparison.csv')
df_step.to_csv('Si_GaN_Step_Response_Comparison.csv')
df_step_derivative.to_csv('Si_GaN_Step_Response_Derivative-Comparison.csv')
print('Exported data')
print("Plotting data")

# Step Plot
sns.set_style("whitegrid")
plt.figure(figsize=(14, 7))
sns.lineplot(data=df_step,palette={'Si - TPH2R104PL': 'red', 'GaN - EPC2302': 'blue'}, dashes=False)
plt.title("Step Response (eRPM / Time) TPH2R104PL (1.6mOhm) vs EPC2302 (1.8mOhm)\nAM32 Firmware, Deadtime = 20, Variable PWM Frequency, Complementary PWM = ON\n80mm EDF @ 12000mAh 6s\n0% Throttle, 50% Throttle, 0% Throttle", fontsize=16, pad=15)
plt.xlabel('Time (30 ms Telemetry)', fontsize=10)
plt.ylabel('eRPM', fontsize=10)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Derivative Plot
sns.set_style("whitegrid")
plt.figure(figsize=(14, 7))
sns.lineplot(data=df_step_derivative,palette={'Si - TPH2R104PL': 'red', 'GaN - EPC2302': 'blue'}, dashes=False)
plt.title("Step Response Derivative (eRPM / Time^2) TPH2R104PL (1.6mOhm) vs EPC2302 (1.8mOhm)\nAM32 Firmware, Deadtime = 20, Variable PWM Frequency, Complementary PWM = ON\n80mm EDF @ 12000mAh 6s\n0% Throttle, 50% Throttle, 0% Throttle", fontsize=16, pad=15)
plt.xlabel('Time (30 ms Telemetry)', fontsize=10)
plt.ylabel('eRPM Rate of Change', fontsize=10)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Zoomed Step Plot
sns.set_style("whitegrid")
plt.figure(figsize=(14, 7))
sns.lineplot(data=df_zoomed_step,palette={'Si - TPH2R104PL': 'red', 'GaN - EPC2302': 'blue'}, dashes=False)
plt.title("Step Response Close-Up (eRPM / Time) TPH2R104PL (1.6mOhm) vs EPC2302 (1.8mOhm)\nAM32 Firmware, Deadtime = 20, Variable PWM Frequency, Complementary PWM = ON\n80mm EDF @ 12000mAh 6s\n0% Throttle, 50% Throttle, 0% Throttle", fontsize=16, pad=15)
plt.xlabel('Time (30 ms Telemetry)', fontsize=10)
plt.ylabel('eRPM', fontsize=10)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print(df6.head())
print(df6.columns)
# Zoomed Step Plot Derivative
sns.set_style("whitegrid")
plt.figure(figsize=(14, 7))
sns.lineplot(data=df6,palette={'Si - TPH2R104PL': 'red', 'GaN - EPC2302': 'blue'}, dashes=False)
plt.title("Step Response Derivative Close-Up (eRPM / Time^2) TPH2R104PL (1.6mOhm) vs EPC2302 (1.8mOhm)\nAM32 Firmware, Deadtime = 20, Variable PWM Frequency, Complementary PWM = ON\n80mm EDF @ 12000mAh 6s\n0% Throttle, 50% Throttle, 0% Throttle", fontsize=16, pad=15)
plt.xlabel('Time (30 ms Telemetry)', fontsize=10)
plt.ylabel('eRPM', fontsize=10)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Efficiency Plot
sns.set_style("whitegrid")
plt.figure(figsize=(14, 7))
sns.lineplot(data=df_efficiency,palette={'Si - TPH2R104PL': 'red', 'GaN - EPC2302': 'blue'}, dashes=False)
plt.title("Relative Efficiency [eRPM / W] TPH2R104PL (1.6mOhm) vs EPC2302 (1.8mOhm)\nAM32 Firmware, Deadtime = 20, Variable PWM Frequency, Complementary PWM = ON\n80mm EDF @ 12000mAh 6s\n10 Second Ramp To 50%, 5 Second Hold, 10 Second Ramp Down", fontsize=16, pad=15)
plt.xlabel('Time (30 ms Telemetry)', fontsize=10)
plt.ylabel('Relative Efficiency (eRPM / W)', fontsize=10)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


