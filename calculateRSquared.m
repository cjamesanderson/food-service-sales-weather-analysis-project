function R2 = calculateRSquared(y, y_predict)
% CALCULATERSQUARED Calculate the coeffecient of determination from observations
%                   vector y and predicted values vector y_predict

mu = mean(y)*ones(size(y));

ss_tot = sum((y-mu).^2);
ss_res = sum((y-y_predict).^2);

R2 = 1 - ss_res/ss_tot;
