%% Clear and Close Figures
clear ; close all; clc

fprintf('Loading data ...\n');

%% Load Data
weather = load('weather_data.csv');
X = weather(:, 2:end);
sales = load('sales_data.csv');
%sales = load('smoothies_data.csv');
%sales = load('food_data.csv');
%sales = load('food_sales_data.csv');
%sales = load('smoothie_sales_data.csv');
y = sales(:, 2);
m = length(y);

fprintf('Eliminating unused features...');

% Cull useless features
f_sums = sum(X);
for i = size(X, 2):-1:1
  if f_sums(i) == 0
    X = [X(:, 1:i-1) X(:, i+1:end)];
  end
end

fprintf(' %f \n', size(X, 2));

% Scale features and set them to zero mean
fprintf('Normalizing Features ...\n');

[X mu sigma] = featureNormalize(X);

% Add intercept term to X
X = [ones(m, 1) X];

% Run gradient descent
fprintf('Running gradient descent ...\n');

alpha = 0.01;
lambda = 0;
num_iters = 500;

% Init Theta and Run Gradient Descent
theta = zeros(size(X, 2), 1);
%[theta, J_history] = gradientDescentMulti(X, y, theta, alpha, num_iters);
[theta, J_history] = gdmReg(X, y, theta, alpha, lambda, num_iters);

% Plot convergence graph
%figure;
%plot(1:numel(J_history), J_history, '-b', 'LineWidth', 3);
%xlabel('Number of interations');
%ylabel('Cost J');

% Display gradient descent's result
fprintf('Theta computed from gradient descent: \n');
fprintf(' %f \n', theta);
fprintf('\n');

% Predict
fprintf('Generating predictions...\n');

predictions = X*theta;
r2 = calculateRSquared(y, predictions);

% Plot model
figure;
subplot(2,1,1);
plot(1:numel(y), y, '.b', 'MarkerSize', 3, 1:numel(predictions), predictions, '-r', 'LineWidth', 1);
xlim([0 numel(y)]);
xlabel('Days since open');
title('Daily Net Income');
legend('Actual', 'Predicted');
limits = axis();
r2str = sprintf('{R^2} = %f', r2);
text(limits(2)*0.03, limits(4)*0.93, r2str);

% Performance histogram

differences = y-predictions;
%figure;
%hist(differences, 30);

% 7-day average store performance v. model

mu7day = intervalMean(differences, 7);
%figure;
subplot(2,2,3);
plot(1:numel(mu7day), zeros(size(mu7day)), '--k', 1:numel(mu7day), mu7day, '-m',  'LineWidth', 1);
xlim([0 numel(y)]);
%xlabel('Time');
title('7-Day Average');
ylabel('(actual - predicted)');

% 30-day average store performance v. model


mu30day = intervalMean(differences, 30);
%figure;
subplot(2,2,4);
plot(1:numel(mu30day), zeros(size(mu30day)), '--k', 1:numel(mu30day), mu30day, '-m',  'LineWidth', 1);
xlim([0 numel(y)]);
%xlabel('Time');
title('30-day Average');

mu7day = intervalMean((y-(ones(size(y))*mean(y))), 30);
figure;
plot(1:numel(mu7day), ones(size(mu7day))*0, '--k', 1:numel(mu7day), mu7day, '-m', 'Linewidth', 2);
xlim([0 numel(y)]);
title('7-day Average (raw)');
