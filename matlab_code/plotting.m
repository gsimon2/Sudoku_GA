%% Creates a scatter plot of the fitnesses for each generation and overlays a plot of average and best fitness
%
% Must be in the logs directory
%
% GAS 10-26-17

file_name = '9x9_run1.dat';
gen_count = 500;
title('9x9 Run 1')
table = readtable(file_name);
hold on
avg = [];
best = [];
generation = [];

% loop through each generation
for i=0:gen_count
    
    % Create a table of just the individuals from this generation
    A = table(table.Generation == i, :);
    
    % For each generation add to the arrays tracking the average and best
    % fitnesss as well as the one for generations
    avg = [avg, mean(A.Fitness)];
    best = [best, max(A.Fitness)];
    generation = [generation, A.Generation(1)];
    
    % Create a scattor plot for this generatin
    %   for the two arrays need to be the same size since it does pairwise
    %   matching
    scatter(A.Generation,A.Fitness);
end

% Plot average line in red and best in blue
plot(generation,avg,'r')
plot(generation,best,'b')
legend('Average Fitness','Best Fitness')
xlabel('Generation')
ylabel('Fitness')
hold off
