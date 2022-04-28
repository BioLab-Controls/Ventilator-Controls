data = readmatrix("data.csv");
%Separate flow 
flow_values = data(:,1);
%Separate time 
time_values = data(:,2);
%Plot values vs time '
plot(flow_values, time_values);