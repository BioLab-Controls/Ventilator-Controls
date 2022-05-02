data = csvread("data.csv");
%Separate flow 
flow_values = data(1,:);
%Separate time 
time_values = data(2,1);
complete = [1:time_values];
%Plot values vs time '
plot(flow_values);
