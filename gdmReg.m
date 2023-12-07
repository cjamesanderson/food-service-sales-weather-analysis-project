function [theta, J_history] = gdmReg(X, y, theta, alpha, lambda, num_iters)
%GDMREG Performs gradient descent to learn theta
%   theta = GDMREG(x, y, theta, alpha, lambda, num_iters) updates theta by
%   taking num_iters gradient steps with learning rate alpha and regularization
%   parameter lambda

% Initialize some useful values
m = length(y); % number of training examples
J_history = zeros(num_iters, 1);

for iter = 1:num_iters


    % hypothesis vector
    h = X*theta;

    % errors vector
    err = h-y;

    change_theta = alpha*(1/m)*(X'*err);

    reg_theta = [theta(1); theta(2:end)*(1-alpha*(lambda/m))];

    theta = reg_theta - change_theta;


    % Save the cost J in every iteration    
    J_history(iter) = computeCostMulti(X, y, theta);

end

end
