
file_name = '9x9_ultra_long_run.dat';
pop_size = 2000;
title('16x16 Run 2')
table = readtable(file_name);
hold on
avg = [];
best = [];
generation = [];
for i=1:pop_size
    A = table(table.Generation == i-1, :);
    avg = [avg, mean(A.Fitness)];
    best = [best, max(A.Fitness)];
    generation = [generation, A.Generation(1)];
    scatter(A.Generation,A.Fitness);
end
plot(generation,avg,'r')
plot(generation,best,'b')
legend('Average Fitness','Best Fitness')
xlabel('Generation')
ylabel('Fitness')
hold off
